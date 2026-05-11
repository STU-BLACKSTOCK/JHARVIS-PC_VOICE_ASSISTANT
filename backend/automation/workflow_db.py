from backend.database.db_client import get_db

db = get_db()

def save_workflow(name: str, steps: list) -> str:
    if not db: return "Database not connected."
    try:
        db.table("workflows").insert({"name": name, "steps": steps}).execute()
        return f"Workflow '{name}' saved successfully."
    except Exception as e:
        return f"Failed to save workflow: {e}"

def get_workflows() -> list:
    if not db: return []
    try:
        response = db.table("workflows").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Failed to fetch workflows: {e}")
        return []

def log_system_stats(cpu: float, ram: float):
    if not db: return
    try:
        db.table("system_logs").insert({"cpu_percent": cpu, "ram_percent": ram}).execute()
    except:
        pass
