from fastapi import APIRouter
from pydantic import BaseModel

from app.chains.roadmap_chain import generate_roadmap

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


class RoadmapRequest(BaseModel):
    career: str


class RoadmapResponse(BaseModel):
    career: str
    steps: list


@router.post("/generate", response_model=RoadmapResponse)
async def generate(req: RoadmapRequest):
    roadmap = await generate_roadmap(req.career)
    return roadmap
