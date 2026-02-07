from fastapi import APIRouter, WebSocket, Query
from jose import jwt
import websockets
import asyncio
from app.config import settings
from app.core.logger import logger

router = APIRouter()

@router.websocket("/ws/tutor")
async def tutor_ws(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()
    logger.info("tutor_ws_connected", user_id=user_id)

    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    user_id = payload["user_id"]

    orch_ws = await websockets.connect(
        f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/tutor/{user_id}"
    )

    async def frontend_to_backend():
        while True:
            msg = await websocket.receive_text()
            await orch_ws.send(msg)

    async def backend_to_frontend():
        while True:
            msg = await orch_ws.recv()
            await websocket.send_text(msg)

    await asyncio.gather(frontend_to_backend(), backend_to_frontend())
