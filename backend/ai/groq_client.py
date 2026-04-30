import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    client = None
    print(f"Failed to initialize Groq client: {e}")

def aiProcess(command: str) -> str:
    if not client:
        return "Groq API is not configured properly."
        
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis. Give short, helpful, and concise responses."},
                {"role": "user", "content": command}
            ],
            model="llama3-70b-8192", # Using a fast groq model
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with Groq: {e}")
        return "I'm having trouble connecting to my AI brain right now."
