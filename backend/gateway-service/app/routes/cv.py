import httpx
from fastapi import APIRouter, Response

from app.config import settings

router = APIRouter(prefix="/cv", tags=["CV"])


@router.post("/generate")
async def generate_cv(payload: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        res = await client.post(
            f"{settings.ORCHESTRATOR_SERVICE_URL}/cv/generate", json=payload
        )
        return res.json()


@router.post("/generate/pdf")
async def generate_cv_pdf(payload: dict):
    async with httpx.AsyncClient(timeout=60) as client:
        res = await client.post(
            f"{settings.ORCHESTRATOR_SERVICE_URL}/cv/generate/pdf", json=payload
        )

        return Response(
            content=res.content, media_type="application/pdf", headers=res.headers
        )
