# J.A.R.V.I.S. Pro — Autonomous AI Desktop & Quantitative Trading System

[![Groq](https://img.shields.io/badge/AI%20Brain-Groq%20LLaMA%203.3%2070B-6366F1)](https://groq.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20ASGI-059669)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Electron-06B6D4)](https://react.dev)
[![Trading](https://img.shields.io/badge/Engine-Paper%20Trading%20%26%20Quant-F59E0B)]()

**J.A.R.V.I.S. (Just A Rather Very Intelligent System)** is a state-of-the-art autonomous desktop AI assistant and real-time quantitative trading terminal. Designed with a sleek Obsidian Glassmorphism theme inspired by Linear and TradingView, J.A.R.V.I.S. combines multi-turn conversational intelligence, autonomous tool dispatching, paper trading execution ($100k sandbox), technical analysis indicators (RSI, MACD, EMA ribbons), and full desktop automation.

---

## 🚀 Key Features

* **🧠 Autonomous Groq LLaMA 3.3 Engine:** Native function/tool calling for tasks, notes, alarms, market quotes, paper orders, and OS automation.
* **🎙️ Acoustic Voice Interface:** Real-time wake-word detection ("Jarvis") with Azure Neural TTS (`edge-tts`) and dynamic canvas frequency visualizer.
* **📈 Paper Trading Simulator:** $100,000 USD virtual brokerage account supporting Market/Limit orders, position tracking, and live P&L calculations.
* **📊 Quantitative Technical Analysis:** Mathematical calculations for RSI (14), MACD (12/26/9), EMA (20/50/200), and Bollinger Bands with interactive candlestick charting.
* **💼 Portfolio Risk Analytics:** Real-time computation of Sharpe Ratio, Maximum Drawdown (MDD), Win Rate, and Asset Allocation breakdowns.
* **📝 Resilient Productivity Hub:** Task checklists with priority tagging, smart notes, and automated Supabase / local JSON storage fallbacks.
* **⚡ Host Hardware Telemetry:** Real-time CPU, RAM, Battery, and network latency monitoring gauges.
* **🖥️ Electron Desktop Wrapper:** Native cross-platform desktop application packaging.

---

## 📁 Architecture & Folder Structure

```bash
Jharvis BOT/
├── backend/
│   ├── main.py                  # FastAPI server, REST routes & WebSocket hub
│   ├── ai/
│   │   ├── groq_client.py       # Multi-turn conversational memory & tool loop
│   │   ├── tools.py             # Groq function calling registry & dispatchers
│   │   └── task_planner.py      # JSON-schema multi-step automation planner
│   ├── speech/
│   │   ├── listener.py          # Ambient speech recognition & wake-word gating
│   │   ├── speaker.py           # Async Edge-TTS neural speech synthesis
│   │   └── state.py             # Atomic audio mutex lock
│   ├── trading/
│   │   ├── market_data.py       # Real-time quotes & historical candlestick cache
│   │   ├── indicators.py        # Quantitative math for RSI, MACD, EMA, Bollinger
│   │   ├── paper_engine.py      # Virtual broker simulator ($100k sandbox)
│   │   └── portfolio_analytics.py # Sharpe ratio, MDD, win rate, & equity curves
│   ├── automation/              # PyAutoGUI, Playwright, window management & monitor
│   ├── productivity/            # Notes, tasks, clipboard, & Gmail API integration
│   ├── reminders/               # Threaded alarms & timers
│   └── database/                # Supabase PostgreSQL client & local fallback
├── frontend/
│   ├── main.cjs                 # Electron window container (1200x800)
│   └── src/
│       ├── App.jsx              # Master state, tabs, & WebSocket lifecycle
│       ├── App.css              # Obsidian slate design tokens & glassmorphism
│       ├── components/
│       │   ├── Header.jsx       # Latency, Groq status, & quick balance badge
│       │   ├── HomeView.jsx     # AI Assistant terminal & audio visualizer
│       │   ├── MarketView.jsx   # Interactive Candlestick chart & Trade Console
│       │   ├── PortfolioView.jsx# Equity curves, risk gauges & trade journal
│       │   ├── ProductivityView.jsx # Tasks checklist & Smart Notes
│       │   ├── SystemMonitor.jsx# Host CPU & RAM telemetry meters
│       │   └── Icons.jsx        # High-res SVG icon library
├── data/                        # Persistent local JSON data cache
├── requirements.txt             # Python dependencies
└── package.json                 # Frontend & Electron scripts
```

---

## 🛠️ Quick Start Guide

### 1. Environment Setup
Create or update `.env` in the root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=your_supabase_url_optional
SUPABASE_KEY=your_supabase_anon_key_optional
```

### 2. Start the Backend Server
```bash
# Activate Python Virtual Environment
.venv\Scripts\activate

# Run FastAPI ASGI server with auto-reload
uvicorn backend.main:app --reload --port 8000
```

### 3. Start the Frontend & Desktop App
```bash
# In a new terminal
cd frontend
npm install

# Run Vite web development server
npm run dev

# Or launch as native Electron desktop window
npm run electron:dev
```

