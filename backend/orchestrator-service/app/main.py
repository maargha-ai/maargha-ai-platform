# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.graph.orchestrator_graph import app as graph_app
from app.core.state import AgentState
from app.db.database import engine, Base
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.ws import quiz, emotional_support, career, linkedin, tutor, live_chat
from app.router import music, roadmap, jobs, news, cv
from fastapi import WebSocket
from app.agents.emotional_support_agent import transcribe_audio 
import json
import numpy as np
import io
import soundfile as sf
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="MAARGHA AI Orchestrator")

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(music.router)
app.include_router(roadmap.router)
app.include_router(jobs.router)
app.include_router(news.router)
app.include_router(cv.router)

@app.websocket("/ws/career/{user_id}")
async def career_ws(websocket: WebSocket, user_id: str):
    await career.career_ws_handler(websocket, user_id)

@app.websocket("/ws/quiz/{user_id}")
async def quiz_ws(websocket: WebSocket, user_id: str):
    await quiz.quiz_ws_handler(websocket, user_id)

@app.websocket("/ws/emotional-support/{user_id}")
async def emotional_support_ws_route(websocket: WebSocket, user_id: str):
    await emotional_support.emotional_support_ws(websocket, user_id)

@app.websocket("/ws/linkedin/{user_id}")
async def linkedin_ws(websocket: WebSocket, user_id: str):
    await linkedin.linkedin_ws_handler(websocket, user_id)

@app.websocket("/ws/tutor/{user_id}")
async def tutor_ws(websocket: WebSocket, user_id: str):
    await tutor.tutor_ws_handler(websocket, user_id)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.websocket("/ws/chat/live")
async def chat_live(websocket: WebSocket):
    await live_chat.chat_live_ws(websocket)

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    print("[CHAT] Connected")

    state: AgentState = {
        "user_id": id(websocket),
        "messages": [],
        "agent_done": False,
    }

    try:
        while True:
            text = await websocket.receive_text()
            print("[CHAT] User:", text)

            state["messages"].append({"role": "user", "content": text})

            output = await graph_app.ainvoke(state)
            state.update(output)

            if state.get("agent_response"):
                await websocket.send_text(json.dumps({
                    "type": "CHAT",
                    "content": state["agent_response"]
                }))

            if state.get("navigate"):
                await websocket.send_text(json.dumps({
                    "navigate": state["navigate"]
                }))

            state.pop("agent_response", None)
            state.pop("navigate", None)

    except WebSocketDisconnect:
        print("[CHAT] Disconnected")

