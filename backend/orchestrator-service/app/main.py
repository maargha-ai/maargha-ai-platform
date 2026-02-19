# app/main.py
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.state import AgentState
from app.db.database import Base, engine
from app.graph.orchestrator_graph import app as graph_app
from app.monitoring.health import router as health_router

# Import monitoring and logging
from app.monitoring.logger import (
    LoggingMiddleware,
    orchestrator_logger,
    performance_monitor,
    websocket_logger,
)
from app.router import cv, jobs, music, news, resume_parser, roadmap
from app.ws import career, emotional_support, linkedin, live_chat, quiz, tutor

load_dotenv()

app = FastAPI(title="MAARGHA AI Orchestrator")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

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

# Include health check endpoints
app.include_router(health_router)

app.include_router(music.router)
app.include_router(roadmap.router)
app.include_router(jobs.router)
app.include_router(news.router)
app.include_router(cv.router)
app.include_router(resume_parser.router)


@app.websocket("/ws/career/{user_id}")
async def career_ws(websocket: WebSocket, user_id: str):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    try:
        orchestrator_logger.info(
            "Career WebSocket connection started",
            extra={"user_id": user_id, "endpoint": "/ws/career"},
        )
        await career.career_ws_handler(websocket, user_id)
    except Exception as e:
        orchestrator_logger.error(
            "Career WebSocket error", error=e, extra={"user_id": user_id}
        )
    finally:
        performance_monitor.record_websocket_disconnection()
        websocket_logger.info(
            "Career WebSocket connection closed", extra={"user_id": user_id}
        )


@app.websocket("/ws/quiz/{user_id}")
async def quiz_ws(websocket: WebSocket, user_id: str):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    try:
        orchestrator_logger.info(
            "Quiz WebSocket connection started",
            extra={"user_id": user_id, "endpoint": "/ws/quiz"},
        )
        await quiz.quiz_ws_handler(websocket, user_id)
    except Exception as e:
        orchestrator_logger.error(
            "Quiz WebSocket error", error=e, extra={"user_id": user_id}
        )
    finally:
        performance_monitor.record_websocket_disconnection()
        websocket_logger.info(
            "Quiz WebSocket connection closed", extra={"user_id": user_id}
        )


@app.websocket("/ws/emotional-support/{user_id}")
async def emotional_support_ws_route(websocket: WebSocket, user_id: str):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    try:
        orchestrator_logger.info(
            "Emotional Support WebSocket connection started",
            extra={"user_id": user_id, "endpoint": "/ws/emotional-support"},
        )
        await emotional_support.emotional_support_ws(websocket, user_id)
    except Exception as e:
        orchestrator_logger.error(
            "Emotional Support WebSocket error", error=e, extra={"user_id": user_id}
        )
    finally:
        performance_monitor.record_websocket_disconnection()
        websocket_logger.info(
            "Emotional Support WebSocket connection closed", extra={"user_id": user_id}
        )


@app.websocket("/ws/linkedin/{user_id}")
async def linkedin_ws(websocket: WebSocket, user_id: str):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    try:
        orchestrator_logger.info(
            "LinkedIn WebSocket connection started",
            extra={"user_id": user_id, "endpoint": "/ws/linkedin"},
        )
        await linkedin.linkedin_ws_handler(websocket, user_id)
    except Exception as e:
        orchestrator_logger.error(
            "LinkedIn WebSocket error", error=e, extra={"user_id": user_id}
        )
    finally:
        performance_monitor.record_websocket_disconnection()
        websocket_logger.info(
            "LinkedIn WebSocket connection closed", extra={"user_id": user_id}
        )


@app.websocket("/ws/tutor/{user_id}")
async def tutor_ws(websocket: WebSocket, user_id: str):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    try:
        orchestrator_logger.info(
            "Tutor WebSocket connection started",
            extra={"user_id": user_id, "endpoint": "/ws/tutor"},
        )
        await tutor.tutor_ws_handler(websocket, user_id)
    except Exception as e:
        orchestrator_logger.error(
            "Tutor WebSocket error", error=e, extra={"user_id": user_id}
        )
    finally:
        performance_monitor.record_websocket_disconnection()
        websocket_logger.info(
            "Tutor WebSocket connection closed", extra={"user_id": user_id}
        )


@app.on_event("startup")
async def on_startup():
    orchestrator_logger.info("Maargha Orchestrator starting up")

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        orchestrator_logger.info("Database initialized successfully")
    except Exception as e:
        orchestrator_logger.error("Database initialization failed", error=e)
        raise


@app.websocket("/ws/chat/live")
async def chat_live(websocket: WebSocket):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    try:
        orchestrator_logger.info("Live chat WebSocket connection started")
        await live_chat.chat_live_ws(websocket)
    except Exception as e:
        orchestrator_logger.error("Live chat WebSocket error", error=e)
    finally:
        performance_monitor.record_websocket_disconnection()
        websocket_logger.info("Live chat WebSocket connection closed")


@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    start_time = time.time()
    performance_monitor.record_websocket_connection()

    await websocket.accept()
    orchestrator_logger.info("Chat WebSocket connection established")

    state: AgentState = {
        "user_id": id(websocket),
        "messages": [],
        "agent_done": False,
    }

    try:
        while True:
            text = await websocket.receive_text()
            orchestrator_logger.info(
                "Chat message received",
                extra={"user_id": state["user_id"], "message_length": len(text)},
            )

            state["messages"].append({"role": "user", "content": text})

            output = await graph_app.ainvoke(state)
            state.update(output)

            if state.get("agent_response"):
                await websocket.send_text(
                    json.dumps({"type": "CHAT", "content": state["agent_response"]})
                )

                orchestrator_logger.info(
                    "Chat response sent",
                    extra={
                        "user_id": state["user_id"],
                        "response_length": len(state["agent_response"]),
                    },
                )

            if state.get("navigate"):
                await websocket.send_text(json.dumps({"navigate": state["navigate"]}))

                orchestrator_logger.info(
                    "Navigation command sent",
                    extra={
                        "user_id": state["user_id"],
                        "navigate_to": state["navigate"],
                    },
                )

            state.pop("agent_response", None)
            state.pop("navigate", None)

    except WebSocketDisconnect:
        orchestrator_logger.info(
            "Chat WebSocket disconnected", extra={"user_id": state["user_id"]}
        )
    except Exception as e:
        orchestrator_logger.error(
            "Chat WebSocket error", error=e, extra={"user_id": state["user_id"]}
        )
    finally:
        performance_monitor.record_websocket_disconnection()
