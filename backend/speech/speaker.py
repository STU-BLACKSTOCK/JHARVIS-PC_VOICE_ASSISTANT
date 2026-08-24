import os
import pygame
import tempfile
import uuid
import threading
import queue
import asyncio
import edge_tts
from backend.speech import state

# Initialize pygame mixer once globally
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Warning: Failed to initialize pygame mixer: {e}")

_tts_queue = queue.Queue()

async def _generate_edge_tts(text: str, output_path: str, voice: str = "en-US-AriaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def _tts_worker():
    while True:
        text = _tts_queue.get()
        if text is None:
            break
            
        if not text or not text.strip():
            _tts_queue.task_done()
            continue

        temp_filename = f"temp_tts_{uuid.uuid4().hex}.mp3"
        temp_filepath = os.path.join(tempfile.gettempdir(), temp_filename)
        
        try:
            # Use direct async edge-tts execution
            asyncio.run(_generate_edge_tts(text, temp_filepath))
            
            # Play audio with pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.load(temp_filepath)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.delay(50)
                    
                pygame.mixer.music.unload()
            
            print(f"[Jarvis Speaks]: {text}")
        except Exception as e:
            print(f"Edge TTS synthesis notice ({e}), trying pyttsx3 fallback...")
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception as fb_err:
                print(f"Offline TTS fallback failed: {fb_err}")
        finally:
            try:
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
            except Exception:
                pass
                
            if _tts_queue.empty():
                state.is_speaking = False
            _tts_queue.task_done()

threading.Thread(target=_tts_worker, daemon=True).start()

def speak(text: str):
    """Non-blocking TTS dispatch."""
    if not text:
        return
    state.is_speaking = True
    _tts_queue.put(text)

