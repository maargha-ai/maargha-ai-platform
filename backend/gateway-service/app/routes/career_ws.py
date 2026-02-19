import asyncio

import websockets
from fastapi import APIRouter, Query, WebSocket
from jose import jwt

from app.config import settings
from app.core.logger import logger

router = APIRouter()


@router.websocket("/ws/career")
async def career_ws(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()
    logger.info("career_ws_connected")

    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    user_id = payload["user_id"]

    logger.info("career_ws_authenticated", user_id=user_id)

    orch_ws = await websockets.connect(
        f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/career/{user_id}"
    )

    async def frontend_to_backend():
        while True:
            msg = await websocket.receive_text()
            logger.debug("career_ws_forward_to_orch")
            await orch_ws.send(msg)

    async def backend_to_frontend():
        while True:
            msg = await orch_ws.recv()
            logger.debug("career_ws_forward_to_client")
            await websocket.send_text(msg)

    await asyncio.gather(frontend_to_backend(), backend_to_frontend())
