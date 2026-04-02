import httpx
from app.core.config import settings


async def detect_text_emotion(text: str) -> list[str]:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/emotion/detect-emotion",
                json={"text": text},
            )

            data = response.json()
            return data.get("emotions", ["Calm"])

    except Exception as e:
        print("[Emotion API ERROR]", e)
        return ["Calm"]