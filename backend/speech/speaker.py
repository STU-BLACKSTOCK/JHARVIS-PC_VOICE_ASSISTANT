import os
import pygame
import subprocess
import tempfile
import uuid
import threading
import queue
from backend.speech import state

# Initialize pygame mixer once globally
pygame.mixer.init()

# Background worker queue for totally non-blocking TTS
_tts_queue = queue.Queue()

def _tts_worker():
    while True:
        text = _tts_queue.get()
        if text is None:
            break
            
        temp_filename = f"temp_tts_{uuid.uuid4().hex}.mp3"
        temp_filepath = os.path.join(tempfile.gettempdir(), temp_filename)
        
        try:
            # Generate audio
            subprocess.run(["edge-tts", "--voice", "en-US-AriaNeural", "--text", text, "--write-media", temp_filepath], check=True)
            
            # Play audio
            pygame.mixer.music.load(temp_filepath)
            pygame.mixer.music.play()
            
            # Wait for it to finish
            while pygame.mixer.music.get_busy():
                pygame.time.delay(100)
                
            pygame.mixer.music.unload()
            
            # Cleanup
            try:
                os.remove(temp_filepath)
            except Exception as e:
                print(f"Warning: Could not remove temp audio file: {e}")
                
            print(f"[Jarvis Speaks]: {text}")
        except Exception as e:
            print(f"Edge TTS failed: {e}")
        finally:
            # Only release the lock if there are no more sentences queued to speak
            if _tts_queue.empty():
                state.is_speaking = False
            _tts_queue.task_done()

# Start the background worker daemon immediately
threading.Thread(target=_tts_worker, daemon=True).start()

def speak(text: str):
    """Primary TTS using edge-tts and pygame. Totally non-blocking."""
    # Instantly lock the listener so it doesn't try to hear while we generate/play
    state.is_speaking = True
    _tts_queue.put(text)
