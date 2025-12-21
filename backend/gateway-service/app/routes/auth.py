# Auth Routes
from fastapi import APIRouter
from app.services.user_client import register_user, login_user

router = APIRouter(predix="/auth", tags=["auth"])

@router.post("/register")
async def register(payload: dict):
    return await register_user(payload)

@router.post("/login")
async def login(payload: dict):
    return await login_user(payload)