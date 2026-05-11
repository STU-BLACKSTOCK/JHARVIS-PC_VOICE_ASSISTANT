import pygetwindow as gw
import time

def get_all_windows():
    return gw.getAllTitles()

def find_window_fuzzy(title_keyword: str):
    keyword = title_keyword.lower()
    # Map common conversational names to actual window titles
    aliases = {
        "vs code": "visual studio code",
        "chrome": "google chrome",
        "edge": "microsoft edge",
        "discord": "discord"
    }
    keyword = aliases.get(keyword, keyword)
    
    for win in gw.getAllWindows():
        if win.title and keyword in win.title.lower():
            return win
    return None

def switch_to_window(title_keyword: str) -> str:
    try:
        win = find_window_fuzzy(title_keyword)
        if win:
            win.restore() # In case it's minimized
            win.activate()
            return f"Switched to {win.title}"
        return f"Failed: No window found matching '{title_keyword}'"
    except Exception as e:
        return f"Failed to switch window: {e}"

def minimize_window(title_keyword: str) -> str:
    try:
        win = find_window_fuzzy(title_keyword)
        if win:
            win.minimize()
            return f"Minimized {win.title}"
        return f"Failed: Window not found matching '{title_keyword}'"
    except Exception as e:
        return f"Failed: {e}"

def maximize_window(title_keyword: str) -> str:
    try:
        win = find_window_fuzzy(title_keyword)
        if win:
            win.maximize()
            return f"Maximized {win.title}"
        return f"Failed: Window not found matching '{title_keyword}'"
    except Exception as e:
        return f"Failed: {e}"

def close_window(title_keyword: str) -> str:
    try:
        win = find_window_fuzzy(title_keyword)
        if win:
            win.close()
            return f"Closed {win.title}"
        return f"Failed: Window not found matching '{title_keyword}'"
    except Exception as e:
        return f"Failed: {e}"
