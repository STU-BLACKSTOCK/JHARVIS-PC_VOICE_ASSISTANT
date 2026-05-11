import pyautogui
from pynput import keyboard
import time
import threading

# Configure PyAutoGUI for human-like interaction and safety
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True # Moving mouse to a corner aborts

class AutomationController:
    def __init__(self):
        self._stop_event = threading.Event()
        self._hotkey_listener = None
        self._start_emergency_listener()

    def _start_emergency_listener(self):
        """Starts a background listener for the emergency stop hotkey (Ctrl+Shift+Esc)."""
        def on_activate():
            print("\n[!] EMERGENCY STOP ACTIVATED. Aborting automation...")
            self.stop()
            
        # Register the hotkey
        self._hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+<esc>': on_activate
        })
        self._hotkey_listener.start()

    def stop(self):
        self._stop_event.set()

    def reset(self):
        self._stop_event.clear()

    def check_stop(self):
        if self._stop_event.is_set():
            raise Exception("Automation aborted by user.")

    def type_text(self, text: str, interval=0.05):
        self.check_stop()
        pyautogui.write(text, interval=interval)

    def press_key(self, key: str):
        self.check_stop()
        pyautogui.press(key)

    def hotkey(self, *keys):
        self.check_stop()
        pyautogui.hotkey(*keys)

    def click(self, x=None, y=None, button='left', clicks=1):
        self.check_stop()
        pyautogui.click(x=x, y=y, button=button, clicks=clicks)

    def move_to(self, x, y, duration=0.5):
        self.check_stop()
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)

    def scroll(self, amount: int):
        self.check_stop()
        pyautogui.scroll(amount)

# Global instance
controller = AutomationController()
