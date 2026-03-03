# orchestrator-service/app/ws/live_chat.py
import asyncio  # NEW: for watchdog
import json

import numpy as np
from fastapi import WebSocket

from app.agents.emotional_support_agent import transcribe_audio
from app.core.state import AgentState
from app.graph.orchestrator_graph import app as graph_app


async def chat_live_ws(websocket: WebSocket):
    await websocket.accept()
    print("[LIVE CHAT] Connected")

    audio_buffer = []
    state: AgentState = {
        "user_id": id(websocket),
        "messages": [],
        "agent_done": False,
    }

    last_activity = asyncio.get_event_loop().time()  # NEW: for idle timeout

    async def watchdog():
        while True:
            await asyncio.sleep(30)  # Check every 30s
            if asyncio.get_event_loop().time() - last_activity > 300:  # 5 min idle
                print("[LIVE CHAT] Idle timeout - closing")
                await websocket.close()
                break

    watchdog_task = asyncio.create_task(watchdog())

    try:
        while True:
            message = await websocket.receive()
            last_activity = asyncio.get_event_loop().time()  # Reset on any msg

            if message.get("bytes"):
                audio = np.frombuffer(message["bytes"], dtype=np.float32)
                audio_buffer.append(audio)
                # NEW: Log more details for debug
                print(
                    "[LIVE CHAT] Audio chunk received | Length: "
                    f"{len(audio)} | Max amp: {np.max(np.abs(audio)):.4f} | "
                    f"Buffer size: {len(audio_buffer)}"
                )
                continue

            if message.get("text") == "STOP":
                if not audio_buffer:
                    print("[LIVE CHAT] No audio to process")
                    # NEW: Send status to frontend
                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "STATUS",
                                "content": "No speech detected. Try speaking again.",
                            }
                        )
                    )
                    continue

                audio_np = np.concatenate(audio_buffer)
                # NEW: Check if audio is silent (debug)
                max_amp = np.max(np.abs(audio_np))
                print(
                    "[LIVE CHAT] Processing audio | Total length: "
                    f"{len(audio_np)} | Max amp: {max_amp:.4f}"
                )
                if max_amp < 0.001:  # Too silent? Skip or handle
                    print("[LIVE CHAT] Audio too silent, skipping")
                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "STATUS",
                                "content": "Audio too quiet. Check mic volume.",
                            }
                        )
                    )
                    audio_buffer.clear()
                    continue

                text = await transcribe_audio(audio_np)
                print("[LIVE CHAT] Transcript:", text)

                if not text:
                    print("[LIVE CHAT] Empty transcript, skipping")
                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "STATUS",
                                "content": "No speech detected in audio.",
                            }
                        )
                    )
                    audio_buffer.clear()
                    continue

                await websocket.send_text(
                    json.dumps({"type": "USER_TRANSCRIPT", "content": text})
                )

                state["messages"].append({"role": "user", "content": text})
                output = await graph_app.ainvoke(state)
                state.update(output)

                if state.get("agent_response"):
                    await websocket.send_text(
                        json.dumps({"type": "CHAT", "content": state["agent_response"]})
                    )

                if state.get("navigate"):
                    await websocket.send_text(
                        json.dumps({"navigate": state["navigate"]})
                    )

                state.pop("agent_response", None)
                state.pop("navigate", None)

                # NEW: Send resume status
                await websocket.send_text(
                    json.dumps({"type": "STATUS", "content": "Listening again..."})
                )

                audio_buffer.clear()  # Explicit clear

    except Exception as e:
        print("[LIVE CHAT ERROR]", e)

    finally:
        watchdog_task.cancel()
        print("[LIVE CHAT] Disconnected")
