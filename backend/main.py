from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import asyncio

from backend.speech.listener import listen, listen_for_wake_word
from backend.ai.groq_client import aiProcess
from backend.speech.speaker import speak
from backend.automation.system_monitor import get_system_stats
from backend.productivity import notes_tasks
from backend.trading import market_data, indicators, paper_engine, portfolio_analytics

app = FastAPI(title="J.A.R.V.I.S. Core Backend", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections = set()

# Request Models
class NoteCreate(BaseModel):
    content: str

class TaskCreate(BaseModel):
    content: str
    priority: Optional[str] = "medium"

class TaskToggle(BaseModel):
    task_id: str
    status: Optional[str] = None

class OrderRequest(BaseModel):
    symbol: str
    shares: float
    side: str
    order_type: Optional[str] = "MARKET"
    limit_price: Optional[float] = None

class ChatRequest(BaseModel):
    message: str

async def broadcast(message: dict):
    """Broadcasts a JSON message to all active WebSocket clients."""
    if not active_connections:
        return
    msg_str = json.dumps(message)
    async def send_msg(conn):
        try:
            await conn.send_text(msg_str)
        except Exception:
            active_connections.discard(conn)
    await asyncio.gather(*(send_msg(conn) for conn in list(active_connections)), return_exceptions=True)

# ----------------- REST ENDPOINTS -----------------

@app.get("/")
def read_root():
    return {"status": "Jarvis Backend is operational", "version": "2.0.0"}

# Productivity Endpoints
@app.get("/api/notes")
def api_get_notes(limit: int = 20):
    return notes_tasks.get_notes(limit)

@app.post("/api/notes")
def api_add_note(note: NoteCreate):
    res = notes_tasks.add_note(note.content)
    return {"message": res, "notes": notes_tasks.get_notes()}

@app.delete("/api/notes/{note_id}")
def api_delete_note(note_id: str):
    notes_tasks.delete_note(note_id)
    return {"success": True, "notes": notes_tasks.get_notes()}

@app.get("/api/tasks")
def api_get_tasks(limit: int = 50):
    return notes_tasks.get_tasks(limit)

@app.post("/api/tasks")
def api_add_task(task: TaskCreate):
    res = notes_tasks.add_task(task.content, task.priority)
    return {"message": res, "tasks": notes_tasks.get_tasks()}

@app.post("/api/tasks/toggle")
def api_toggle_task(req: TaskToggle):
    notes_tasks.toggle_task(req.task_id, req.status)
    return {"success": True, "tasks": notes_tasks.get_tasks()}

@app.delete("/api/tasks/{task_id}")
def api_delete_task(task_id: str):
    notes_tasks.delete_task(task_id)
    return {"success": True, "tasks": notes_tasks.get_tasks()}

# Trading & Market Endpoints
@app.get("/api/trading/watchlist")
def api_get_watchlist():
    return market_data.get_watchlist_quotes()

@app.get("/api/trading/price/{symbol}")
def api_get_price(symbol: str):
    price = market_data.get_current_price(symbol)
    return {"symbol": symbol.upper(), "price": price}

@app.get("/api/trading/candles/{symbol}")
def api_get_candles(symbol: str, interval: str = "1d", range_str: str = "3mo"):
    candles = market_data.get_historical_candles(symbol, interval, range_str)
    inds = indicators.calculate_all_indicators(candles)
    return {
        "symbol": symbol.upper(),
        "candles": candles,
        "indicators": inds
    }

@app.post("/api/trading/order")
def api_place_order(order: OrderRequest):
    res = paper_engine.place_order(
        symbol=order.symbol,
        shares=order.shares,
        side=order.side,
        order_type=order.order_type,
        limit_price=order.limit_price
    )
    return res

@app.get("/api/trading/portfolio")
def api_get_portfolio():
    return paper_engine.get_portfolio_state()

@app.post("/api/trading/portfolio/reset")
def api_reset_portfolio():
    return paper_engine.reset_portfolio()

@app.get("/api/trading/analytics")
def api_get_analytics():
    return portfolio_analytics.compute_portfolio_analytics()

# System Telemetry
@app.get("/api/system/stats")
async def api_system_stats():
    return await asyncio.to_thread(get_system_stats)

# Direct Text Chat Endpoint
@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    loop = asyncio.get_running_loop()
    def sync_broadcast(msg: dict):
        asyncio.run_coroutine_threadsafe(broadcast(msg), loop)

    await broadcast({"type": "status", "message": "Processing..."})
    await broadcast({"type": "response", "message": req.message, "role": "user"})

    reply = await asyncio.to_thread(aiProcess, req.message, sync_broadcast)
    await broadcast({"type": "response", "message": reply, "role": "jarvis"})
    await asyncio.to_thread(speak, reply)
    await broadcast({"type": "status", "message": "Online"})
    return {"response": reply}

# ----------------- WEBSOCKET HANDLER -----------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    loop = asyncio.get_running_loop()

    def sync_broadcast(msg: dict):
        asyncio.run_coroutine_threadsafe(broadcast(msg), loop)

    try:
        # Send initial state greeting
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Connected to Jarvis Neural Hub",
            "portfolio": paper_engine.get_portfolio_state(),
            "watchlist": market_data.get_watchlist_quotes()
        }))

        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                msg_type = message.get("type")

                if msg_type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))

                elif msg_type == "get_system_stats":
                    stats = await asyncio.to_thread(get_system_stats)
                    if stats:
                        stats["type"] = "system_stats"
                        await websocket.send_text(json.dumps(stats))

                elif msg_type == "chat_message":
                    user_text = message.get("message", "").strip()
                    if user_text:
                        await broadcast({"type": "status", "message": "Processing..."})
                        await broadcast({"type": "response", "message": user_text, "role": "user"})
                        
                        reply = await asyncio.to_thread(aiProcess, user_text, sync_broadcast)
                        await broadcast({"type": "response", "message": reply, "role": "jarvis"})
                        await asyncio.to_thread(speak, reply)
                        await broadcast({"type": "status", "message": "Online"})

            except Exception as e:
                print(f"Error processing websocket frame: {e}")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Websocket connection error: {e}")
    finally:
        active_connections.discard(websocket)

# ----------------- CONTINUOUS VOICE ASSISTANT LOOP -----------------

async def continuous_listening_loop():
    """Continuously listens for wake-word or voice commands and dispatches to Groq."""
    loop = asyncio.get_running_loop()
    def sync_broadcast(msg: dict):
        asyncio.run_coroutine_threadsafe(broadcast(msg), loop)

    while True:
        if not active_connections:
            await asyncio.sleep(1)
            continue

        try:
            await broadcast({"type": "status", "message": "Listening..."})
            
            # Listen for wake word ("jarvis") or speech input
            detected, command = await asyncio.to_thread(listen_for_wake_word, "jarvis")
            
            if detected:
                if not command:
                    # Spoke just "Jarvis", acknowledge and listen for query
                    await broadcast({"type": "status", "message": "Listening..."})
                    await asyncio.to_thread(speak, "Yes, sir?")
                    command = await asyncio.to_thread(listen, 8)

                if command and len(command.strip()) > 1:
                    await broadcast({"type": "status", "message": "Processing..."})
                    await broadcast({"type": "response", "message": command, "role": "user"})

                    # Route through autonomous Groq agent (tools & memory)
                    response = await asyncio.to_thread(aiProcess, command, sync_broadcast)
                    
                    await broadcast({"type": "response", "message": response, "role": "jarvis"})
                    await asyncio.to_thread(speak, response)
                    await broadcast({"type": "status", "message": "Online"})

            await asyncio.sleep(0.2)

        except Exception as e:
            print(f"Voice loop notice: {e}")
            await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(continuous_listening_loop())

