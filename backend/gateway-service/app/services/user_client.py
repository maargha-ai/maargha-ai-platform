# User Service Client
from app.utils.http import post
from app.config import settings

async def register_user(data: dict):
    return await post(
        f"{settings.USER_SERVICE_URL}/auth/register/",
        json=data
    )

async def login_user(data: dict):
    return await post(
        f"{settings.USER_SERVICE_URL}/auth/login",
        json=data
    )