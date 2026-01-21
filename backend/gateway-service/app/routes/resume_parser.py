from fastapi import APIRouter, UploadFile, File
import httpx
from app.config import settings

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.ORCHESTRATOR_SERVICE_URL}/resume/parse",
            files={"file": (file.filename, await file.read(), "application/pdf")}
        )
        return response.json()
