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

## 🛠️ Installation & Setup

### 🐧 Linux (Ubuntu/Kubuntu/Debian)

Run these commands in your terminal to install system dependencies and set up the environment:

```bash
# 1. Update and install system dependencies
sudo apt update
sudo apt install ffmpeg python3-dev portaudio19-dev python3-tk python3-venv git -y

# 2. Set up Virtual Environment
python3 -m venv whisper-env
source whisper-env/bin/activate

# 3. Install Python Packages
pip install --upgrade pip
pip install setuptools-rust
pip install git+https://github.com/openai/whisper.git
pip install pyaudio gTTS
```

---

### 🪟 Windows

Follow these steps to get the app running on Windows:

1.  **Install Python:** Download and install **Python 3.10+** from [python.org](https://www.python.org/downloads/). 
    > ⚠️ **Crucial:** Check the box **"Add Python to PATH"** during installation.
2.  **Install Git:** Download and install **Git** from [git-scm.com](https://git-scm.com/).
3.  **Install FFmpeg:**
    -   Download the latest "essentials" build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
    -   Extract the folder (e.g., to `C:\ffmpeg`).
    -   Add the `bin` folder (e.g., `C:\ffmpeg\bin`) to your **System Environment Variables (PATH)**.
4.  **Open Terminal (PowerShell or CMD) and run:**

```powershell
# 1. Set up Virtual Environment
python -m venv whisper-env
whisper-env\Scripts\activate

# 2. Install Python Packages
pip install --upgrade pip
pip install setuptools-rust
pip install git+https://github.com/openai/whisper.git
pip install pyaudio gTTS
```

## 🚀 Usage

Once the installation is complete, you can start the application:

**On Linux:**
```bash
source whisper-env/bin/activate
python3 main.py
```

**On Windows:**
```powershell
whisper-env\Scripts\activate
python main.py
```

- Click **"🎵 Select Audio File"** to transcribe existing `.mp3`, `.wav`, or `.m4a` files.
- Click **"🎤 Start Recording"** for live dictation.
- Hit **"🔊 Read Aloud"** to verify the output.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](issues-link-here).

## 📄 License
This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.
