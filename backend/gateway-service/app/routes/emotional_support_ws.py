from fastapi import APIRouter, WebSocket, Query
from jose import jwt
import websockets
import asyncio
from app.config import settings

router = APIRouter()

@router.websocket("/ws/emotional-support")
async def emotional_support_ws(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()
    print("\n[Gateway] emotional support connection")
    # ✅ JWT validation (same as quiz)
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    user_id = payload["user_id"]

    # 🔁 Connect to orchestrator WS
    orch_ws_url = f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/emotional-support/{user_id}"
    orch_ws = await websockets.connect(orch_ws_url)

    async def frontend_to_backend():
        try:
            while True:
                message = await websocket.receive()

                if message["type"] == "websocket.disconnect":
                    await orch_ws.close()
                    break

                if message.get("bytes") is not None:
                    await orch_ws.send(message["bytes"])

                elif message.get("text") is not None:
                    await orch_ws.send(message["text"])
        except Exception:
            await orch_ws.close()

    async def backend_to_frontend():
        try:
            while True:
                msg = await orch_ws.recv()
                print(f"[Gateway Emotion] message transcribed: {msg}")
                await websocket.send_text(msg)
        except Exception:
            pass

    await asyncio.gather(frontend_to_backend(), backend_to_frontend())
