import pyperclip

def copy_to_clipboard(text: str) -> str:
    if not text or not text.strip():
        return "Nothing to copy. The text provided was empty."
    try:
        pyperclip.copy(text)
        return "Copied to clipboard."
    except Exception as e:
        print(f"Clipboard copy error: {e}")
        return f"Failed to copy: {e}"

def read_from_clipboard() -> str:
    try:
        content = pyperclip.paste()
        if not content or not content.strip():
            return "Your clipboard is currently empty."
        return content
    except Exception as e:
        print(f"Clipboard read error: {e}")
        return f"Failed to read clipboard: {e}"
