import asyncio
import json
import logging
import time
from collections import defaultdict, deque

from fastapi import WebSocket

from app.chains.quiz_evaluation_chain import evaluate_quiz
from app.monitoring.gaze_detector import is_looking_away
from app.monitoring.violation_tracker import ViolationTracker
from app.quiz.service import generate_fallback_question, generate_quiz_direct
from app.utils.reset_quiz import reset_quiz_state

RECENT_QUESTIONS = defaultdict(lambda: deque(maxlen=30))


def _history_key(user_id: str, topic: str, level: str) -> str:
    return f"{user_id}:{(topic or '').strip().lower()}:{(level or '').strip().lower()}"


async def finalize_quiz(websocket: WebSocket, state: dict):
    try:
        evaluation = await asyncio.wait_for(
            evaluate_quiz(
                career=state["quiz_topic"],
                quiz_answers=state["quiz_answers"],
            ),
            timeout=45,
        )
    except Exception:
        answered = [
            str(a).strip() for a in state["quiz_answers"].values() if str(a).strip()
        ]
        score = min(60, len(answered) * 20)
        evaluation = {
            "score": score,
            "level": "Intermediate" if score >= 50 else "Beginner",
            "summary": "Evaluation generated with fallback mode due to analyzer timeout.",
            "strengths": ["Responses were submitted and captured."],
            "weaknesses": ["Detailed AI analysis could not be completed in time."],
            "suggestions": [
                "Retry once for full analysis or continue practicing concise "
                "concept-first answers."
            ],
            "feedback": "Fallback evaluation generated.",
        }

    await websocket.send_text(
        json.dumps({"type": "quiz_evaluation", "result": evaluation})
    )


async def _get_next_question(user_id: str, state: dict) -> dict:
    history_key = _history_key(user_id, state["quiz_topic"], state["quiz_level"])

    try:
        q = await asyncio.wait_for(
            generate_quiz_direct(
                topic=state["quiz_topic"],
                level=state["quiz_level"],
                asked_questions=state["asked_questions"],
            ),
            timeout=6,
        )
    except Exception:
        q = generate_fallback_question(
            topic=state["quiz_topic"],
            level=state["quiz_level"],
            asked_questions=state["asked_questions"],
            offset=len(RECENT_QUESTIONS[history_key]),
        )

    state["current_question"] = q["question"]
    RECENT_QUESTIONS[history_key].append(state["current_question"])
    return q


async def quiz_ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()

    state = {
        "quiz_topic": None,
        "quiz_level": None,
        "current_question": None,
        "quiz_answers": {},
        "asked_questions": set(),
        "violation_tracker": ViolationTracker(),
        "finalized": False,
        "last_monitor_ts": 0.0,
        "away_streak": 0,
        "good_streak": 0,
        "last_warning_ts": 0.0,
    }

    try:
        while True:
            msg = json.loads(await websocket.receive_text())
            msg_type = msg.get("type")

            if msg_type == "start_quiz":
                reset_quiz_state(state)
                state["finalized"] = False
                state["last_monitor_ts"] = 0.0
                state["away_streak"] = 0
                state["good_streak"] = 0
                state["last_warning_ts"] = 0.0

                state["quiz_topic"] = msg.get("topic")
                state["quiz_level"] = msg.get("level")

                history_key = _history_key(
                    user_id, state["quiz_topic"], state["quiz_level"]
                )
                state["asked_questions"] = set(RECENT_QUESTIONS[history_key])

                q = await _get_next_question(user_id, state)
                await websocket.send_text(
                    json.dumps({"type": "quiz_question", "question": q["question"]})
                )

            elif msg_type == "quiz_answer":
                question = state.get("current_question")
                answer = (msg.get("answer") or "").strip()

                if question:
                    state["quiz_answers"][question] = answer

                q = await _get_next_question(user_id, state)
                await websocket.send_text(
                    json.dumps({"type": "quiz_question", "question": q["question"]})
                )

            elif msg_type == "monitor_frame":
                # Drop extra frames so monitoring does not block
                # question/evaluation flow.
                now = time.monotonic()
                if now - state["last_monitor_ts"] < 0.8:
                    continue
                state["last_monitor_ts"] = now

                frame = msg.get("frame")
                if not frame:
                    continue

                try:
                    away = await asyncio.to_thread(is_looking_away, frame)
                    logging.info(
                        "User %s: Gaze detection result - away=%s", user_id, away
                    )
                except Exception as e:
                    away = False
                    logging.error("User %s: Gaze detection error - %s", user_id, str(e))

                if away:
                    state["away_streak"] += 1
                    state["good_streak"] = 0
                    # Require sustained suspicious frames to reduce false positives.
                    if state["away_streak"] < 3:
                        continue
                    # Don't reset away_streak immediately - allow for continued
                    # violation detection.
                    # state["away_streak"] = 0  # Commented out to allow accumulation

                    # Cooldown between warning increments.
                    if now - state["last_warning_ts"] < 4.0:
                        continue
                    state["last_warning_ts"] = now

                    warnings = state["violation_tracker"].register_violation()
                    # Reset away_streak after registering a violation to prevent
                    # multiple rapid violations.
                    state["away_streak"] = 0
                    logging.warning(
                        "User %s: Violation registered - warnings=%s",
                        user_id,
                        warnings,
                    )

                    if state["violation_tracker"].should_terminate():
                        logging.error(
                            "User %s: Quiz terminated due to repeated malpractice",
                            user_id,
                        )
                        if not state["finalized"]:
                            state["finalized"] = True
                            await websocket.send_text(
                                json.dumps(
                                    {
                                        "type": "quiz_terminated",
                                        "reason": "Repeated malpractice detected",
                                    }
                                )
                            )
                            await finalize_quiz(websocket, state)
                        break

                    await websocket.send_text(
                        json.dumps({"type": "quiz_warning", "warnings": warnings})
                    )
                else:
                    state["away_streak"] = 0
                    state["good_streak"] += 1
                    # Decay one warning after sustained attentive frames.
                    if (
                        state["good_streak"] >= 10
                        and state["violation_tracker"].warnings > 0
                    ):  # Increased from 3 to 10
                        old_warnings = state["violation_tracker"].warnings
                        state["violation_tracker"].decay_warning()
                        logging.info(
                            "User %s: Warning decayed from %s to %s",
                            user_id,
                            old_warnings,
                            state["violation_tracker"].warnings,
                        )
                        state["good_streak"] = 0

            elif msg_type == "stop_quiz":
                answer = (msg.get("answer") or "").strip()
                question = state.get("current_question")
                if question and answer:
                    state["quiz_answers"][question] = answer

                if not state["finalized"]:
                    state["finalized"] = True
                    await finalize_quiz(websocket, state)
                break

    except Exception:
        if state["quiz_answers"] and not state["finalized"]:
            state["finalized"] = True
            await finalize_quiz(websocket, state)
