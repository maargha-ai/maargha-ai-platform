import httpx
from fastapi import APIRouter, Request

from app.config import settings
from app.core.logger import logger

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/match")
async def proxy_job_match(req: Request):
    body = await req.body()
    logger.info("jobs_match_request")

    headers = {
        "Authorization": req.headers.get("authorization"),
        "Content-Type": req.headers.get("content-type"),
    }

    async with httpx.AsyncClient(timeout=300) as client:
        resp = await client.post(
            f"{settings.ORCHESTRATOR_SERVICE_URL}/jobs/match",
            content=body,
            headers=headers,
        )

    logger.info("jobs_match_response", status_code=resp.status_code)
    return resp.json()
