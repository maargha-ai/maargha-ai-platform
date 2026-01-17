from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.chains.roadmap_chain import generate_roadmap_video

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

class RoadmapRequest(BaseModel):
    career: str

class RoadmapResponse(BaseModel):
    video_url: str

@router.post("/generate", response_model=RoadmapResponse)
async def generate_roadmap(req: RoadmapRequest):
    video_url = await generate_roadmap_video(req.career)

    return {
        "video_url": video_url
    }
