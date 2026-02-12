"""
JARVIS Main UI Window
Iron Man-style popup interface with arc reactor and voice controls
"""

import customtkinter as ctk
from tkinter import END
import threading
import speech_recognition as sr
import pyttsx3
from ui.widgets import (
    ArcReactorWidget, 
    WaveformWidget, 
    StatusLabel, 
    ConversationText,
    GlassPanel
)
from config import Config
from ai_brain import JarvisAI


class JarvisUI(ctk.CTk):
    """Main JARVIS popup window"""
    
    def __init__(self, ai_brain):
        super().__init__()
        
        self.ai_brain = ai_brain
        
        # Window configuration
        self.title("JARVIS")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.attributes("-alpha", Config.WINDOW_ALPHA)
        
        # Make window stay on top
        self.attributes("-topmost", True)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure background
        self.configure(fg_color=Config.COLOR_BACKGROUND)
        
        # Voice components
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', Config.TTS_RATE)
        
        # State
        self.is_listening = False
        self.is_speaking = False
        
        # Build UI
        self._build_ui()
        
        # Bind escape key to close
        self.bind("<Escape>", lambda e: self.close_window())
        
        # Greeting
        self._show_greeting()
    
    def _build_ui(self):
        """Build the user interface"""
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=Config.COLOR_BACKGROUND)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🤖 J.A.R.V.I.S.",
            font=("Segoe UI", 32, "bold"),
            text_color=Config.COLOR_PRIMARY
        )
        title.pack(pady=(10, 20))
        
        # Arc Reactor (center piece)
        self.arc_reactor = ArcReactorWidget(main_frame, size=Config.ARC_REACTOR_SIZE)
        self.arc_reactor.pack(pady=20)
        
        # Status label
        self.status_label = StatusLabel(main_frame, text="SYSTEM ONLINE")
        self.status_label.pack(pady=10)
        
        # Waveform visualization
        self.waveform = WaveformWidget(main_frame, width=500, height=60, num_bars=40)
        self.waveform.pack(pady=15)
        
        # Control buttons frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        # Listen button
        self.listen_btn = ctk.CTkButton(
            button_frame,
            text="🎤 LISTEN",
            command=self.start_listening,
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color=Config.COLOR_PRIMARY,
            hover_color=Config.COLOR_SECONDARY
        )
        self.listen_btn.pack(side="left", padx=10)
        
        # Stop button
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹ STOP",
            command=self.stop_speaking,
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="#ff4444",
            hover_color="#cc0000",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10)
        
        # Conversation panel
        conv_panel = GlassPanel(main_frame)
        conv_panel.pack(fill="both", expand=True, pady=10)
        
        conv_label = ctk.CTkLabel(
            conv_panel,
            text="CONVERSATION LOG",
            font=("Segoe UI", 12, "bold"),
            text_color=Config.COLOR_PRIMARY
        )
        conv_label.pack(pady=5)
        
        self.conversation = ConversationText(conv_panel, height=150)
        self.conversation.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Instructions
        instructions = ctk.CTkLabel(
            main_frame,
            text="Press SPACE to listen • ESC to close",
            font=("Segoe UI", 10),
            text_color="#888888"
        )
        instructions.pack(pady=5)
        
        # Bind spacebar for quick activation
        self.bind("<space>", lambda e: self.start_listening())
    
    def _show_greeting(self):
        """Show initial greeting"""
        threading.Thread(target=self._greeting_thread, daemon=True).start()
    
    def _greeting_thread(self):
        """Get and display AI greeting"""
        try:
            greeting = self.ai_brain.get_greeting()
            self.conversation.add_message("JARVIS", greeting)
            self.speak(greeting)
        except Exception as e:
            print(f"Greeting error: {e}")
            # Use fallback greeting if AI fails
            fallback = "Good day, sir. JARVIS systems online and ready to assist."
            self.conversation.add_message("JARVIS", fallback)
            self.speak(fallback)
    
    def start_listening(self):
        """Start voice recognition"""
        if self.is_listening or self.is_speaking:
            return
        
        self.is_listening = True
        self.listen_btn.configure(state="disabled")
        self.status_label.set_status("🎤 LISTENING...", Config.COLOR_GLOW)
        self.arc_reactor.set_active(True)
        self.waveform.set_active(True)
        
        # Run in thread to avoid blocking UI
        threading.Thread(target=self._listen_thread, daemon=True).start()
    
    def _listen_thread(self):
        """Voice recognition thread"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=Config.VOICE_TIMEOUT,
                    phrase_time_limit=Config.VOICE_PHRASE_LIMIT
                )
                
                # Update status
                self.status_label.set_status("⚙️ PROCESSING...", "#ffaa00")
                
                # Recognize speech
                command = self.recognizer.recognize_google(audio)
                
                # Display user command
                self.conversation.add_message("YOU", command)
                
                # Process with AI
                self._process_command(command)
        
        except sr.WaitTimeoutError:
            self.status_label.set_status("⚠️ NO SPEECH DETECTED", "#ff4444")
            self.conversation.add_message("SYSTEM", "No speech detected. Please try again.")
        
        except sr.UnknownValueError:
            self.status_label.set_status("⚠️ COULD NOT UNDERSTAND", "#ff4444")
            self.conversation.add_message("SYSTEM", "Could not understand audio. Please speak clearly.")
        
        except Exception as e:
            self.status_label.set_status("❌ ERROR", "#ff0000")
            self.conversation.add_message("SYSTEM", f"Error: {str(e)}")
        
        finally:
            self.is_listening = False
            self.listen_btn.configure(state="normal")
            self.arc_reactor.set_active(False)
            self.waveform.set_active(False)
            
            if not self.is_speaking:
                self.status_label.set_status("SYSTEM ONLINE", Config.COLOR_PRIMARY)
    
    def _process_command(self, command):
        """Process command with AI brain"""
        try:
            # Get AI response
            response, command_executed = self.ai_brain.process_command(command)
            
            # Display response
            self.conversation.add_message("JARVIS", response)
            
            # Speak response
            self.speak(response)
        
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.conversation.add_message("SYSTEM", error_msg)
            print(error_msg)
    
    def speak(self, text):
        """Speak text using TTS"""
        if self.is_speaking:
            return
        
        self.is_speaking = True
        self.stop_btn.configure(state="normal")
        
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
    
    def _speak_thread(self, text):
        """TTS thread"""
        try:
            self.status_label.set_status("🔊 SPEAKING...", Config.COLOR_SECONDARY)
            self.waveform.set_active(True)
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        except Exception as e:
            print(f"TTS error: {e}")
        
        finally:
            self.is_speaking = False
            self.stop_btn.configure(state="disabled")
            self.waveform.set_active(False)
            self.status_label.set_status("SYSTEM ONLINE", Config.COLOR_PRIMARY)
    
    def stop_speaking(self):
        """Stop TTS"""
        try:
            self.tts_engine.stop()
        except:
            pass
    
    def close_window(self):
        """Close the JARVIS window"""
        self.stop_speaking()
        self.destroy()
