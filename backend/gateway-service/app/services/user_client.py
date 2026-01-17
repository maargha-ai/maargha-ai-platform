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
        f"{settings.USER_SERVICE_URL}/auth/login/",
        json=data
    )

async def logout_user(data: dict, auth_header: str):
    return await post(
        f"{settings.USER_SERVICE_URL}/auth/logout/",
        headers={
            "Authorization": auth_header,
        },
        json={
            "refresh": data.get("refresh")
        }
    )