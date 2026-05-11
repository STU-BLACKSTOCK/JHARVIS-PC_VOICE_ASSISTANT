from backend.database.db_client import get_db

db = get_db()

def add_note(note_content: str) -> str:
    if not note_content or not note_content.strip():
        return "Cannot save an empty note."
    if not db: return "Database is not connected. Can't save note."
    try:
        data = db.table("notes").insert({"content": note_content}).execute()
        return "Note saved successfully."
    except Exception as e:
        return f"Failed to save note: {e}"

def get_notes() -> list:
    if not db: return ["Database not connected."]
    try:
        response = db.table("notes").select("*").order('created_at', desc=True).limit(5).execute()
        return [item['content'] for item in response.data]
    except Exception as e:
        print(f"Failed to get notes: {e}")
        return []

def add_task(task_content: str) -> str:
    if not task_content or not task_content.strip():
        return "Cannot save an empty task."
    if not db: return "Database is not connected. Can't save task."
    try:
        data = db.table("tasks").insert({"content": task_content, "status": "pending"}).execute()
        return f"Task '{task_content}' added to your list."
    except Exception as e:
        return f"Failed to save task: {e}"

def get_tasks() -> list:
    if not db: return ["Database not connected."]
    try:
        response = db.table("tasks").select("*").eq('status', 'pending').execute()
        return [item['content'] for item in response.data]
    except Exception as e:
        print(f"Failed to get tasks: {e}")
        return []

def log_conversation(role: str, content: str):
    if not content or not content.strip():
        return
    if db:
        try:
            db.table("chat_history").insert({"role": role, "content": content}).execute()
        except Exception as e:
            print(f"Warning: Failed to log conversation to Supabase: {e}")