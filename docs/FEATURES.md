# Jarvis AI Features

This document outlines the complete list of features integrated into the Jarvis AI Desktop Assistant.

## Core Assistant Features

* **Continuous Voice Listening:** Uses `speech_recognition` to detect commands seamlessly.
* **Wake Word Detection:** Responds to the "Jarvis" wake word before initiating a full command query.
* **Groq API Integration:** Lightning-fast AI responses powered by `llama3-70b-8192` (or configurable models) via Groq.
* **Text-To-Speech (TTS):** Uses Google TTS (`gTTS`) combined with `pygame` for smooth playback, with a robust offline fallback via `pyttsx3`.

## Productivity Features (Supabase Powered)

* **Persistent Memory:** Chat history logging to Supabase to retain conversational context.
* **To-Do List Manager:** Voice-activated task management ("add buy milk to my task list").
* **Smart Notes:** Speak to save important information directly into your secure database.
* **Clipboard Manager:** Read and write directly to your OS clipboard using voice commands.
* **Email Integration:** Read your latest unread emails securely using the official Gmail API via OAuth 2.0.

## Automation & Utility Features

* **App Launcher:** Open any desktop application directly (e.g., Chrome, VS Code, Notepad).
* **File Search:** Rapidly search your file system for specific documents or files.
* **Web Navigation:** Open specific websites instantly (Google, LinkedIn, Netflix, YouTube).
* **Media & Music:** Automatically search and play requested songs/videos on YouTube.
* **Daily Summary:** Gives a personalized briefing including date, time, top news headlines, and a motivational quote.
* **Dictionary:** Get instant definitions of complex words via the Free Dictionary API.
* **Reminders/Alarms:** Thread-based background timers to remind you of tasks without blocking the main assistant thread.

## User Interface (Frontend)

* **Glassmorphism Design:** Modern, futuristic, and sleek aesthetic with a dark theme.
* **Real-time WebSockets:** Instant UI updates reflecting the assistant's internal state (Listening, Processing, Offline).
* **Voice Waveform Animations:** Dynamic CSS animations that respond when Jarvis is active.
* **Chat History Feed:** Scrollable interface displaying the live conversation log.
