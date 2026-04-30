import os

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
        return "App path not found. Please update the app list."
