import requests
import time
from datetime import datetime

DEVPOST_API = "https://devpost.com/api/hackathons"

def parse_devpost_dates(date_text: str):
    """
    Returns proper datetime.date objects.
    """

    if not date_text:
        return None, None

    try:
        date_text = date_text.strip()

        # Case 1: Full range with two years
        if " - " in date_text and "," in date_text.split(" - ")[0]:
            start_str, end_str = date_text.split(" - ")

            start_date = datetime.strptime(
                start_str.strip(),
                "%b %d, %Y"
            ).date()

            end_date = datetime.strptime(
                end_str.strip(),
                "%b %d, %Y"
            ).date()

            return start_date, end_date

        # Case 2: Single year at end
        if " - " in date_text:
            start_part, end_part = date_text.split(" - ")
            year = end_part.split(",")[1].strip()

            start_date = datetime.strptime(
                f"{start_part.strip()} {year}",
                "%b %d %Y"
            ).date()

            end_clean = end_part.split(",")[0].strip()

            if " " not in end_clean:
                month = start_part.split()[0]
                end_clean = f"{month} {end_clean}"

            end_date = datetime.strptime(
                f"{end_clean} {year}",
                "%b %d %Y"
            ).date()

            return start_date, end_date

        # Case 3: Single date
        start_date = datetime.strptime(
            date_text.strip(),
            "%b %d, %Y"
        ).date()

        return start_date, None

    except Exception as e:
        print("Date parse failed:", date_text, "| Error:", e)
        return None, None

def fetch_devpost_events(status_list=None):
    if status_list is None:
        status_list = ["open", "upcoming"]

    all_events = []
    seen_urls = set()  # prevent duplicates

    for status in status_list:
        print(f"\nFetching status: {status}")

        page = 1

        while True:
            params = {
                "page": page,
                "status": status
            }

            response = requests.get(
                DEVPOST_API,
                params=params,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code != 200:
                print("Failed on page", page)
                break

            data = response.json()
            hackathons = data.get("hackathons", [])

            if not hackathons:
                print("No more pages for", status)
                break  # stops when empty page

            for hackathon in hackathons:
                url = hackathon.get("url")

                # Avoid duplicates between open + upcoming
                if url in seen_urls:
                    continue

                seen_urls.add(url)

                date_text = hackathon.get("submission_period_dates")
                start_date, end_date = parse_devpost_dates(date_text)

                displayed_location = hackathon.get("displayed_location", {})
                location = displayed_location.get("location")
                if location=="Online":
                    mode = "Online"
                else:
                    mode = "Offline"

                all_events.append({
                    "title": hackathon.get("title"),
                    "event_type": "hackathon",
                    "location": location,
                    "mode": mode,
                    "registration_url": url,
                    "start_date": start_date,
                    "end_date": end_date,
                    "tags": hackathon.get("themes"),
                })

            print(f"Fetched page {page} ({status}) — {len(hackathons)} events")

            page += 1
            time.sleep(0.5)  # polite delay

    return all_events


if __name__ == "__main__":
    events = fetch_devpost_events()

    print("\nTotal events fetched:", len(events))

    for e in events[:10]:
        print("-" * 40)
        print("Title:", e["title"])
        print("mode:", e["mode"])
        print("location:", e["location"])
        print("start_date:", e["start_date"])
        print("end_date:", e["end_date"])
        print("URL:", e["registration_url"])
