import speech_recognition as sr
import pyttsx3
import os
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()
def speak(text):
    print("Jarvis:",text)
    engine.say(text)
    engine.runAndWait()
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        recognizer.energy_threshold = 300
        recognizer.pause_threshold=0.5
        try:
           audio = recognizer.listen(source, timeout=2,phrase_time_limit=4)         
           command = recognizer.recognize_google(audio)
           print("You said:", command)
           return command.lower()
        except sr.WaitTimeoutError:
             return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there seems to be an issue with the service.")
            return ""
#main loop
speak("Hello sir, I am your assistant Jarvis. How can I help you today?")
while True:
    command = listen()
    if not command:
         continue
    if "stop" in command or "exit" in command:
        speak("Goodbye!")
        break
    elif"hey jarvis" in command:
         speak("yes sir, how can I help you")
         command=listen()
    elif "your name" in command:
        speak("My name is Jarvis.")
    elif "whats is the time" in command:
        from datetime import datetime
        speak("The current time is " + datetime.now().strftime("%I:%M %p"))
    elif "open notepad" in command:
         speak("yes sir, Opening Notepad")
         os.system("notepad.exe")
    elif "open chrome" in command:
         speak("yes sir, Opening Chrome")
         os.startfile(r"C:\\Users\\omanl\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
  
    elif "open vs code" in command:
         speak("yes sir, Opening VS Code")
         os.startfile(r"C:\\Users\\omanl\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
    elif"open lead code" in command:
        speak("yes sir,Opening Leetcode")
        webbrowser.open("https://leetcode.com/u/SAAI_PRAKASH/")
    elif "open my github" in command:
         speak("yes sir,opening github")
         webbrowser.open("https://github.com/Saai416")
    elif"open youtube"in command:
         speak("yes sir,opening youtube")
         webbrowser.open("https://www.youtube.com/")
    elif "open my folder" in command:
            speak("yes sir,opening your folder")
            os.startfile("explorer.exe")
    elif"open whatsapp" in command:
           speak("yes sir,opening whatsapp")
           os.startfile(r"C:\\Users\\omanl\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk")
    elif command:
        speak("You said: " + command)


    