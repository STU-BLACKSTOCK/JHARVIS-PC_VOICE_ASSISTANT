import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_supabase_client = None
_last_check_time = 0
_is_healthy = False
COOLDOWN_SECONDS = 300 # 5 minute cooldown when host fails

if SUPABASE_URL and SUPABASE_KEY:
    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        _supabase_client = None
        print(f"Supabase initialization notice: {e}")

def get_db():
    """Returns Supabase client if healthy, else None (triggering fast local storage fallback)."""
    global _last_check_time, _is_healthy
    
    if not _supabase_client:
        return None

    # Check health with rate-limited probe
    now = time.time()
    if now - _last_check_time > COOLDOWN_SECONDS:
        _last_check_time = now
        try:
            # Lightweight health ping
            _supabase_client.table("notes").select("id").limit(1).execute()
            _is_healthy = True
        except Exception:
            _is_healthy = False
            
    return _supabase_client if _is_healthy else None

