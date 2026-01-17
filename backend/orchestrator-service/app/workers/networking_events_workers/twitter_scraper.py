from .utils import fallback_dates, detect_tags

KEYWORDS = ["hackathon", "ideathon", "conference", "meetup", "seminar"]

def scrape_twitter():
    events = []

    for k in KEYWORDS:
        start_date, end_date = fallback_dates()

        events.append({
            "title": f"{k.capitalize()} announced on X",
            "event_type": k,
            "mode": "online",
            "platform": "twitter",
            "registration_url": "https://x.com",
            "start_date": start_date,
            "end_date": end_date,
            "location": "",
            "tags": detect_tags(k)
        })

    return events
