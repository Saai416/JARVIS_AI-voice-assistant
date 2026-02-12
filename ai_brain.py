"""
JARVIS AI Brain - Multi-Provider Support
Handles intelligent conversations with Google Gemini or local Ollama
"""

import os
import webbrowser
from datetime import datetime
from config import Config

# Try importing AI providers
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False


class JarvisAI:
    """AI-powered brain for JARVIS with multi-provider support"""
    
    def __init__(self):
        """Initialize AI based on configured provider"""
        self.provider = Config.AI_PROVIDER
        self.conversation_history = []
        
        # System prompt for JARVIS personality
        self.system_prompt = """You are JARVIS, an advanced AI assistant inspired by Iron Man's AI companion.

Personality traits:
- Professional, helpful, and efficient
- Concise responses (2-3 sentences max unless asked for details)
- Slightly formal but friendly
- Use phrases like "Certainly, sir" or "Right away" when appropriate
- Never use emojis in responses

Capabilities:
- Answer questions with intelligence and context
- Execute system commands (open apps, websites)
- Provide time, date, and information
- Maintain conversation context

When the user asks to open something or execute a command, acknowledge it briefly and confirm the action."""
        
        # Initialize the selected provider
        if self.provider == "ollama":
            self._init_ollama()
        elif self.provider == "gemini":
            self._init_gemini()
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
    
    def _init_ollama(self):
        """Initialize Ollama local AI"""
        if not OLLAMA_AVAILABLE:
            raise ImportError("Ollama package not installed. Run: pip install ollama")
        
        self.model = Config.OLLAMA_MODEL
        print(f"✅ Using Ollama with model: {self.model}")
        
        # Test connection
        try:
            ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                options={"num_predict": 10}
            )
        except Exception as e:
            print(f"\n⚠️  Warning: Could not connect to Ollama")
            print(f"Make sure Ollama is running: ollama serve")
            print(f"And model is pulled: ollama pull {self.model}\n")
            raise
    
    def _init_gemini(self):
        """Initialize Google Gemini"""
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed")
        
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        self.model = genai.GenerativeModel(
            model_name=Config.AI_MODEL,
            generation_config={
                "temperature": Config.AI_TEMPERATURE,
                "max_output_tokens": Config.AI_MAX_TOKENS,
            }
        )
        
        self.chat = self.model.start_chat(history=[])
        self.chat.send_message(self.system_prompt)
        print(f"✅ Using Google Gemini: {Config.AI_MODEL}")
    
    def process_command(self, user_input):
        """
        Process user input - detect if it's a system command or conversation
        
        Returns:
            tuple: (response_text, command_executed)
        """
        user_input_lower = user_input.lower().strip()
        
        # Check for system commands first
        command_executed = self._execute_system_command(user_input_lower)
        
        # Get AI response
        try:
            if command_executed:
                # Command was executed, get brief confirmation from AI
                prompt = f"User said: '{user_input}'. I've executed the command. Give a brief 1-sentence confirmation."
                response = self._get_ai_response(prompt)
                return response, True
            else:
                # Regular conversation
                response = self._get_ai_response(user_input)
                return response, False
        except Exception as e:
            print(f"AI response error: {e}")
            return f"I apologize, sir. I encountered an error: {str(e)}", False
    
    def _get_ai_response(self, prompt):
        """Get response from configured AI provider"""
        if self.provider == "ollama":
            return self._get_ollama_response(prompt)
        elif self.provider == "gemini":
            return self._get_gemini_response(prompt)
    
    def _get_ollama_response(self, prompt):
        """Get response from Ollama"""
        # Build messages with history
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        for msg in self.conversation_history[-Config.CONVERSATION_HISTORY_LIMIT:]:
            messages.append(msg)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Get response
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": Config.AI_TEMPERATURE,
                "num_predict": Config.AI_MAX_TOKENS
            }
        )
        
        response_text = response['message']['content']
        
        # Update history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def _get_gemini_response(self, prompt):
        """Get response from Gemini"""
        response = self.chat.send_message(prompt)
        return response.text
    
    def _execute_system_command(self, command):
        """
        Execute system commands based on user input
        
        Returns:
            bool: True if command was executed, False otherwise
        """
        try:
            # Open Chrome
            if ("open chrome" in command or "launch chrome" in command) and "chrome" in command:
                os.system(Config.COMMANDS["chrome"])
                return True
            
            # Open Notepad
            if ("open notepad" in command or "launch notepad" in command):
                os.system(Config.COMMANDS["notepad"])
                return True
            
            # Open YouTube
            if ("open youtube" in command or "youtube" in command) and "open" in command:
                webbrowser.open(Config.COMMANDS["youtube"])
                return True
            
            # Open GitHub
            if ("open github" in command or "github" in command) and "open" in command:
                webbrowser.open(Config.COMMANDS["github"])
                return True
            
            # Open LeetCode
            if ("open leetcode" in command or "leetcode" in command) and "open" in command:
                webbrowser.open(Config.COMMANDS["leetcode"])
                return True
            
            return False
        
        except Exception as e:
            print(f"Command execution error: {e}")
            return False
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        if self.provider == "gemini":
            self.chat = self.model.start_chat(history=[])
            self.chat.send_message(self.system_prompt)
    
    def get_greeting(self):
        """Get AI greeting message"""
        try:
            response = self._get_ai_response("Greet the user as JARVIS when the system starts. Keep it to 1 sentence.")
            return response
        except:
            return "Good day, sir. JARVIS is online and ready to assist."
