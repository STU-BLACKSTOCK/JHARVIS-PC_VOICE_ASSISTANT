import threading
import uuid
from datetime import datetime, timedelta

active_reminders = {}

def _trigger_reminder(reminder_id: str, message: str, callback=None):
    """Executes the reminder callback safely."""
    try:
        if reminder_id in active_reminders:
            del active_reminders[reminder_id]
        if callback:
            callback(f"Reminder: {message}")
    except Exception as e:
        print(f"Error executing reminder callback: {e}")

def set_reminder(minutes: float, message: str, callback=None) -> str:
    try:
        try:
            minutes = float(minutes)
        except ValueError:
            return "Invalid duration. Please provide a valid number."
            
        if minutes <= 0:
            return "Invalid duration. Minutes must be greater than zero."
            
        delay_seconds = minutes * 60.0
        reminder_id = str(uuid.uuid4())[:8]
        fire_time = (datetime.now() + timedelta(seconds=delay_seconds)).strftime("%H:%M:%S")
        
        timer = threading.Timer(delay_seconds, _trigger_reminder, args=(reminder_id, message, callback))
        timer.daemon = True
        timer.start()
        
        active_reminders[reminder_id] = {
            "id": reminder_id,
            "message": message,
            "fire_time": fire_time,
            "minutes": minutes,
            "timer": timer
        }
        
        return f"Reminder set for {minutes} minute(s) (at {fire_time}): '{message}'"
    except Exception as e:
        print(f"Failed to initialize reminder: {e}")
        return f"Could not set reminder: {e}"

def list_active_reminders() -> list:
    return [
        {"id": r["id"], "message": r["message"], "fire_time": r["fire_time"], "minutes": r["minutes"]}
        for r in active_reminders.values()
    ]

