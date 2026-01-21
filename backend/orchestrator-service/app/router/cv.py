from fastapi import APIRouter
from app.chains.cv_chain import CVInput, generate_cv

router = APIRouter(prefix="/cv", tags=["CV Generator"])

@router.post("/generate")
async def generate_cv_endpoint(payload: CVInput):
    cv_text = await generate_cv(payload)
    return {
        "status": "success",
        "cv": cv_text
    }
