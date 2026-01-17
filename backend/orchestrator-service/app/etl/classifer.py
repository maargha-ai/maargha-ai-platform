def classify_event_type(text: str) -> str:
    t = text.lower()

    if "hackathon" in t:
        return "hackathon"
    if "ideathon" in t:
        return "ideathon"
    if "conference" in t:
        return "conference"
    if "meetup" in t:
        return "meetup"
    if "seminar" in t:
        return "seminar"

    return "other"
