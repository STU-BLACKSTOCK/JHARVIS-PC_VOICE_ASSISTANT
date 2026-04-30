import pyperclip

def copy_to_clipboard(text: str) -> str:
    try:
        pyperclip.copy(text)
        return "Copied to clipboard."
    except Exception as e:
        return f"Failed to copy: {e}"

def read_from_clipboard() -> str:
    try:
        return pyperclip.paste()
    except Exception as e:
        return f"Failed to read clipboard: {e}"
