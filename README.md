# 🎙️ Whisper AI Speech-to-Text Transcriber 

An incredibly fast, fully offline, and open-source Speech-to-Text transcriber built with Python, Tkinter, and OpenAI's Whisper model. Designed specifically for Linux (Ubuntu/Kubuntu) environments, this tool converts your audio files (or live mic recordings) into perfectly formatted text.

![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Ubuntu-orange.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)

## ✨ Key Features
- **100% Offline AI:** Powered by OpenAI's Whisper model (runs locally, no API keys, no subscriptions).
- **Live Mic Recording & Timer:** Record directly from your microphone with an active timer.
- **Multilingual Support:** Highly accurate Hindi, Marathi (Devanagari), and English transcription.
- **🔊 Read Aloud (gTTS):** AI reads back your transcribed text, highlighting the paragraph in real-time.
- **Strict Privacy:** Temporary audio files are strictly and permanently deleted immediately after processing.
- **IDE-Like Editor:** Modern Dark Mode UI with uncopiable line numbers and text zoom (A+/A-) controls.

## 🛠️ Installation & Setup (Ubuntu/Kubuntu)

### 1. Install System Dependencies
First, install the required system libraries for audio processing:
```bash
sudo apt update
sudo apt install ffmpeg python3-dev portaudio19-dev python3-tk
```

### 2. Set Up Virtual Environment
It is highly recommended to use a virtual environment:
```bash
python3 -m venv whisper-env
source whisper-env/bin/activate
```

### 3. Install Python Packages
```bash
pip install setuptools-rust
pip install git+https://github.com/openai/whisper.git
pip install pyaudio gTTS
```

## 🚀 Usage
Simply run the python script:
```bash
python3 mp3.py
```
- Click **"🎵 Select Audio File"** to transcribe existing `.mp3`, `.wav`, or `.m4a` files.
- Click **"🎤 Start Recording"** for live dictation.
- Hit **"🔊 Read Aloud"** to verify the output.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](issues-link-here).

## 📄 License
This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.
