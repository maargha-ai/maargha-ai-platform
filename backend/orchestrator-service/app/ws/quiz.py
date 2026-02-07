from fastapi import WebSocket
import json

from app.quiz.service import generate_quiz_direct
from app.chains.quiz_evaluation_chain import evaluate_quiz
from app.utils.reset_quiz import reset_quiz_state
from app.monitoring.violation_tracker import ViolationTracker
from app.monitoring.gaze_detector import is_looking_away


# ---------------------------
# Finalize quiz (SEND ONLY)
# ---------------------------
async def finalize_quiz(websocket: WebSocket, state: dict):
    evaluation = await evaluate_quiz(
        career=state["quiz_topic"],
        quiz_answers=state["quiz_answers"]
    )

    await websocket.send_text(json.dumps({
        "type": "quiz_evaluation",
        "result": evaluation
    }))


# ---------------------------
# Quiz WebSocket handler
# ---------------------------
async def quiz_ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()

    state = {
        "quiz_topic": None,
        "quiz_level": None,
        "current_question": None,
        "quiz_answers": {},
        "asked_questions": set(),
        "violation_tracker": ViolationTracker(),
        "finalized": False,   # 🔒 prevent double finalize
    }

    try:
        while True:
            msg = json.loads(await websocket.receive_text())

            # ======================
            # START QUIZ
            # ======================
            if msg["type"] == "start_quiz":
                reset_quiz_state(state)
                state["finalized"] = False

                state["quiz_topic"] = msg["topic"]
                state["quiz_level"] = msg["level"]

                q = await generate_quiz_direct(
                    topic=state["quiz_topic"],
                    level=state["quiz_level"],
                    asked_questions=state["asked_questions"]
                )

                state["current_question"] = q["question"]

                await websocket.send_text(json.dumps({
                    "type": "quiz_question",
                    "question": state["current_question"]
                }))

            # ======================
            # ANSWER QUESTION
            # ======================
            elif msg["type"] == "quiz_answer":
                question = state["current_question"]
                answer = msg["answer"]

                # Store answer
                state["quiz_answers"][question] = answer

                # Generate NEXT question
                q = await generate_quiz_direct(
                    topic=state["quiz_topic"],
                    level=state["quiz_level"],
                    asked_questions=state["asked_questions"]
                )

                state["current_question"] = q["question"]

                await websocket.send_text(json.dumps({
                    "type": "quiz_question",
                    "question": state["current_question"]
                }))

            # ======================
            # MONITORING (Gaze)
            # ======================
            elif msg["type"] == "monitor_frame":
                frame = msg["frame"]

                if is_looking_away(frame):
                    warnings = state["violation_tracker"].register_violation()

                    if state["violation_tracker"].should_terminate():
                        if not state["finalized"]:
                            state["finalized"] = True

                            await websocket.send_text(json.dumps({
                                "type": "quiz_terminated",
                                "reason": "Repeated malpractice detected"
                            }))

                            await finalize_quiz(websocket, state)
                        break

                    await websocket.send_text(json.dumps({
                        "type": "quiz_warning",
                        "warnings": warnings
                    }))
                else:
                    state["violation_tracker"].reset()

            # ======================
            # MANUAL TERMINATION
            # ======================
            elif msg["type"] == "stop_quiz":
                if not state["finalized"]:
                    state["finalized"] = True
                    await finalize_quiz(websocket, state)
                break

    except Exception:
        # Client disconnected unexpectedly
        if state["quiz_answers"] and not state["finalized"]:
            state["finalized"] = True
            await finalize_quiz(websocket, state)
