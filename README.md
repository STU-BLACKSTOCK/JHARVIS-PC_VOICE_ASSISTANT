# J.A.R.V.I.S. Desktop AI Assistant

![Jarvis AI](https://ui-avatars.com/api/?name=J&background=0D8ABC&color=fff&rounded=true&size=128)

An advanced, production-ready desktop voice assistant powered by Groq, FastAPI, React, and Supabase. Designed with a stunning cyberpunk/glassmorphism UI and lightning-fast AI responses.

## 🚀 Project Overview

The Jarvis AI Desktop Assistant project is a complete overhaul of a legacy voice assistant. It transitions from a simple, monolithic script into a highly scalable full-stack application. It features real-time voice interaction, background task execution, and seamless productivity integrations (Notes, Tasks, Reminders).

### Core Technologies
- **AI Brain:** Groq API (`llama3-70b-8192`)
- **Backend:** Python, FastAPI, WebSockets
- **Frontend:** React (Vite), Vanilla CSS (Glassmorphism), Electron (Desktop Wrapper)
- **Database:** Supabase (PostgreSQL)
- **Email:** Google Gmail API (OAuth 2.0)
- **Voice/Audio:** `speech_recognition`, `pyttsx3`, `gTTS`, `pygame`

## 📁 Architecture & Folder Structure

```bash
jarvis/
├── backend/                  # Python FastAPI Backend
│   ├── main.py               # FastAPI & WebSocket entry
│   ├── ai/                   # Groq SDK integration
│   ├── speech/               # Listening and TTS modules
│   ├── automation/           # Apps, Files, and Web handlers
│   ├── productivity/         # Notes, Tasks, Clipboard
│   ├── reminders/            # Threaded Alarms
│   └── database/             # Supabase Client
├── frontend/                 # React UI
│   └── src/                  # Glassmorphism UI & Socket hooks
├── docs/                     # Detailed Documentation
├── .env                      # Environment Variables
└── requirements.txt          # Python Dependencies
```

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/STU-BLACKSTOCK/JHARVIS-PC_VOICE_ASSISTANT.git
cd "JHARVIS-PC_VOICE_ASSISTANT"
```

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Backend Setup
Activate your virtual environment and install dependencies:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend server:
```bash
uvicorn backend.main:app --reload --port 8000
```

### 4. Frontend Setup
In a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

## 🌟 Future Roadmap
- [ ] Implement robust IMAP/SMTP Email integration.
- [ ] Wrap the React application in Electron for native desktop packaging.
- [ ] Connect the backend asyncio speech listening loop directly to the WebSocket stream.

## 🤝 Contribution
Contributions, issues, and feature requests are welcome!

---
*Built with ❤️ and Groq.*
