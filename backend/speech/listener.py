import speech_recognition as sr
import time
import re
import threading
from backend.speech import state

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 300
recognizer.non_speaking_duration = 0.4

_mic_lock = threading.Lock()
_has_calibrated = False

def _safe_calibrate(source):
    global _has_calibrated
    if not _has_calibrated:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            _has_calibrated = True
        except Exception:
            pass

def listen(phrase_time_limit: int = 7) -> str:
    """Safely listens to the microphone with proper context manager lifecycle."""
    if state.is_speaking:
        time.sleep(0.3)
        return ""

    # Acquire lock with non-blocking timeout to prevent audio device contention
    acquired = _mic_lock.acquire(timeout=0.5)
    if not acquired:
        return ""

    try:
        # Create fresh Microphone instance to ensure clean PyAudio stream lifecycle
        with sr.Microphone() as source:
            _safe_calibrate(source)
            
            # Listen with short timeout
            audio = recognizer.listen(source, timeout=3.5, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio).strip()
            return text
    except (sr.WaitTimeoutError, sr.UnknownValueError):
        return ""
    except Exception as e:
        # Suppress benign audio stream device warnings
        return ""
    finally:
        _mic_lock.release()

def listen_for_wake_word(wake_word: str = "jarvis") -> tuple[bool, str]:
    """
    Listens for speech and checks if the wake word is present.
    Returns (True, command_after_wake_word) if detected, else (False, "").
    """
    text = listen(phrase_time_limit=8)
    if not text:
        return False, ""
    
    text_lower = text.lower()
    clean_text = re.sub(r'[^\w\s]', '', text_lower)
    
    if wake_word in clean_text:
        parts = text_lower.split(wake_word, 1)
        command = parts[1].strip() if len(parts) > 1 else ""
        return True, command or text
    
    return False, ""


