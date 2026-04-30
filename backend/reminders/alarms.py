import threading
import time

def _reminder_thread(minutes: int, message: str, callback):
    time.sleep(minutes * 60)
    callback(f"Reminder: {message}")

def set_reminder(minutes: int, message: str, callback) -> str:
    try:
        threading.Thread(target=_reminder_thread, args=(minutes, message, callback), daemon=True).start()
        return f"Reminder set for {minutes} minutes."
    except Exception as e:
        return f"Could not set reminder: {e}"
