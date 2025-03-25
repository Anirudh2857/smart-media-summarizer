import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import tempfile
import os
from moviepy.editor import AudioFileClip
import yt_dlp
from textblob import TextBlob
from openai import OpenAI
import base64
from datetime import datetime
import json

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to summarize text with adjustable length
def summarize_text(text, detail_level, language="English"):
    prompt = f"Summarize the following text in {detail_level} detail in {language}:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# Extract text from a website URL
def get_website_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    return ' '.join(paragraphs)

# Sentiment Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Download link generator
def generate_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'

# Extract video metadata
def get_video_metadata(video_url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return {
            "title": info.get("title"),
            "channel": info.get("uploader"),
            "thumbnail": info.get("thumbnail"),
            "description": info.get("description")
        }

# Extract audio using yt_dlp, convert to mp3, and transcribe with timestamps
def extract_and_transcribe(video_url):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'audio.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            mp3_file_path = os.path.join(temp_dir, 'audio.mp3')

            with open(mp3_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            full_text = transcript.text
            segments = transcript.segments
            timestamped = [
                f"[{str(datetime.utcfromtimestamp(seg.start).strftime('%H:%M:%S'))}] {seg.text}"
                for seg in segments
            ]
            return full_text, "\n".join(timestamped)

        except Exception as e:
            st.error(f"Error during audio download or transcription: {e}")
            return "", ""

# Streamlit UI
st.title("Ultimate Video & Website Summarizer")

# Sidebar controls
st.sidebar.header("🛠️ Settings")
detail_level = st.sidebar.selectbox("Select Summary Detail Level", ["brief", "detailed", "bullet points"])
language = st.sidebar.selectbox("Select Output Language", ["English", "Spanish", "French", "German", "Hindi"])

# Tabs for Video and Website summarization
tab1, tab2 = st.tabs(["🎥 Video Summarizer", "🌐 Website Summarizer"])

with tab1:
    st.header("Video Summarization")
    video_url = st.text_input("Enter YouTube Video URL:")

    if st.button("Summarize Video"):
        metadata = get_video_metadata(video_url)
        st.subheader("Video Metadata")
        st.markdown(f"**Title:** {metadata['title']}")
        st.markdown(f"**Channel:** {metadata['channel']}")
        st.image(metadata['thumbnail'], width=300)
        st.markdown(f"**Description:**\n{metadata['description'][:500]}...")

        with st.spinner('Extracting and transcribing...'):
            full_transcript, timestamped_transcript = extract_and_transcribe(video_url)

        if full_transcript:
            st.subheader("📝 Full Transcript")
            st.text_area("Transcript", full_transcript, height=200)

            st.subheader("⏱️ Timestamped Highlights")
            st.text_area("With Timestamps", timestamped_transcript, height=200)

            polarity, subjectivity = analyze_sentiment(full_transcript)
            st.markdown(f"**Sentiment Polarity:** {polarity:.2f}, **Subjectivity:** {subjectivity:.2f}")

            with st.spinner('Generating summary...'):
                summary = summarize_text(full_transcript, detail_level, language)
            st.subheader("📌 Summary:")
            st.write(summary)
            st.markdown(generate_download_link(summary, "video_summary.txt"), unsafe_allow_html=True)

with tab2:
    st.header("Website Summarization")
    website_url = st.text_input("Enter Website URL:")

    if st.button("Summarize Website"):
        with st.spinner('Fetching content...'):
            web_text = get_website_text(website_url)
        st.subheader("🌐 Website Content")
        st.text_area("Raw Text", web_text[:2000], height=300)

        polarity, subjectivity = analyze_sentiment(web_text)
        st.markdown(f"**Sentiment Polarity:** {polarity:.2f}, **Subjectivity:** {subjectivity:.2f}")

        with st.spinner('Generating summary...'):
            summary = summarize_text(web_text, detail_level, language)
        st.subheader("📌 Summary:")
        st.write(summary)
        st.markdown(generate_download_link(summary, "website_summary.txt"), unsafe_allow_html=True)