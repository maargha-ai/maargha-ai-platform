# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.graph.orchestrator_graph import app as graph_app
from app.core.state import AgentState
from app.db.database import engine, Base
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.core.session_store import USER_STATE
import shutil
from app.intent.intent_router import route_intent
from app.intent.planner_gate import should_enter_planner

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

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# WebSocket endpoint for real-time chat
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    if user_id not in USER_STATE:
        USER_STATE[user_id] = {}

    # Initial state
    state: AgentState = {
        "messages": [],
        "user_id": user_id,

        # agent loop
        "agent_thought": None,
        "agent_action": None,
        "agent_action_input": None,
        "agent_done": False,
        "agent_waiting_for_user": False,

        # domain state
        "selected_career": None,
        "roadmap_generated": False,

        "career_answers": {},
        "career_question_idx": 0,
        "career_options": None,

        # jobs
        "cv_path": USER_STATE[user_id].get("cv_path"),
        "job_role": None,
        "job_location": None,
    }

    try:
        while True:
            data = await websocket.receive_text()
            print(f"[DEBUG main] Received user message: {data}")

            state["messages"].append({"role": "user", "content": data})
            # Reset waiting flag
            state["agent_waiting_for_user"] = False
            # Route intent
            intent = await route_intent(data)
            print(f"[INTENT] Detected intent: {intent}")

            enter_planner = (
                intent != "general_chat"
                or state.get("career_question_idx") is not 0
                or state.get("career_options") is not None
                or state.get("selected_career") is not None
            )

            # Planner gate
            if not enter_planner:
                # Casual chat response (NO LangGraph)
                await websocket.send_text(
                    "Got it! Whenever you're ready, I can help with careers, roadmaps, or jobs."
                )
                continue
            
            print(f"[DEBUG main] Received user message: {data}")
            # print(f"[DEBUG main] Pre-ainvoke state: {state}")

            output = await graph_app.ainvoke(
                state,
                config={"recursion_limit": 10}
                )
            print(f"\n[DEBUG main] Graph output: {output}")
            state.update(output)

            # print(f"[DEBUG main] Post-ainvoke state: {state}")
            if state["messages"] and state["messages"][-1]["role"] == "assistant":
                reply = state["messages"][-1]["content"]
                print(f"\n[DEBUG main] Sending assistant reply: {reply}")
                await websocket.send_text(reply)
            
            if state.get("agent_done"):
                print("\n[DEBUG main] Agent done — breaking")
                break

    except WebSocketDisconnect:
        print(f"[main 6] User disconnected: {user_id}")

@app.post("/upload-cv/{user_id}")
async def upload_cv(user_id: str, file: UploadFile = File(...)):
    user_dir = STATIC_DIR / "cvs" / user_id
    user_dir.mkdir(parents=True, exist_ok=True)

    cv_path = user_dir / file.filename
    with open(cv_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # THIS IS THE CRITICAL PART
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {}

    USER_STATE[user_id]["cv_path"] = str(cv_path)
    return {
        "message": "CV uploaded successfully",
        "cv_path": str(cv_path)
    }
