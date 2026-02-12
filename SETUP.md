# 🤖 JARVIS Setup Guide

Quick setup instructions for your Iron Man-style AI assistant.

## Prerequisites

- Python 3.8 or higher
- Windows OS (for voice features)
- Microphone for voice input

## Setup Steps

### 1. Get Google Gemini API Key

1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
```

### 3. Install Dependencies

Open terminal in project directory and run:

```bash
# Activate virtual environment
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note**: If `pyaudio` installation fails, download the wheel file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### 4. Run JARVIS

```bash
python main.py
```

## Usage

- **Activate JARVIS**: Press `Ctrl + Space`
- **Voice Input**: Click "LISTEN" button or press `Space`
- **Close Window**: Press `Escape`
- **Exit Application**: Press `Ctrl + C` in terminal

## Features

✅ AI-powered conversations with Google Gemini
✅ Voice recognition and text-to-speech
✅ Iron Man-style UI with arc reactor animation
✅ Animated waveform visualization
✅ Global hotkey activation
✅ System command execution (open apps, websites)

## Voice Commands Examples

- "What time is it?"
- "Open YouTube"
- "Open Chrome"
- "What's the weather like?"
- "Tell me about quantum computing"

## Troubleshooting

**API Key Error**: Make sure `.env` file exists and contains valid API key

**Voice Not Working**: Check microphone permissions and ensure PyAudio is installed

**Hotkey Not Working**: Run as administrator or change hotkey in `config.py`

---

Enjoy your JARVIS AI assistant! 🚀
