# app/crud/career.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.career import Career

async def get_user_career(db: AsyncSession, user_id: str) -> str | None:
    result = await db.execute(select(Career.selected_career).where(Career.user_id == user_id))
    return result.scalar_one_or_none()

async def save_user_career(db: AsyncSession, user_id: str, career: str):
    stmt = update(Career).where(Career.user_id == user_id).values(selected_career=career)
    await db.execute(stmt)
    
    # If user doesn't exist → insert
    result = await db.execute(select(Career.user_id).where(Career.user_id == user_id))
    if not result.scalar_one_or_none():
        new_user = Career(user_id=user_id, selected_career=career)
        db.add(new_user)
    await db.commit()