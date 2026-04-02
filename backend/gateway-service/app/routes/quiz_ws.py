import asyncio

import websockets
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from jose import jwt

from app.config import settings

router = APIRouter()


@router.websocket("/ws/quiz")
async def quiz_ws(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()

    # JWT validation (same as orchestrator_ws)
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    user_id = payload["user_id"]

    quiz_ws_url = f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/quiz/{user_id}"
    orch_ws = await websockets.connect(quiz_ws_url)

    async def frontend_to_backend():
        try:
            while True:
                msg = await websocket.receive_text()
                await orch_ws.send(msg)
        except WebSocketDisconnect:
            return
        except Exception:
            return

    async def backend_to_frontend():
        try:
            while True:
                msg = await orch_ws.recv()
                await websocket.send_text(msg)
        except Exception:
            return

    t1 = asyncio.create_task(frontend_to_backend())
    t2 = asyncio.create_task(backend_to_frontend())

    pending = await asyncio.wait({t1, t2}, return_when=asyncio.FIRST_COMPLETED)
    for t in pending:
        t.cancel()

    try:
        await orch_ws.close()
    except Exception:
        pass
