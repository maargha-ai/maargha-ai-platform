# orchestrator-service/app/workers/job_scraper_worker.py

import httpx
from app.core.config import settings


async def scrape_jobs(query: str, location: str, max_jobs: int = 200):
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.SCRAPER_SERVICE_URL}scrape-jobs",
                json={
                    "query": query,
                    "location": location,
                    "max_jobs": max_jobs,
                },
            )
            response.raise_for_status()
            return response.json()["jobs"]

    except Exception as e:
        print(f"Scraper service failed: {e}")
        return []