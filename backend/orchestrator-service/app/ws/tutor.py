from fastapi import WebSocket
import json
from app.chains.tutor_chain import ask_tutor

async def tutor_ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()

    while True:
        msg = json.loads(await websocket.receive_text())

        if msg["type"] == "tutor_question":
            question = msg["question"]

            answer = await ask_tutor(question)

            await websocket.send_text(json.dumps({
                "type": "tutor_answer",
                "answer": answer
            }))
