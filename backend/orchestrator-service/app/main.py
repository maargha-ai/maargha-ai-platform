# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.graph.orchestrator_graph import app as graph_app
from app.core.state import AgentState
from app.db.database import engine, Base
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.ws import quiz, emotional_support, career, linkedin, tutor
from app.router import music, roadmap, jobs, news
import json
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm
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

async def general_chat_reply(state: AgentState, message: str) -> str:
    state["messages"].append({"role": "user", "content": message})

    response = await llm.ainvoke([
        HumanMessage(content=m["content"])
        for m in state["messages"]
        if m["role"] == "user"
    ])

    reply = response.content.strip()

    state["messages"].append({
        "role": "assistant",
        "content": reply
    })

    return reply

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    user_id = id(websocket)
    state: AgentState = {
        "user_id": user_id,
        "messages": [],
        "agent_done": False,
    }

    try:
        while True:
            data = await websocket.receive_text()

            state["messages"].append({
                "role": "user",
                "content": data
            })

            output = await graph_app.ainvoke(state)

            agent_action = output.get("agent_action")
            agent_response = output.get("agent_response")
            navigate = output.get("navigate")

            state.update(output)

            print(
                f"[Main] Action: {state.get('agent_action')} | "
                f"Agent Response: {state.get('agent_response')}"
            )

            # CHAT
            if agent_action == "CHAT" and agent_response:
                await websocket.send_text(json.dumps({
                    "type": "CHAT",
                    "content": agent_response
                }))

            # NAVIGATION
            if navigate:
                await websocket.send_text(json.dumps({
                    "navigate": navigate
                }))

            # cleanup
            state["agent_action"] = None
            state["agent_response"] = None
            state.pop("navigate", None)

    except WebSocketDisconnect:
        print(f"User disconnected: {user_id}")