"""
JARVIS Configuration Management
Handles API keys, UI settings, and application configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for JARVIS"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # UI Settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_ALPHA = 0.95  # Transparency (0.0 to 1.0)
    
    # Colors (Iron Man theme - Cyan/Blue)
    COLOR_PRIMARY = "#00d4ff"  # Bright cyan
    COLOR_SECONDARY = "#7b2ff7"  # Purple accent
    COLOR_BACKGROUND = "#0a0e27"  # Dark navy
    COLOR_PANEL = "#1a1e3a"  # Slightly lighter panel
    COLOR_TEXT = "#ffffff"  # White text
    COLOR_GLOW = "#00ffff"  # Cyan glow
    
    # Arc Reactor Animation
    ARC_REACTOR_SIZE = 200
    ARC_REACTOR_RINGS = 3
    PULSE_SPEED = 2.0  # seconds per pulse
    
    # Voice Settings
    VOICE_TIMEOUT = 5  # seconds
    VOICE_PHRASE_LIMIT = 10  # seconds
    TTS_RATE = 175  # speaking rate (words per minute)
    TTS_VOICE_INDEX = 0  # 0 for default, 1 for female (if available)
    
    # Hotkey Configuration
    ACTIVATION_HOTKEY = "<ctrl>+<space>"
    CLOSE_HOTKEY = "escape"
    
    # AI Settings
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")  # "gemini" or "ollama"
    
    # Gemini Settings
    AI_MODEL = "gemini-1.5-flash"  # Stable free-tier model
    
    # Ollama Settings (local AI)
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  # or "mistral", "phi", etc.
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # General AI Settings
    AI_TEMPERATURE = 0.7
    AI_MAX_TOKENS = 1024
    CONVERSATION_HISTORY_LIMIT = 10
    
    # System Commands
    COMMANDS = {
        "chrome": "start chrome",
        "notepad": "notepad.exe",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com/Saai416",
        "leetcode": "https://leetcode.com/u/SAAI_PRAKASH/",
    }
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        # API key only required for Gemini
        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            print("\n⚠️  WARNING: GEMINI_API_KEY not found!")
            print("Please create a .env file with:")
            print("GEMINI_API_KEY=your_api_key_here")
            print("\nGet your free API key: https://aistudio.google.com/app/apikey\n")
            return False
        return True
    
    @classmethod
    def get_project_root(cls):
        """Get project root directory"""
        return Path(__file__).parent
