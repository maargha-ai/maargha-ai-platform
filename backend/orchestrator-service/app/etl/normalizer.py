import uuid
from app.etl.classifer import classify_event_type
from datetime import datetime

def normalize_event(raw):
    event_type = classify_event_type(
        raw["raw_title"] + " " + raw["raw_description"]
    )

    start_date = datetime.strptime(raw["start_date"], "%Y-%m-%d")

    return {
        "event_id": str(uuid.uuid4()),
        "title": raw["raw_title"],
        "event_type": event_type,
        "mode": "online" if "online" in raw["raw_description"].lower() else "offline",
        "start_date": start_date,
        "end_date": start_date,
        "location": raw["raw_location"],
        "platform": raw["source"],
        "registration_url": raw["url"],
        "tags": [],
        "scraped_at": raw["scraped_at"]
    }
