import speech_recognition as sr
import pyttsx3
import webbrowser
import os

# Initialize the recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice commands
def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        return command

# Function to open website
def open_website(name):
    common_websites = {
        'youtube': 'https://www.youtube.com',
        'google': 'https://www.google.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://www.twitter.com',
        'instagram': 'https://www.instagram.com'
    }
    
    url = common_websites.get(name.lower(), f"https://{name.lower()}.com")
    webbrowser.open(url)
    speak(f"Opening {name}")

# Function to open application
def open_application(app_name):
    try:
        if os.name == 'nt':  # Windows
            common_apps = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'file explorer': 'explorer.exe',
                'command prompt': 'cmd.exe'
            }
            app_path = common_apps.get(app_name.lower(), app_name)
            os.startfile(app_path)
        elif os.name == 'posix':  # MacOS and Linux
            os.system(f"open {app_name}")
        speak(f"Opening {app_name}")
    except Exception as e:
        speak(f"Failed to open {app_name}. Error: {str(e)}")

# Function to handle commands
def handle_command(command):
    if 'open website' in command or 'open' in command:
        if 'open website' in command:
            name = command.replace('open website', '').strip()
        else:
            name = command.replace('open', '').strip()
        
        # Try to open it as a website first
        open_website(name)

        # If it's an application, handle it separately
        if 'website' not in command and name not in common_websites:
            open_application(name)
    else:
        speak("Command not recognized. Please try again.")

# Main function
def main():
    speak("How can I assist you?")
    while True:
        command = listen_command()
        if command:
            handle_command(command)
        if 'exit' in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
