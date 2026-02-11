from sqlalchemy import String, Date
from app.db.database import Base

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Event(Base):
    __tablename__ = "events"

    event_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    mode: Mapped[str] = mapped_column(String)
    platform: Mapped[str] = mapped_column(String)
    registration_url: Mapped[str] = mapped_column(String)
    start_date: Mapped[str] = mapped_column(Date, nullable=False)
    end_date: Mapped[str] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(String)
    tags: Mapped[list] = mapped_column(JSON, default=list)