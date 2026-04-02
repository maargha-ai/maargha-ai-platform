import requests
from app.core.config import settings


def get_embeddings(texts):
    try:
        response = requests.post(
            f"{settings.ML_SERVICE_URL}/embed",
            json={"texts": texts},
            timeout=30
        )
        return response.json()
    except Exception as e:
        print("ML embedding error:", e)
        return None