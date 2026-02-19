# app/db/models.py
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from app.db.database import Base


class Career(Base):
    __tablename__ = "careers"

    user_id = Column(String, primary_key=True, index=True)
    selected_career = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())