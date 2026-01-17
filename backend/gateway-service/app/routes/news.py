from fastapi import APIRouter
from app.utils.http import post
from app.config import settings

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/latest")
async def proxy_news():
    return await post(
        url=f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/news/latest"
    )
