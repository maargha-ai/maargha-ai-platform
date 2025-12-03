import asyncio
from playwright.async_api import async_playwright
import json
import re

async def scrape_devpost():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
            )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height':1080}
        )
        page = await context.new_page()
        
        print("Loading hackathons...")
        await page.goto("https://devpost.com/hackathons?challenge_type=in-person&sort_by=upcoming")
        await page.wait_for_load_state('networkidle')
        
        # Scroll to load ALL
        for i in range(10):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
        
        # Target the EXACT card structure we found
        cards = await page.query_selector_all('a.flex-row.tile-anchor')
        print(f"Found {len(cards)} hackathon cards")
        
        hackathons = []
        
        for i, card in enumerate(cards):
            try:
                # Get the FULL card content
                card_link = card
                href = await card_link.get_attribute('href')
                
                # Clean URL (remove tracking params)
                clean_url = re.sub(r'\?.*', '', href)
                hackathon_url = f"https://devpost.com{clean_url}" if clean_url.startswith('/') else clean_url
                
                # Get ALL text from the card
                full_text = await card_link.inner_text()
                
                # PARSE EACH FIELD using regex patterns
                data = {
                    "title": "",
                    "days_left": "",
                    "mode": "",
                    "prize_pool": "",
                    "participants": "",
                    "organizer": "",
                    "dates": "",
                    "tags": [],
                    "type": "Hackathon",
                    "registration_url": hackathon_url,
                    "hackathon_url": hackathon_url
                }
                
                title_match = re.search(r'^([^\n]+?)(?=\n\d+\s+days|\n\d+days)', full_text, re.MULTILINE)
                data["title"] = title_match.group(1).strip() if title_match else full_text.split('\n')[0].strip()
                
                days_match = re.search(r'(\d+\s+days?\s+left)', full_text)
                data["days_left"] = days_match.group(1) if days_match else ""
                
                if "Online" in full_text:
                    data["mode"] = "Online"
                elif "In-person" in full_text:
                    data["mode"] = "In-person"
                else:
                    data["mode"] = "Unknown"
                
                prize_match = re.search(r'\$[\d,]+(?:\.\d{2})?\s+in\s+prizes', full_text)
                data["prize_pool"] = prize_match.group(0) if prize_match else ""
                
                participants_match = re.search(r'(\d+(?:,\d+)?)\s+participants', full_text)
                data["participants"] = participants_match.group(1) if participants_match else "0"
                
                organizer_match = re.search(r'([^\n]+?)(?=\n(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d+-\d+))', full_text)
                data["organizer"] = organizer_match.group(1).strip() if organizer_match else ""
                
                date_match = re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?(?=\n[A-Z][a-z]+)', full_text)
                data["dates"] = date_match.group(0) if date_match else ""
                
                tag_lines = full_text.split('\n')[-3:]  # Last 3 lines are usually tags
                for line in tag_lines:
                    line = line.strip()
                    if '/' in line and len(line) < 20 and line not in data["tags"]:
                        data["tags"].append(line)
                
                hackathons.append(data)
                
                # Progress
                print(f"{i+1}: {data['title'][:40]}... | {data['mode']} | {data['prize_pool']}")
                
            except Exception as e:
                print(f"Error {i}: {e}")
                continue
        
        await browser.close()
        return hackathons

if __name__ == "__main__":
    hackathons = asyncio.run(scrape_devpost())
    print(f"\nFound {len(hackathons)} PERFECTLY STRUCTURED hackathons:")
    print(json.dumps(hackathons, indent=2))