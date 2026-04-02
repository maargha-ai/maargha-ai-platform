import httpx
from fastapi import APIRouter

from app.config import settings
from app.core.logger import logger

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/latest")
async def proxy_news():
    logger.info("news_request_started")

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{settings.ORCHESTRATOR_SERVICE_URL}/news/latest")

    logger.info("news_request_completed", status=resp.status_code)
    return resp.json()
