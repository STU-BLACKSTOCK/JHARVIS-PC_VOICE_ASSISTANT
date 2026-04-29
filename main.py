import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import glob
import time
import threading
from dotenv import load_dotenv
from datetime import datetime

# Load .env for GitHub Token
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
newsapi = "pub_77770e046950e250e95802b553dc994af9e86"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=token)
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis."},
            {"role": "user", "content": command}
        ],
        model="gpt-4o"
    )
    return completion.choices[0].message.content

def get_weather():
    api_key = "your_weatherapi_key"  # Optional: if using a weather API
    return "Weather API not integrated. Replace with your own."

def get_motivational_quote():
    try:
        r = requests.get("https://zenquotes.io/api/random")
        return r.json()[0]["q"]
    except:
        return "Stay positive and keep pushing forward."

def daily_summary():
    now = datetime.now()
    date = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")
    speak(f"Good day! It's {date} and the time is {time_str}.")

    speak("Here's the top news.")
    headers = {'Authorization': f'Bearer {newsapi}'}
    r = requests.get("https://newsapi.org/v2/top-headlines?country=in", headers=headers)
    if r.status_code == 200:
        data = r.json()
        for article in data.get('articles', [])[:3]:
            speak(article['title'])
    else:
        speak("Could not fetch the news.")

    quote = get_motivational_quote()
    speak("And here's your motivational quote:")
    speak(quote)

def define_word(word):
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        data = res.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        speak(f"The definition of {word} is: {definition}")
    except:
        speak("Sorry, I couldn't find the definition.")

def launch_app(app_name):
    app_paths = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "notepad": "notepad.exe",
        "vs code": r"C:\Users\YOUR_USER\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }
    path = app_paths.get(app_name.lower())
    if path:
        os.startfile(path)
        speak(f"Launching {app_name}")
    else:
        speak("App path not found. Please update the app list.")

def search_file(keyword, directory="C:/Users"):
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if keyword.lower() in file.lower():
                matches.append(os.path.join(root, file))
    if matches:
        speak(f"I found {len(matches)} files. Here's one:")
        speak(matches[0])
    else:
        speak("No files found with that name.")

def set_reminder(minutes, message):
    def reminder():
        time.sleep(minutes * 60)
        speak(f"Reminder: {message}")
    threading.Thread(target=reminder).start()
    speak(f"Reminder set for {minutes} minutes.")

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play "):
        song = c.split("play ", 1)[1]
        speak(f"Searching for {song}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    elif "news" in c:
        daily_summary()
    elif "daily update" in c or "daily summary" in c:
        daily_summary()
    elif "define" in c:
        word = c.split("define ", 1)[-1]
        define_word(word)
    elif "launch" in c:
        app = c.split("launch ", 1)[-1]
        launch_app(app)
    elif "find file" in c or "search file" in c:
        keyword = c.split("file", 1)[-1].strip()
        search_file(keyword)
    elif "remind me in" in c:
        try:
            parts = c.split("remind me in ")[1]
            number, message = parts.split(" minutes to ")
            set_reminder(int(number.strip()), message.strip())
        except:
            speak("Sorry, I couldn't set the reminder. Please try again.")
    elif "stop" in c or "exit" in c:
        speak("Goodbye!")
        exit()
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio).lower()
                print(f"Detected: {word}")

                if word == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        print(f"Command received: {command}")
                        processCommand(command)
        except sr.WaitTimeoutError:
            print("Timeout, waiting for trigger word again...")
        except sr.UnknownValueError:
            print("Sorry, couldn't understand that.")
        except Exception as e:
            print(f"Error: {e}")
