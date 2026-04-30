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

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages from UI if needed
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/")
def read_root():
    return {"status": "Jarvis Backend is running."}

async def broadcast(message: dict):
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(message))
        except:
            pass

from backend.speech.listener import listen
from backend.ai.groq_client import aiProcess
from backend.speech.speaker import speak

async def continuous_listening_loop():
    """Background task to listen continuously and broadcast states."""
    while True:
        if active_connections:
            await broadcast({"type": "status", "message": "Listening..."})
            
            # Run the blocking speech recognition in a thread
            command = await asyncio.to_thread(listen)
            
            if command:
                await broadcast({"type": "status", "message": "Processing..."})
                
                # Send the detected text to the frontend chat history
                await broadcast({"type": "response", "message": command, "role": "user"})
                
                # Process with Groq
                response = await asyncio.to_thread(aiProcess, command)
                
                # Send the response back to the frontend
                await broadcast({"type": "response", "message": response, "role": "jarvis"})
                
                # Speak it aloud
                await asyncio.to_thread(speak, response)
        else:
            await asyncio.sleep(1) # Wait for a connection

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(continuous_listening_loop())
