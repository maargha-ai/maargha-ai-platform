import asyncio
import traceback
from typing import Dict

import websockets
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt

from app.config import settings

router = APIRouter()

# Global registry: user_id -> active text chat WebSocket (or None)
active_text_chats: Dict[str, WebSocket] = (
    {}
)  # thread-safe enough for async with proper locking if needed


@router.websocket("/ws/chat")
async def orchestrator_ws(websocket: WebSocket, token: str = Query(...)):
    print("[Gateway] Text WS connection attempt")

    await websocket.accept()
    print("[Gateway] Frontend text WS accepted")

    user_id = None

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

    # Register this connection
    old_ws = active_text_chats.get(user_id)
    if old_ws is not None:
        print(f"[Gateway] Closing old text WS for user {user_id}")
        try:
            await old_ws.close(code=1000)  # normal closure
        except Exception:
            pass

    active_text_chats[user_id] = websocket

    # Build orchestrator WS URL
    orchestrator_ws_url = f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/chat"
    print("[Gateway] Connecting to orchestrator:", orchestrator_ws_url)

    try:
        orch_ws = await websockets.connect(orchestrator_ws_url)
        print("[Gateway] Connected to orchestrator WS")
    except Exception:
        print("[Gateway] FAILED to connect to orchestrator WS")
        traceback.print_exc()
        await websocket.close()
        return

    try:

        async def frontend_to_orchestrator():
            try:
                while True:
                    message = await websocket.receive()
                    print(f"[Gateway Text] Message: {message}")

                    if message["type"] == "websocket.disconnect":
                        await orch_ws.close()
                        break

                    if message.get("bytes") is not None:
                        print("[Gateway Text] -> Orch AUDIO")
                        await orch_ws.send(message["bytes"])
                    elif message.get("text") is not None:
                        print("[Gateway Text] -> Orch TEXT:", message["text"])
                        await orch_ws.send(message["text"])

            except Exception as e:
                print("[Gateway Text] frontend_to_orchestrator error", e)
                await orch_ws.close()

        async def orchestrator_to_frontend():
            try:
                while True:
                    msg = await orch_ws.recv()
                    print("[Gateway Text] Orch -> Frontend:", msg)
                    await websocket.send_text(msg)
            except Exception:
                pass

        await asyncio.gather(
            frontend_to_orchestrator(),
            orchestrator_to_frontend(),
        )

    except WebSocketDisconnect:
        print("[Gateway Text] Frontend disconnected")

    except Exception:
        print("[Gateway Text] WS runtime error")
        traceback.print_exc()

    finally:
        print("[Gateway Text] Cleaning up")
        await orch_ws.close()
        # Remove from registry if it's still us
        if active_text_chats.get(user_id) is websocket:
            del active_text_chats[user_id]
            print(f"[Gateway] Removed text WS for user {user_id} from registry")


@router.websocket("/ws/chat/live")
async def orchestrator_chat_live(websocket: WebSocket, token: str = Query(...)):
    print("[Gateway] Live WS connection attempt")

    await websocket.accept()

    user_id = None

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("user_id")
        print("[Gateway Live] JWT decoded, user_id =", user_id)

        if not user_id:
            await websocket.close(code=1008)
            return

    except Exception:
        await websocket.close(code=1008)
        return

    # NEW: Disconnect any existing text chat for this user
    if user_id in active_text_chats:
        old_ws = active_text_chats[user_id]
        print(f"[Gateway Live] Closing existing text chat WS for user {user_id}")
        try:
            await old_ws.close(code=1000, reason="Switched to live voice mode")
        except Exception as e:
            print("[Gateway Live] Error closing old text WS:", e)
        # Remove it (even if close failed)
        del active_text_chats[user_id]

    # Connect to orchestrator live endpoint
    try:
        orch_ws = await websockets.connect(
            f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/ws/chat/live"
        )
        print("[Gateway Live] Connected to orchestrator live WS")
    except Exception as e:
        print("[Gateway Live] Failed to connect to orchestrator:", e)
        await websocket.close()
        return

    async def frontend_to_orch():
        try:
            while True:
                try:
                    msg = await websocket.receive()
                except RuntimeError as e:
                    if "disconnect message has been received" in str(e):
                        print(
                            "[Gateway Live] Frontend already disconnected "
                            "- stopping forward"
                        )
                        break
                    raise

                if msg.get("bytes"):
                    await orch_ws.send(msg["bytes"])
                elif msg.get("text"):
                    await orch_ws.send(msg["text"])

        except WebSocketDisconnect:
            print("[Gateway Live] Frontend disconnected (WebSocketDisconnect)")
        except Exception as e:
            print("[Gateway Live] frontend_to_orch error:", e)
        finally:
            try:
                await orch_ws.close()
            except Exception:
                pass

    async def orch_to_frontend():
        try:
            while True:
                try:
                    msg = await orch_ws.recv()
                    await websocket.send_text(msg)
                except websockets.exceptions.ConnectionClosed:
                    print("[Gateway Live] Orchestrator closed connection")
                    break
                except Exception as e:
                    print("[Gateway Live] orch_to_frontend error:", e)
                    break
        except Exception as e:
            print("[Gateway Live] orch_to_frontend outer error:", e)

    try:
        await asyncio.gather(
            frontend_to_orch(), orch_to_frontend(), return_exceptions=True
        )
    finally:
        try:
            await orch_ws.close()
        except Exception:
            pass
        # try:
        #     await websocket.close()
        # except:
        #     pass
