from fastapi import APIRouter, Request

from app.config import settings
from app.core.logger import logger
from app.utils.http import post

router = APIRouter(prefix="/music", tags=["Music"])


@router.post("/recommend")
async def proxy_music(req: Request):
    logger.info("song_recommendation_connected")
    return await post(
        url=f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/music/recommend",
        json=await req.json(),
        headers={"Authorization": req.headers.get("authorization")},
    )
