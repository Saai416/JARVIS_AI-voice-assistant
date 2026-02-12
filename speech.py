from flask import Flask, request, jsonify, render_template
import os
import webbrowser
from datetime import datetime

# Optional: Speech recognition (works only if installed)
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_ENABLED = True
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
except:
    VOICE_ENABLED = False
    print("Voice features disabled - speech libraries not installed")

app = Flask(__name__)

def speak(text):
    """Text-to-speech (if available)"""
    if VOICE_ENABLED:
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

def execute_command(command):
    """Process command and return response"""
    command = command.lower().strip()
    
    if "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    elif "date" in command:
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}"
    
    elif "open chrome" in command or "chrome" in command:
        try:
            os.system("start chrome")
            return "Opening Google Chrome"
        except:
            return "Could not open Chrome"
    
    elif "open youtube" in command or "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"
    
    elif "open github" in command or "github" in command:
        webbrowser.open("https://github.com/Saai416")
        return "Opening your GitHub profile"
    
    elif "open leetcode" in command or "leetcode" in command:
        webbrowser.open("https://leetcode.com/u/SAAI_PRAKASH/")
        return "Opening LeetCode profile"
    
    elif "open notepad" in command or "notepad" in command:
        try:
            os.system("notepad.exe")
            return "Opening Notepad"
        except:
            return "Could not open Notepad"
    
    elif "hello" in command or "hi" in command or "hey" in command:
        return "Hello! I am Jarvis, your AI assistant. How can I help you?"
    
    elif "your name" in command or "who are you" in command:
        return "I am Jarvis, your personal AI assistant created by Sai Prakash"
    
    elif "help" in command:
        return """I can help you with:
- Tell time and date
- Open applications (Chrome, Notepad, VS Code)
- Open websites (YouTube, GitHub, LeetCode)
- System commands"""
    
    else:
        return f"I received your command: '{command}'. I'm still learning this one!"

# Routes

@app.route('/')
def home():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def api_command():
    """Execute text command via API"""
    try:
        data = request.json
        command = data.get('command', '')
        
        if not command:
            return jsonify({
                "status": "error",
                "message": "No command provided"
            }), 400
        
        response = execute_command(command)
        speak(response)
        
        return jsonify({
            "status": "success",
            "command": command,
            "response": response
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/voice', methods=['GET'])
def api_voice():
    """Listen for voice command"""
    if not VOICE_ENABLED:
        return jsonify({
            "status": "error",
            "message": "Voice features not available"
        }), 400
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            response = execute_command(command)
            
            return jsonify({
                "status": "success",
                "command": command,
                "response": response
            })
    except sr.WaitTimeoutError:
        return jsonify({
            "status": "error",
            "message": "No speech detected"
        }), 400
    except sr.UnknownValueError:
        return jsonify({
            "status": "error",
            "message": "Could not understand audio"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check server status"""
    return jsonify({
        "status": "online",
        "name": "Jarvis",
        "version": "2.0",
        "voice_enabled": VOICE_ENABLED
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🤖 JARVIS AI Assistant - Flask Server")
    print("="*50)
    print(f"✅ Server running at: http://localhost:5000")
    print(f"✅ Voice features: {'Enabled' if VOICE_ENABLED else 'Disabled'}")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
