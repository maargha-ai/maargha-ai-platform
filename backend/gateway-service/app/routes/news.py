from fastapi import APIRouter
import httpx
from app.config import settings

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/latest")
async def proxy_news():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{settings.ORCHESTRATOR_SERVICE_URL}/news/latest"
        )
    return resp.json()
