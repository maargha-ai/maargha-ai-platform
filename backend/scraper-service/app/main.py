# scraper-service/app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from app.job_scraper import scrape_jobs_sync

app = FastAPI()


class ScrapeRequest(BaseModel):
    query: str
    location: str
    max_jobs: int = 200


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scrape-jobs")
def scrape_jobs(req: ScrapeRequest):
    jobs = scrape_jobs_sync(req.query, req.location, req.max_jobs)
    return {"jobs": jobs}