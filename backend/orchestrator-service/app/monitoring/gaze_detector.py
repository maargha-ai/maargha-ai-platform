import httpx
from app.core.config import settings

async def is_looking_away(frame_b64: str) -> bool:
    """
    Calls ML service instead of running mediapipe locally
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}detect-malpractice",
                json={"frame": frame_b64},
            )

        if response.status_code == 200:
            return response.json().get("result", False)

        return False

    except Exception as e:
        print(f"ML service error: {e}")
        return False