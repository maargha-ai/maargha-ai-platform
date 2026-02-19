# app/router/jobs.py
import os
import tempfile

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.chains.jobs_chain import find_jobs_for_cv

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/match")
async def match_jobs(
    role: str = Form(...), location: str = Form(...), cv: UploadFile = File(...)
):
    # Save CV temporarily
    suffix = ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await cv.read()
        tmp.write(content)
        cv_path = tmp.name

    try:
        results = await find_jobs_for_cv(cv_path=cv_path, role=role, location=location)

        formatted = [
            {
                "score": float(score),
                "title": job["title"],
                "company": job["company"],
                "link": job["link"],
                "desc": job.get("desc", ""),
                "source": job["source"],
            }
            for score, job in results
        ]

        return {"count": len(formatted), "jobs": formatted}

    finally:
        if os.path.exists(cv_path):
            os.remove(cv_path)
