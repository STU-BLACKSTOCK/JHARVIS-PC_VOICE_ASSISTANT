import json
import os
import uuid
from datetime import datetime
from backend.database.db_client import get_db

# Local fallback storage path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
os.makedirs(DATA_DIR, exist_ok=True)
LOCAL_STORE_PATH = os.path.join(DATA_DIR, "productivity.json")

def _load_local_store() -> dict:
    if os.path.exists(LOCAL_STORE_PATH):
        try:
            with open(LOCAL_STORE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"notes": [], "tasks": [], "chat_history": []}

def _save_local_store(data: dict):
    try:
        with open(LOCAL_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving local productivity store: {e}")

def add_note(note_content: str) -> str:
    if not note_content or not note_content.strip():
        return "Cannot save an empty note."
    
    note_item = {
        "id": str(uuid.uuid4())[:8],
        "content": note_content.strip(),
        "created_at": datetime.now().isoformat()
    }
    
    db = get_db()
    if db:
        try:
            db.table("notes").insert({"content": note_item["content"]}).execute()
            return f"Note saved successfully: '{note_content.strip()}'"
        except Exception:
            pass

    # Local fallback
    store = _load_local_store()
    store["notes"].insert(0, note_item)
    _save_local_store(store)
    return f"Note saved successfully: '{note_content.strip()}'"

def get_notes(limit: int = 20) -> list:
    db = get_db()
    if db:
        try:
            response = db.table("notes").select("*").order('created_at', desc=True).limit(limit).execute()
            if response.data:
                return response.data
        except Exception:
            pass
            
    store = _load_local_store()
    return store.get("notes", [])[:limit]

def delete_note(note_id: str) -> bool:
    db = get_db()
    if db:
        try:
            db.table("notes").delete().eq("id", note_id).execute()
        except Exception:
            pass
    store = _load_local_store()
    store["notes"] = [n for n in store.get("notes", []) if n.get("id") != note_id]
    _save_local_store(store)
    return True

def add_task(task_content: str, priority: str = "medium") -> str:
    if not task_content or not task_content.strip():
        return "Cannot save an empty task."
    
    task_item = {
        "id": str(uuid.uuid4())[:8],
        "content": task_content.strip(),
        "status": "pending",
        "priority": priority,
        "created_at": datetime.now().isoformat()
    }
    
    db = get_db()
    if db:
        try:
            db.table("tasks").insert({"content": task_item["content"], "status": "pending"}).execute()
            return f"Task '{task_content.strip()}' added to your list."
        except Exception:
            pass

    store = _load_local_store()
    store["tasks"].insert(0, task_item)
    _save_local_store(store)
    return f"Task '{task_content.strip()}' added to your list."

def get_tasks(limit: int = 50) -> list:
    db = get_db()
    if db:
        try:
            response = db.table("tasks").select("*").order('created_at', desc=True).limit(limit).execute()
            if response.data:
                return response.data
        except Exception:
            pass
            
    store = _load_local_store()
    return store.get("tasks", [])[:limit]

def toggle_task(task_id: str, status: str = None) -> bool:
    store = _load_local_store()
    for task in store.get("tasks", []):
        if task.get("id") == task_id or task.get("content") == task_id:
            task["status"] = status if status else ("completed" if task.get("status") == "pending" else "pending")
            _save_local_store(store)
            return True
    return False

def delete_task(task_id: str) -> bool:
    db = get_db()
    if db:
        try:
            db.table("tasks").delete().eq("id", task_id).execute()
        except Exception:
            pass
    store = _load_local_store()
    store["tasks"] = [t for t in store.get("tasks", []) if t.get("id") != task_id and t.get("content") != task_id]
    _save_local_store(store)
    return True

def log_conversation(role: str, content: str):
    if not content or not content.strip():
        return
    db = get_db()
    if db:
        try:
            db.table("chat_history").insert({"role": role, "content": content}).execute()
        except Exception:
            pass
            
    store = _load_local_store()
    store.setdefault("chat_history", []).append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    # Keep last 100 entries locally
    store["chat_history"] = store["chat_history"][-100:]
    _save_local_store(store)

def get_chat_history(limit: int = 50) -> list:
    store = _load_local_store()
    return store.get("chat_history", [])[-limit:]