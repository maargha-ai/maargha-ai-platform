from fastapi import APIRouter, Request
import httpx
from app.config import settings

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/match")
async def proxy_job_match(req: Request):
    body = await req.body()

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

    return resp.json()
