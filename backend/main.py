from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "get_system_stats":
                    from backend.automation.system_monitor import get_system_stats
                    # MUST run in thread because psutil.cpu_percent blocks for 0.5s!
                    stats = await asyncio.to_thread(get_system_stats)
                    if stats:
                        stats["type"] = "system_stats"
                        await websocket.send_text(json.dumps(stats))
            except Exception as e:
                print(f"Error processing websocket message: {e}")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Websocket connection error: {e}")
    finally:
        active_connections.discard(websocket)

@app.get("/")
def read_root():
    return {"status": "Jarvis Backend is running."}

async def broadcast(message: dict):
    if not active_connections:
        return
        
    msg_str = json.dumps(message)
    
    async def send_msg(conn):
        try:
            await conn.send_text(msg_str)
        except Exception:
            # Just discard dead connections silently without crashing the broadcast
            active_connections.discard(conn)
            
    # Gather creates concurrent tasks for ultra-fast broadcasting
    # list() creates a snapshot of the set to avoid "Set changed size during iteration"
    await asyncio.gather(*(send_msg(conn) for conn in list(active_connections)), return_exceptions=True)

from backend.speech.listener import listen
from backend.ai.groq_client import aiProcess
from backend.speech.speaker import speak
from backend.ai.task_planner import plan_task
from backend.automation.workflow_engine import run_workflow

automation_keywords = ["open", "search", "type", "automate", "take a screenshot", "minimize", "minimise", "maximize", "maximise", "close", "switch"]

async def continuous_listening_loop():
    """Background task to listen continuously and broadcast states."""
    loop = asyncio.get_running_loop()
    
    def sync_broadcast(msg: dict):
        asyncio.run_coroutine_threadsafe(broadcast(msg), loop)

    while True:
        if not active_connections:
            await asyncio.sleep(1) # Wait for a connection
            continue
            
        try:
            await broadcast({"type": "status", "message": "Listening..."})
            
            # Run the blocking speech recognition in a thread
            command = await asyncio.to_thread(listen)
            
            if command:
                await broadcast({"type": "status", "message": "Processing..."})
                
                # Send the detected text to the frontend chat history
                await broadcast({"type": "response", "message": command, "role": "user"})
                
                command_lower = command.lower()
                
                # Intent Detection: If the user wants to automate something
                if any(keyword in command_lower for keyword in automation_keywords):
                    await broadcast({"type": "response", "message": "Planning automation steps...", "role": "jarvis"})
                    
                    # Plan the steps using LLM
                    steps = await asyncio.to_thread(plan_task, command)
                    
                    if steps:
                        await broadcast({"type": "response", "message": f"Executing {len(steps)} steps.", "role": "jarvis"})
                        
                        results = await asyncio.to_thread(run_workflow, steps, sync_broadcast)
                        
                        # Generate a nice completion message based on results
                        if any("ABORTED" in res for res in results if isinstance(res, str)):
                            final_msg = "Automation was successfully aborted."
                        elif any("Failed" in res for res in results if isinstance(res, str)):
                            final_msg = "I attempted the automation, but encountered some issues."
                        else:
                            final_msg = "Automation tasks completed successfully."
                            
                        await broadcast({"type": "response", "message": final_msg, "role": "jarvis"})
                        await asyncio.to_thread(speak, final_msg)
                    else:
                        await broadcast({"type": "response", "message": "I could not figure out how to automate that.", "role": "jarvis"})
                        await asyncio.to_thread(speak, "I could not figure out how to automate that.")
                else:
                    # Regular conversational Process with Groq
                    response = await asyncio.to_thread(aiProcess, command)
                    
                    # Send the response back to the frontend
                    await broadcast({"type": "response", "message": response, "role": "jarvis"})
                    
                    # Speak it aloud
                    await asyncio.to_thread(speak, response)
                    
        except Exception as e:
            print(f"CRITICAL ERROR in continuous listening loop: {e}")
            import traceback
            traceback.print_exc()
            await asyncio.sleep(2) # Prevent rapid crash loops

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(continuous_listening_loop())
