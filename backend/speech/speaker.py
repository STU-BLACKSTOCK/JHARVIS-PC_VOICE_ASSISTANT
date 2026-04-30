import os
import pygame
import asyncio

def speak(text: str):
    """Primary TTS using edge-tts and pygame for high-quality voice output."""
    try:
        # Generate the audio file using edge-tts CLI directly
        # Escape double quotes to avoid command injection
        safe_text = text.replace('"', '\\"')
        
        # We use en-US-AriaNeural which is a very natural sounding female AI voice
        os.system(f'edge-tts --voice en-US-AriaNeural --text "{safe_text}" --write-media temp.mp3')
        
        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
            
        pygame.mixer.music.unload()
        try:
            os.remove("temp.mp3")
        except:
            pass # Ignore if file is locked
            
    except Exception as e:
        print(f"Edge TTS failed: {e}")
        print(f"[Jarvis Speaks]: {text}")
