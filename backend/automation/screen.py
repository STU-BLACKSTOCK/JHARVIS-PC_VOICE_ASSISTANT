import mss
import mss.tools
import cv2
import numpy as np
import os
from datetime import datetime

SCREENSHOT_DIR = "recordings/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot() -> str:
    try:
        with mss.mss() as sct:
            filename = os.path.join(SCREENSHOT_DIR, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            sct.shot(output=filename)
            return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Failed to take screenshot: {e}"

# Future implementation: Screen Recording using OpenCV VideoWriter
def record_screen(duration=5) -> str:
    # Basic stub for screen recording logic
    return "Screen recording functionality initialized but not yet recording."
