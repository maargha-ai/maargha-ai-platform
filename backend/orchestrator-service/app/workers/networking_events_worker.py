import re
from playwright.sync_api import sync_playwright

def scrape_devpost():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        page.goto(
            "https://devpost.com/hackathons?challenge_type=in-person&sort_by=upcoming",
            timeout=60000
        )
        page.wait_for_load_state("networkidle")

        for _ in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1500)

        cards = page.query_selector_all("a.flex-row.tile-anchor")

        events = []

        for card in cards:
            try:
                text = card.inner_text()
                href = card.get_attribute("href")

                clean_url = re.sub(r"\?.*", "", href)
                url = f"https://devpost.com{clean_url}"

                events.append({
                    "title": text.split("\n")[0].strip(),
                    "mode": "Online" if "Online" in text else "In-person",
                    "type": "Hackathon",
                    "registration_url": url
                })
            except:
                continue

        browser.close()
        return events
