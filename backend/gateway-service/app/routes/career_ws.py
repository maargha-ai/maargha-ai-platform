from fastapi import APIRouter, WebSocket, Query
from jose import jwt
import websockets
import asyncio
from app.config import settings

router = APIRouter()

@router.websocket("/ws/career")
async def career_ws(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()
    print("\n[Gateway] career connection")
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    user_id = payload["user_id"]

    orch_ws_url = f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/career/{user_id}"
    orch_ws = await websockets.connect(orch_ws_url)

    async def frontend_to_backend():
        while True:
            msg = await websocket.receive_text()
            await orch_ws.send(msg)

    async def backend_to_frontend():
        while True:
            msg = await orch_ws.recv()
            await websocket.send_text(msg)

    await asyncio.gather(frontend_to_backend(), backend_to_frontend())
