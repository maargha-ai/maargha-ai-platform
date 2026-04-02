import json
import time

import numpy as np
from fastapi import WebSocket

from app.agents.emotional_support_agent import (
    detect_text_emotion,
    generate_response,
    transcribe_audio,
)

IGNORE_SECONDS_AFTER_REPLY = 3.0  # Increased wait time after AI speaks
MIN_AUDIO_DURATION = 2.0  # Minimum 2 seconds of audio
MIN_WORD_COUNT = 3  # Minimum 3 words required


async def emotional_support_ws(websocket: WebSocket, user_id: str):
    await websocket.accept()
    print(f"[EMO] Connected user {user_id}")

    audio_buffer = []
    ignore_until = 0.0  # 🔥 CRITICAL

    try:
        while True:
            message = await websocket.receive()

            now = time.time()
            if now < ignore_until:
                continue  # 🚫 HARD IGNORE WINDOW

            # STOP SIGNAL
            if message.get("text") == "STOP":
                if not audio_buffer:
                    continue

                full_audio = np.concatenate(audio_buffer)
                audio_buffer.clear()

                # 🔒 AUDIO DURATION GUARD - Must be at least 2 seconds
                audio_duration = len(full_audio) / 16000  # 16kHz sample rate
                if audio_duration < MIN_AUDIO_DURATION:
                    print(f"[EMO] Audio too short: {audio_duration:.2f}s < {MIN_AUDIO_DURATION}s")
                    continue

                text = await transcribe_audio(full_audio)

                # 🔒 WORD COUNT VALIDATION - Must have minimum words
                words = text.strip().split()
                if len(words) < MIN_WORD_COUNT:
                    print(f"[EMO] Too few words: {len(words)} < {MIN_WORD_COUNT} - '{text}'")
                    continue

                # 🔒 BACKGROUND NOISE FILTER - Check if it's just noise or filler
                noise_indicators = {
                    "thank you", "thanks", "okay", "ok", "yes", "no", "um", "uh", "yeah", 
                    "hmm", "alright", "sure", "cool", "nice", "good", "great", "fine"
                }
                
                # Only filter if ALL words are noise indicators
                if all(word.lower() in noise_indicators for word in words):
                    print(f"[EMO] Background noise detected: '{text}'")
                    continue

                # SEND USER TEXT
                await websocket.send_text(
                    json.dumps({"type": "user_text", "text": text})
                )

                emotion = detect_text_emotion(text)
                reply = generate_response(text, emotion)

                # SEND AGENT REPLY
                await websocket.send_text(
                    json.dumps(
                        {"type": "agent_reply", "text": reply, "emotion": emotion}
                    )
                )

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
