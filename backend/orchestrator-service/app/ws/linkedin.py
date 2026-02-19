import json

from fastapi import WebSocket

from app.chains.linkedin_chain import run_linkedin_assistant


async def linkedin_ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()

    while True:
        msg = json.loads(await websocket.receive_text())

        if msg["type"] == "linkedin_message":
            user_text = msg["message"]

            reply = await run_linkedin_assistant(user_text)

            await websocket.send_text(
                json.dumps({"type": "linkedin_reply", "message": reply})
            )
