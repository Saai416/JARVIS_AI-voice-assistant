"""
JARVIS - Just A Rather Very Intelligent System
Iron Man-style AI Assistant with voice control and futuristic UI

Main entry point - launches JARVIS with global hotkey activation
"""

import customtkinter as ctk
from pynput import keyboard
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from ai_brain import JarvisAI
from ui.jarvis_ui import JarvisUI


class JarvisApp:
    """Main JARVIS application controller"""
    
    def __init__(self):
        """Initialize JARVIS"""
        print("\n" + "="*60)
        print("🤖 J.A.R.V.I.S. - Iron Man AI Assistant")
        print("="*60)
        
        # Validate configuration
        if not Config.validate():
            print("\n❌ Configuration error! Please set up your .env file.")
            print("See .env.example for template.\n")
            input("Press Enter to exit...")
            sys.exit(1)
        
        print("✅ Configuration validated")
        print(f"✅ AI Model: {Config.AI_MODEL}")
        print(f"✅ Hotkey: {Config.ACTIVATION_HOTKEY}")
        print("\n" + "="*60)
        print("JARVIS is ready!")
        print(f"Press {Config.ACTIVATION_HOTKEY} to activate")
        print("Press Ctrl+C to exit")
        print("="*60 + "\n")
        
        # Initialize AI
        try:
            self.ai_brain = JarvisAI()
            print("✅ AI Brain initialized successfully\n")
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Failed to initialize AI: {e}\n")
            
            # Provide helpful guidance based on error type
            if "429" in error_msg or "quota" in error_msg.lower():
                print("💡 SOLUTION: Rate limit or quota exceeded")
                print("   The model config has been updated to use 'gemini-1.5-flash'")
                print("   Please restart JARVIS with: python main.py")
                print("   OR wait a few minutes and try again\n")
            elif "API_KEY" in error_msg or "api key" in error_msg.lower():
                print("💡 SOLUTION: Check your .env file")
                print("   Make sure GEMINI_API_KEY is set correctly\n")
            else:
                print("💡 SOLUTION: Check your internet connection")
                print("   Verify your API key at: https://aistudio.google.com/app/apikey\n")
            
            input("Press Enter to exit...")
            sys.exit(1)
        
        # UI window reference
        self.ui_window = None
        
        # Set up hotkey listener
        self.setup_hotkey()
    
    def setup_hotkey(self):
        """Set up global hotkey listener"""
        
        def on_activate():
            """Called when hotkey is pressed"""
            print("🎯 Hotkey activated! Opening JARVIS...")
            self.show_ui()
        
        # Parse hotkey combination from config
        # Format: "<ctrl>+<space>"
        hotkey = Config.ACTIVATION_HOTKEY
        
        # Set up listener
        with keyboard.GlobalHotKeys({
            hotkey: on_activate
        }) as listener:
            listener.join()
    
    def show_ui(self):
        """Show JARVIS UI window"""
        if self.ui_window is not None:
            try:
                # Window already exists, bring to front
                self.ui_window.lift()
                self.ui_window.focus_force()
                return
            except:
                # Window was closed, create new one
                pass
        
        try:
            # Create new window
            self.ui_window = JarvisUI(self.ai_brain)
            
            # Center window on screen
            self.center_window(self.ui_window)
            
            # Run UI
            self.ui_window.mainloop()
            
            # Window closed
            self.ui_window = None
        
        except Exception as e:
            print(f"Error showing UI: {e}")
            self.ui_window = None
    
    def center_window(self, window):
        """Center window on screen"""
        window.update_idletasks()
        
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - Config.WINDOW_WIDTH) // 2
        y = (screen_height - Config.WINDOW_HEIGHT) // 2
        
        # Set position
        window.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}")


def main():
    """Main entry point"""
    try:
        app = JarvisApp()
    except KeyboardInterrupt:
        print("\n\n👋 JARVIS shutting down...")
        print("Goodbye, sir.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
