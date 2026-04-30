import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Successfully connected to Supabase.")
    except Exception as e:
        supabase = None
        print(f"Failed to connect to Supabase: {e}")
else:
    supabase = None
    print("Supabase credentials not found. Database features will be disabled.")

def get_db():
    return supabase
