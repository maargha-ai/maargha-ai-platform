# Auth Routes
from fastapi import APIRouter, Request, Depends
from app.services.user_client import register_user, login_user, logout_user
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/")
async def register(payload: dict):
    logger.info("register_request")
    return await register_user(payload)

@router.post("/login/")
async def login(payload: dict):
    logger.info("login_request")
    return await login_user(payload)

@router.post("/logout")
async def logout(request: Request):
    body = await request.json()
    logger.info("logout_request")
    return await logout_user(
        body,
        request.headers.get("authorization")
    )
