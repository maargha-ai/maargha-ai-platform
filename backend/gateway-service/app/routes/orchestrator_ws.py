from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
import asyncio
import websockets
from app.config import settings
import traceback

router = APIRouter()

@router.websocket("/ws/chat")
async def orchestrator_ws(
    websocket: WebSocket,
    token: str = Query(...)
):
    print("\n[Gateway] WS connection attempt")

    await websocket.accept()
    print("[Gateway] Frontend WS accepted")

    # Decode JWT
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = payload.get("user_id")
        print("[Gateway] JWT decoded, user_id =", user_id)

        if not user_id:
            raise JWTError("user_id missing")

    except Exception as e:
        print("[Gateway] JWT ERROR:", e)
        traceback.print_exc()
        await websocket.close(code=1008)
        return

    # Build orchestrator WS URL
    orchestrator_ws_url = f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/{user_id}"
    print("[Gateway] Connecting to orchestrator:", orchestrator_ws_url)

    # Try connecting to orchestrator
    try:
        orch_ws = await websockets.connect(orchestrator_ws_url)
        print("[Gateway] Connected to orchestrator WS")

    except Exception as e:
        print("[Gateway] FAILED to connect to orchestrator WS")
        traceback.print_exc()
        await websocket.close()
        return

    try:
        async def frontend_to_orchestrator():
            while True:
                msg = await websocket.receive_text()
                print("[Gateway] Frontend → Orch:", msg)
                await orch_ws.send(msg)

        async def orchestrator_to_frontend():
            while True:
                msg = await orch_ws.recv()
                print("[Gateway] Orch → Frontend:", msg)
                await websocket.send_text(msg)

        # Parallel run (Full-duplex)
        await asyncio.gather(
            frontend_to_orchestrator(),
            orchestrator_to_frontend(),
        )

    except WebSocketDisconnect:
        print("[Gateway] Frontend disconnected")

    except Exception as e:
        print("[Gateway] WS runtime error")
        traceback.print_exc()

    finally:
        print("[Gateway] Closing orchestrator WS")
        await orch_ws.close()
