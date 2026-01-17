from fastapi import WebSocket
import json
from app.quiz.service import generate_quiz_direct
from app.chains.quiz_evaluation_chain import evaluate_quiz
from app.fer.emotion_buffer import summarize, reset_buffer
from app.fer.active_user import set_active_user, clear_active_user
from app.fer.camera_runner import start_fer, stop_fer
from app.utils.reset_quiz import reset_quiz_state

async def quiz_ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()

    state = {
        "quiz_topic": None,
        "quiz_level": None,
        "current_question": None,
        "quiz_answers": {},
    }

    while True:
        msg = json.loads(await websocket.receive_text())

        # ▶ START QUIZ
        if msg["type"] == "start_quiz":
            set_active_user(user_id)
            reset_buffer(user_id)
            start_fer()                 # ✅ start FER ONLY here
            reset_quiz_state(state)

            state["quiz_topic"] = msg["topic"]
            state["quiz_level"] = msg["level"]

            q = await generate_quiz_direct(
                topic=state["quiz_topic"],
                level=state["quiz_level"]
            )

            state["current_question"] = q["question"]

            await websocket.send_text(json.dumps({
                "type": "quiz_question",
                "question": state["current_question"]
            }))

        # ▶ ANSWER QUESTION
        elif msg["type"] == "quiz_answer":
            question = state["current_question"]
            answer = msg["answer"]

            state["quiz_answers"][question] = answer

            q = await generate_quiz_direct(
                topic=state["quiz_topic"],
                level=state["quiz_level"]
            )

            state["current_question"] = q["question"]

            await websocket.send_text(json.dumps({
                "type": "quiz_question",
                "question": state["current_question"]
            }))

        # 🛑 STOP QUIZ
        elif msg["type"] == "stop_quiz":
            emotions = summarize(user_id)

            evaluation = await evaluate_quiz(
                career=state["quiz_topic"],
                quiz_answers=state["quiz_answers"],
                emotion_summary=emotions
            )

            stop_fer()                  # ✅ stop FER here
            clear_active_user()

            await websocket.send_text(json.dumps({
                "type": "quiz_evaluation",
                "result": evaluation
            }))
            break
