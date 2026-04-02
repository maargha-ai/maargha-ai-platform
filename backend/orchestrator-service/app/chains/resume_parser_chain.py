# orchestrator-service/app/chains/resume_parser_chain.py

from typing import Dict, List
import httpx
from app.core.config import settings

async def extract_resume_entities(text: str):
    timeout = httpx.Timeout(60.0, connect=10.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}parse-resume",
                json={"text": text},
            )

            response.raise_for_status()
            data = response.json()

            return data.get("entities", {})

    except httpx.ReadTimeout:
        return {"error": "ML service timeout"}