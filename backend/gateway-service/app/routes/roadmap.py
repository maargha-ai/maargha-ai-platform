from fastapi import APIRouter, Request
from app.utils.http import post
from app.config import settings

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.post("/generate")
async def proxy_roadmap(req: Request):
    return await post(
        url=f"{settings.ORCHESTRATOR_SERVICE_WS_URL}/roadmap/generate",
        json=await req.json(),
        headers={
            "Authorization": req.headers.get("authorization")
        }
    )
