import time
import pyautogui
from backend.automation.mouse_keyboard import controller
from backend.automation.windows import get_all_windows, minimize_window, maximize_window, close_window, switch_to_window
from backend.automation.screen import take_screenshot
from backend.automation.browser import browser_controller
from backend.automation.apps import launch_app

def execute_step(step: dict, broadcast_callback=None):
    """Executes a single planned automation step."""
    action = step.get("action")
    
    try:
        controller.check_stop()
        if broadcast_callback:
            broadcast_callback({"type": "automation_step", "message": f"Executing: {action}"})
            
        if action == "open_app":
            return launch_app(step.get("target"))
        elif action == "type_text":
            controller.type_text(step.get("text"))
            return "Text typed."
        elif action == "press_key":
            controller.press_key(step.get("key"))
            return f"Pressed {step.get('key')}."
        elif action == "hotkey":
            controller.hotkey(*step.get("keys"))
            return "Hotkey executed."
        elif action == "navigate_browser":
            return browser_controller.navigate(step.get("url"))
        elif action == "search_google":
            return browser_controller.search_google(step.get("query"))
        elif action == "take_screenshot":
            return take_screenshot()
        elif action == "minimize_window":
            return minimize_window(step.get("title"))
        elif action == "maximize_window":
            return maximize_window(step.get("title"))
        elif action == "close_window":
            return close_window(step.get("title"))
        elif action == "switch_window":
            return switch_to_window(step.get("title"))
        else:
            return f"Unknown action: {action}"
    except pyautogui.FailSafeException:
        raise Exception("Automation aborted by user (FailSafe triggered).")
    except Exception as e:
        # Check if it's our manual abort exception
        if "aborted" in str(e).lower():
            raise e
        return f"Error executing {action}: {str(e)}"

def run_workflow(steps: list, broadcast_callback=None):
    """Executes an array of steps sequentially."""
    results = []
    for step in steps:
        time.sleep(1) # Human delay
        try:
            controller.check_stop()
            res = execute_step(step, broadcast_callback)
            results.append(res)
        except Exception as e:
            if "abort" in str(e).lower():
                if broadcast_callback: broadcast_callback({"type": "automation_step", "message": "🚨 AUTOMATION ABORTED."})
                results.append("ABORTED")
                break
            
    return results
