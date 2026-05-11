import speech_recognition as sr
import time
import re
from backend.speech import state

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8 # Optimized for lower latency
recognizer.dynamic_energy_threshold = True

# Global microphone instance to avoid probing audio devices every call
mic = sr.Microphone()
_calibrated = False

def listen() -> str:
    """Listens to the microphone and returns recognized text."""
    global _calibrated
    if state.is_speaking:
        time.sleep(0.5)
        return ""

    try:
        with mic as source:
            if not _calibrated:
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                _calibrated = True
            
            print("Listening...")
            # Reduced phrase_time_limit slightly for faster turnaround
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
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
    global _calibrated
    try:
        with mic as source:
            if not _calibrated:
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                _calibrated = True
                
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio).lower()
            
            # Remove punctuation to improve wake word detection reliability
            normalized_word = re.sub(r'[^\w\s]', '', word)
            return wake_word in normalized_word
    except:
        return False
