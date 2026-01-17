from playwright.sync_api import sync_playwright
from .utils import fallback_dates, detect_mode, detect_tags

def scrape_devfolio():
    events = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://devfolio.co/hackathons", timeout=60000)
        page.wait_for_load_state("networkidle")

        cards = page.query_selector_all("a")

        for card in cards:
            try:
                title = card.inner_text()
                url = card.get_attribute("href")

                if not title or not url:
                    continue

                start_date, end_date = fallback_dates()
                event_type = "ideathon" if "ideathon" in title.lower() else "hackathon"

                events.append({
                    "title": title.strip(),
                    "event_type": event_type,
                    "mode": detect_mode(title),
                    "platform": "devfolio",
                    "registration_url": url,
                    "start_date": start_date,
                    "end_date": end_date,
                    "location": "",
                    "tags": detect_tags(title)
                })
            except Exception:
                continue

        browser.close()

    return events
