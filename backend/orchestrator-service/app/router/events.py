from fastapi import APIRouter

from app.db.database import SessionLocal
from app.models.event import Event

router = APIRouter()


@router.get("/events")
def get_events():
    db = SessionLocal()
    events = db.query(Event).limit(100).all()
    db.close()
    return events
