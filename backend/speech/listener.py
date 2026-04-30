import speech_recognition as sr

recognizer = sr.Recognizer()

def listen() -> str:
    """Listens to the microphone and returns recognized text."""
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio).lower()
            return text
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return ""

def listen_for_wake_word(wake_word="jarvis") -> bool:
    """Listens for a specific wake word."""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio).lower()
            return wake_word in word
    except:
        return False
