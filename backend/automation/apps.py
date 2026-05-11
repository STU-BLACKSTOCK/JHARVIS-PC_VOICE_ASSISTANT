import os
import time
import pyautogui

def launch_app(app_name: str) -> str:
    app_paths = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "notepad": "notepad.exe",
        "vs code": r"C:\Users\visha\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }
    path = app_paths.get(app_name.lower())
    if path:
        try:
            os.startfile(path)
            return f"Launching {app_name}"
        except Exception as e:
            return f"Failed to launch {app_name}: {e}"
    else:
        # Fallback to Windows Start Menu search
        try:
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(app_name, interval=0.05)
            time.sleep(0.5)
            pyautogui.press('enter')
            return f"Attempted to open {app_name} via Windows Search."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"
