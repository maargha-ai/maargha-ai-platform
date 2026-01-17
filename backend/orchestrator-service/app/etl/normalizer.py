import uuid
from app.etl.classifer import classify_event_type

def normalize_event(raw):
    event_type = classify_event_type(
        raw["raw_title"] + " " + raw["raw_description"]
    )

    return {
        "event_id": str(uuid.uuid4()),
        "title": raw["raw_title"],
        "event_type": event_type,
        "mode": "online" if "online" in raw["raw_description"].lower() else "offline",
        "start_date": None,
        "end_date": None,
        "location": raw["raw_location"],
        "platform": raw["source"],
        "registration_url": raw["url"],
        "tags": [],
        "scraped_at": raw["scraped_at"]
    }
