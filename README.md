# 📘 Ultimate Video & Website Summarizer

A powerful Streamlit application that transcribes and summarizes **YouTube videos** and **web content** using **OpenAI's Whisper and GPT-3.5**. It includes sentiment analysis, timestamped highlights, multi-language summaries, and download options.

---

## 🚀 Live Demo
👉 [Deployed App](https://smart-media-summarizer-gbn9r6ajxtt3jvajtmtf7e.streamlit.app)

---

## 🎯 Features

### 🎥 Video Summarization
- Extract audio from YouTube via `yt_dlp`
- Transcribe audio using OpenAI Whisper API
- Timestamped transcript segments
- Metadata: title, channel, description, thumbnail
- Sentiment analysis
- GPT-powered summary in selected language and style
- Downloadable `.txt` summary

### 🌐 Website Summarization
- Extract main content from any URL
- GPT-generated summaries
- Sentiment analysis
- Downloadable summaries

### ⚙️ Customization
- Select summary detail: **Brief**, **Detailed**, or **Bullet Points**
- Output summaries in: **English**, **Spanish**, **French**, **German**, **Hindi**

---

## 🛠️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 3. Add ffmpeg Support for Audio Processing
For **Streamlit Cloud**, create a `packages.txt` with:
```txt
ffmpeg
```

For local installs:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 4. Set OpenAI API Key
Create an `.env` file or export in your terminal:
```bash
export OPENAI_API_KEY=your-secret-key
```

### 5. Run the App
```bash
streamlit run app.py
```

---

## 📦 Project Structure
```
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── packages.txt         # OS-level packages (e.g., ffmpeg)
└── README.md            # This file
```

---


## 📄 License
[MIT](LICENSE)

---

## 🙌 Acknowledgments
- [OpenAI Whisper + GPT-3.5](https://openai.com/)
- [Streamlit](https://streamlit.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [TextBlob](https://textblob.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

## 🛣️ Roadmap Ideas
- 🎙️ Support local audio/video uploads
- 📂 Export summaries as PDF/Word
- 🔗 Google Drive integration
- 🧩 Multi-video summarization session

