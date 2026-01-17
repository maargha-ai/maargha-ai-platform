import re
from playwright.sync_api import sync_playwright
from .utils import fallback_dates, detect_mode, detect_tags

def scrape_devpost():
    events = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://devpost.com/hackathons", timeout=60000)
        page.wait_for_load_state("networkidle")

        for _ in range(8):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1200)

        cards = page.query_selector_all("a.flex-row.tile-anchor")

        for card in cards:
            try:
                text = card.inner_text()
                href = card.get_attribute("href")

                start_date, end_date = fallback_dates()

                events.append({
                    "title": text.split("\n")[0].strip(),
                    "event_type": "hackathon",
                    "mode": detect_mode(text),
                    "platform": "devpost",
                    "registration_url": f"https://devpost.com{re.sub(r'\\?.*', '', href)}",
                    "start_date": start_date,
                    "end_date": end_date,
                    "location": "Online" if "online" in text.lower() else "In-person",
                    "tags": detect_tags(text)
                })
            except Exception:
                continue

        browser.close()

    return events
