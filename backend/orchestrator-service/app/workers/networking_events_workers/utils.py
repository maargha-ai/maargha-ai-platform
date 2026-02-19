from datetime import date, timedelta


def fallback_dates():
    start = date.today()
    end = start + timedelta(days=2)
    return start, end


def detect_mode(text: str) -> str:
    t = text.lower()
    if "online" in t:
        return "online"
    if "offline" in t or "in-person" in t:
        return "offline"
    return "hybrid"


def detect_tags(text: str) -> list:
    tags = []
    keywords = ["ai", "ml", "web3", "blockchain", "cloud", "data", "security"]

    t = text.lower()
    for k in keywords:
        if k in t:
            tags.append(k)

    return tags
