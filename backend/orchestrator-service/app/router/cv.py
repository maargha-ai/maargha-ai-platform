from fastapi import APIRouter, Response
from app.chains.cv_chain import CVInput, generate_cv
from app.utils.pdf_generator import cv_text_to_pdf

router = APIRouter(prefix="/cv", tags=["CV Generator"])


@router.post("/generate")
async def generate_cv_endpoint(payload: CVInput):
    cv_text = await generate_cv(payload)
    return {
        "status": "success",
        "cv": cv_text
    }


@router.post("/generate/pdf")
async def generate_cv_pdf(payload: CVInput):
    cv_text = await generate_cv(payload)
    pdf_bytes = cv_text_to_pdf(cv_text)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=generated_cv.pdf"
        }
    )


@router.post("/generate/pdf/download")
async def download_cv_pdf(payload: CVInput):
    cv_text = await generate_cv(payload)
    pdf_bytes = cv_text_to_pdf(cv_text)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=generated_cv.pdf"
        }
    )
