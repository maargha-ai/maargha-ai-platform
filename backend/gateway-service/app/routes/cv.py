from fastapi import APIRouter
import httpx
from app.config import settings

router = APIRouter(prefix="/cv", tags=["CV"])

@router.post("/generate")
async def generate_cv(payload: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.ORCHESTRATOR_SERVICE_URL}/cv/generate",
            json=payload
        )
        return response.json()
