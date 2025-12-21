from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import httpx
from jose import jwt, JWTError
from app.config import settings
import asyncio

router = APIRouter()

@router.websocket("/ws/orchestrator")
async def orchestrator_ws(websocket: WebSocket):
    """
    WebSocket Gateway → Orchestrator WebSocket Proxy
    """

    # 1. Accept frontend WS
    await websocket.accept()

    # 2. Extract JWT from headers
    auth_header = websocket.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        await websocket.close(code=1008)
        return

    token = auth_header.split(" ")[1]

    # 3. Decode JWT
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = payload.get("user_id")
        if not user_id:
            raise JWTError("user_id missing")
    except JWTError:
        await websocket.close(code=1008)
        return

    # 4. Connect to orchestrator WS
    orchestrator_ws_url = (
        f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/{user_id}"
    )

    try:
        async with httpx.AsyncClient() as client:
            async with client.ws_connect(orchestrator_ws_url) as orchestrator_ws:

                async def frontend_to_orchestrator():
                    while True:
                        data = await websocket.receive_text()
                        await orchestrator_ws.send_text(data)

                async def orchestrator_to_frontend():
                    while True:
                        data = await orchestrator_ws.receive_text()
                        await websocket.send_text(data)

                # 5. Run both directions concurrently
                await httpx.AsyncClient().aclose()
                await asyncio.gather(
                    frontend_to_orchestrator(),
                    orchestrator_to_frontend(),
                )

    except WebSocketDisconnect:
        print("[Gateway] Frontend disconnected")
    except Exception as e:
        print("[Gateway] Error:", e)
        await websocket.close()
