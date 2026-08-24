# J.A.R.V.I.S. Pro — Feature Specifications

This document outlines the complete capabilities of the J.A.R.V.I.S. Desktop AI & Quantitative Platform.

---

## 1. Autonomous AI Assistant & Tool Execution
* **Groq LLaMA 3.3 70B Integration:** Ultra-fast sub-200ms conversational inference.
* **Native Tool Calling Engine:** Dynamic function calling dispatch for productivity, market data, paper orders, alarms, and OS automation.
* **Sliding Window Multi-Turn Memory:** Retains multi-turn conversation context across queries.
* **Dual Input Gateways:** Voice microphone input and instant text command input.

## 2. Voice & Audio Pipeline
* **Wake-Word Gating:** Recognizes the "Jarvis" wake-word before activating query ingestion.
* **Neural Text-To-Speech (Edge-TTS):** High-fidelity Microsoft Azure neural voice synthesis (`en-US-AriaNeural`).
* **Acoustic Audio Visualizer:** Real-time acoustic frequency spectrum bars reacting to listening and processing states.
* **Offline Fallback:** Automated fallback to `pyttsx3` when offline.

## 3. Paper Trading Simulator & Market Engine
* **Virtual Broker Simulation:** $100,000 USD sandbox cash balance for zero-risk trading.
* **Order Execution Engine:** Instant execution of Market and Limit BUY/SELL orders.
* **Real-time Price Feeds:** Live quotes and historical candlestick retrieval for US Equities (AAPL, NVDA, TSLA, MSFT, SPY, etc.) and Crypto (BTC, ETH, SOL).
* **Position Tracking:** Automatic tracking of average cost basis, market value, and unrealized/realized P&L.

## 4. Quantitative Technical Analysis Engine
* **Relative Strength Index (RSI 14):** Wilder's smoothed momentum oscillator with overbought/oversold boundaries.
* **Moving Average Convergence Divergence (MACD):** Fast 12, Slow 26, Signal 9 line and histogram crossover detection.
* **Exponential Moving Average (EMA):** 20, 50, and 200 EMA ribbon overlays.
* **Bollinger Bands (BB 20, 2):** Volatility channel bands.
* **Interactive Candlestick Chart:** High-performance SVG candlestick and volume rendering.

## 5. Portfolio Analytics & Risk Metrics
* **Sharpe Ratio:** Annualized risk-adjusted return ratio.
* **Maximum Drawdown (MDD):** Peak-to-trough risk percentage evaluation.
* **Win Rate & Profit Factor:** Historical execution profitability statistics.
* **Asset Allocation:** Real-time percentage distribution across cash and open assets.
* **Equity Curve Visualization:** Cumulative portfolio growth time-series.

## 6. Resilient Productivity Hub
* **Task Checklist:** Interactive to-do checklist with priority tags (High, Medium, Low) and completion status.
* **Smart Notes:** Instant thought capture and searchable note log with timestamps.
* **Hybrid Storage Engine:** Supabase PostgreSQL integration with automatic local JSON fallback.
* **Alarms & Reminders:** Threaded background timers with audio and visual triggers.
* **Clipboard Tools:** Voice and automated clipboard reading/writing.

## 7. Hardware Telemetry & Desktop Automation
* **Host Telemetry:** Real-time CPU usage, RAM utilization, and battery state.
* **OS Task Planner:** Break down multi-step desktop automation into actionable sequences.
* **Safety Failsafe:** Hardware emergency killswitch (`Ctrl + Shift + Esc`) to abort automation runs.

