# HTTP Client Helper
import httpx


async def post(url: str, json: dict, headers: dict | None = None):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
