from fastapi import WebSocket
import json
import numpy as np

from app.agents.emotional_support_agent import (
    transcribe_audio,
    detect_text_emotion,
    generate_response
)

import time

IGNORE_SECONDS_AFTER_REPLY = 2.0

async def emotional_support_ws(websocket: WebSocket, user_id: str):
    await websocket.accept()
    print(f"[EMO] Connected user {user_id}")

    audio_buffer = []
    ignore_until = 0.0   # 🔥 CRITICAL

    try:
        while True:
            message = await websocket.receive()

            now = time.time()
            if now < ignore_until:
                continue   # 🚫 HARD IGNORE WINDOW

            # STOP SIGNAL
            if message.get("text") == "STOP":
                if not audio_buffer:
                    continue

                full_audio = np.concatenate(audio_buffer)
                audio_buffer.clear()

                # 🔒 SHORT AUDIO GUARD
                if len(full_audio) < 16000:   # <1s
                    continue

                text = await transcribe_audio(full_audio)

                # 🔒 TEXT FILTER
                if not text or len(text) < 5:
                    continue

                if text.lower() in {
                    "thank you", "thanks", "okay", "yes", "no", "um",
                    "you're welcome", "how can i help you", "i'm here for you"
                }:
                    continue

                # SEND USER TEXT
                await websocket.send_text(json.dumps({
                    "type": "user_text",
                    "text": text
                }))

                emotion = detect_text_emotion(text)
                reply = generate_response(text, emotion)

                # SEND AGENT REPLY
                await websocket.send_text(json.dumps({
                    "type": "agent_reply",
                    "text": reply,
                    "emotion": emotion
                }))

                # 🔥 THIS IS THE KEY LINE
                ignore_until = time.time() + IGNORE_SECONDS_AFTER_REPLY

            # AUDIO CHUNK
            elif message.get("bytes") is not None:
                audio_chunk = np.frombuffer(message["bytes"], dtype=np.float32)
                audio_buffer.append(audio_chunk)

                print(f"Bytes: {len(audio_buffer)}")

    except Exception as e:
        print("[EMO WS ERROR]", e)

    finally:
        print(f"[EMO] Disconnected user {user_id}")
