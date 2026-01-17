from fastapi import WebSocket
import json
from app.chains.career_chain import QUESTIONS, predict_careers_from_answers
from app.crud.career import save_user_career
from app.db.database import get_db

async def career_ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()

    state = {
        "current_index": 0,
        "answers": {}
    }

    while True:
        msg = json.loads(await websocket.receive_text())

        if msg["type"] == "start_career":
            state["current_index"] = 0
            state["answers"] = {}

            await websocket.send_text(json.dumps({
                "type": "career_question",
                "question_id": 0,
                "question": QUESTIONS[0]
            }))

        elif msg["type"] == "career_answer":
            idx = state["current_index"]

            # SAFETY CHECK
            if idx >= len(QUESTIONS):
                continue  # ignore extra answers

            question = QUESTIONS[idx]
            state["answers"][question] = msg["answer"]

            state["current_index"] += 1

            # ASK NEXT QUESTION
            if state["current_index"] < len(QUESTIONS):
                next_idx = state["current_index"]
                await websocket.send_text(json.dumps({
                    "type": "career_question",
                    "question_id": next_idx,
                    "question": QUESTIONS[next_idx]
                }))
            else:
                # FINISH QUESTIONS
                careers = await predict_careers_from_answers(state["answers"])

                await websocket.send_text(json.dumps({
                    "type": "career_result",
                    "careers": careers
                }))

        elif msg["type"] == "select_career":
            selected_career = msg["career"]

            async for db in get_db():
                await save_user_career(db, user_id, selected_career)

            await websocket.send_text(json.dumps({
                "type": "career_saved",
                "career": selected_career
            }))
            break
