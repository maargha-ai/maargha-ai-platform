# Auth Routes
from fastapi import APIRouter, Request, Depends
from app.services.user_client import register_user, login_user, logout_user
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/")
async def register(payload: dict):
    return await register_user(payload)

@router.post("/login/")
async def login(payload: dict):
    return await login_user(payload)

@router.post("/logout")
async def logout(request: Request):
    body = await request.json()
    return await logout_user(
        body,
        request.headers.get("authorization")
    )
