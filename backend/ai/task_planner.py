import json
from backend.ai.groq_client import client, GROQ_API_KEY

def plan_task(natural_language_command: str) -> list:
    """Uses Groq to break down a command into an array of executable automation steps."""
    if not client:
        return []

    prompt = f"""
    You are the brain of a desktop automation agent.
    Convert the user's natural language command into a JSON array of actionable steps.
    Available actions:
    - {{"action": "open_app", "target": "<app_name_or_path>"}}
    - {{"action": "type_text", "text": "<text>"}}
    - {{"action": "press_key", "key": "<key_name>"}}
    - {{"action": "hotkey", "keys": ["<key1>", "<key2>"]}}
    - {{"action": "navigate_browser", "url": "<url>"}}
    - {{"action": "search_google", "query": "<query>"}}
    - {{"action": "take_screenshot"}}
    - {{"action": "minimize_window", "title": "<window_title>"}}
    - {{"action": "maximize_window", "title": "<window_title>"}}
    - {{"action": "close_window", "title": "<window_title>"}}
    - {{"action": "switch_window", "title": "<window_title>"}}
    
    IMPORTANT RULES:
    1. If asked to search Google, ALWAYS use the `search_google` action. Do not use navigate_browser + type_text.
    2. If asked to open the "project folder", "workspace", or "files", use the `open_app` action with the target set exactly to "C:\\project\\Jharvis BOT".
    
    User Command: "{natural_language_command}"
    
    You MUST output a valid JSON object with a single key "steps" containing the array of actions.
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        response_text = completion.choices[0].message.content.strip()
        data = json.loads(response_text)
        return data.get("steps", [])
    except Exception as e:
        print(f"Task planning failed: {e}")
        return []
