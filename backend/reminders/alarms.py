import threading

def _trigger_reminder(message: str, callback):
    """Executes the reminder callback safely."""
    try:
        callback(f"Reminder: {message}")
    except Exception as e:
        print(f"Error executing reminder callback: {e}")

def set_reminder(minutes: float, message: str, callback) -> str:
    try:
        # Safe validation
        try:
            minutes = float(minutes)
        except ValueError:
            return "Invalid duration. Please provide a valid number."
            
        if minutes <= 0:
            return "Invalid duration. Minutes must be greater than zero."
            
        # Convert to seconds
        delay_seconds = minutes * 60.0
        
        # Use a lightweight Timer instead of manually sleeping a Thread
        timer = threading.Timer(delay_seconds, _trigger_reminder, args=(message, callback))
        timer.daemon = True
        timer.start()
        
        return f"Reminder set for {minutes} minutes."
    except Exception as e:
        print(f"Failed to initialize reminder: {e}")
        return f"Could not set reminder: {e}"
