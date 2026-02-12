# 🤖 J.A.R.V.I.S. - Iron Man AI Assistant

**Just A Rather Very Intelligent System**

An AI-powered voice assistant with a stunning Iron Man-inspired interface, featuring Google Gemini AI for natural conversations.

![JARVIS UI](https://img.shields.io/badge/Status-Online-00d4ff?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![AI](https://img.shields.io/badge/AI-Google_Gemini-7b2ff7?style=for-the-badge)

## ✨ Features

- 🎯 **AI-Powered Conversations** - Natural language understanding with Google Gemini
- 🎤 **Voice Control** - Speech recognition and text-to-speech
- 💎 **Iron Man UI** - Futuristic popup interface with animated arc reactor
- 📊 **Visual Feedback** - Real-time waveform visualization
- ⌨️ **Global Hotkey** - Activate with `Ctrl+Space` from anywhere
- 🌐 **System Integration** - Open apps and websites with voice commands
- ⚡ **Fast & Responsive** - Smooth animations and instant reactions

## 🎥 Demo

The UI features:
- **Arc Reactor** centerpiece with pulsing glow animation
- **Waveform visualization** during voice input/output
- **Glassmorphic panels** with Iron Man color scheme (cyan/blue)
- **Conversation log** with scrollable history
- **Status indicators** for system state

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows OS
- Microphone
- Google Gemini API key (free)

### Installation

1. **Clone or download this project**

2. **Get API Key**
   ```
   Visit: https://aistudio.google.com/app/apikey
   Create a free API key
   ```

3. **Configure Environment**
   ```bash
   # Create .env file
   copy .env.example .env
   
   # Edit .env and add your API key
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Install Dependencies**
   ```bash
   # Activate virtual environment
   myenv\Scripts\activate
   
   # Install packages
   pip install -r requirements.txt
   ```

5. **Run JARVIS**
   ```bash
   python main.py
   ```

## 🎮 Usage

### Activation
- Press `Ctrl+Space` to open JARVIS window

### Voice Commands
- Click **"LISTEN"** button or press `Space`
- Speak your command clearly
- Wait for JARVIS response

### Example Commands
```
"What time is it?"
"Open YouTube"
"Open Chrome"
"Tell me about artificial intelligence"
"What's the weather in New York?"
"Open my GitHub"
```

### Keyboard Shortcuts
- `Ctrl+Space` - Activate JARVIS
- `Space` - Start listening (when window is open)
- `Escape` - Close window
- `Ctrl+C` - Exit application (in terminal)

## 🏗️ Project Structure

```
JARVIS ai assistant/
├── main.py              # Entry point with hotkey listener
├── config.py            # Configuration settings
├── ai_brain.py          # Google Gemini AI integration
├── ui/
│   ├── jarvis_ui.py     # Main popup window
│   ├── widgets.py       # Custom UI components
│   └── animations.py    # Animation engine
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── SETUP.md            # Detailed setup guide
└── README.md           # This file
```

## 🎨 Customization

Edit `config.py` to customize:

- **Colors**: Change the Iron Man theme colors
- **Hotkey**: Modify activation hotkey
- **Voice**: Adjust speech rate and timeout
- **AI**: Configure model and parameters
- **Commands**: Add custom system commands

## 🔧 Troubleshooting

### API Key Error
- Ensure `.env` file exists in project root
- Verify API key is correct and active

### Voice Not Working
- Check microphone permissions
- Install PyAudio: `pip install pyaudio`
- If PyAudio fails, get wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### Hotkey Not Responding
- Run terminal as administrator
- Change hotkey in `config.py`

### Import Errors
- Activate virtual environment: `myenv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## 📦 Dependencies

- **google-generativeai** - AI brain
- **customtkinter** - Modern UI framework
- **SpeechRecognition** - Voice input
- **pyttsx3** - Text-to-speech
- **pynput** - Global hotkey listener
- **python-dotenv** - Environment configuration

## 🤝 Contributing

Feel free to fork, modify, and enhance JARVIS! Ideas:
- Add more voice commands
- Integrate with smart home devices
- Add web search capabilities
- Create mobile companion app

## 📝 License

This project is open source and available for personal use.

## 🙏 Acknowledgments

- Inspired by Iron Man's JARVIS
- Powered by Google Gemini AI
- Built with ❤️ for AI enthusiasts

---

**Made by Sai Prakash** | [GitHub](https://github.com/Saai416)

*"Sometimes you gotta run before you can walk."* - Tony Stark
