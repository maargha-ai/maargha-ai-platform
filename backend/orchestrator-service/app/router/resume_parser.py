from fastapi import APIRouter, File, UploadFile

from app.chains.resume_parser_chain import extract_resume_entities
from app.utils.pdf_reader import extract_text_from_pdf

router = APIRouter(prefix="/resume", tags=["Resume Parsing"])


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    entities = extract_resume_entities(text)

    return {"status": "success", "entities": entities}
