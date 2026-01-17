import asyncio
from app.workers.networking_events_workers.devpost_scraper import scrape_devpost
from app.workers.networking_events_workers.devfolio_scraper import scrape_devfolio
from app.workers.networking_events_workers.twitter_scraper import scrape_twitter
from app.models.event import Event
from app.db.database import AsyncSessionLocal


async def run():
    # 1. Run sync scrapers safely in threads
    devpost_events = await asyncio.to_thread(scrape_devpost)
    devfolio_events = await asyncio.to_thread(scrape_devfolio)
    twitter_events = await asyncio.to_thread(scrape_twitter)

    all_events = devpost_events + devfolio_events + twitter_events

    # 2. Async DB write
    async with AsyncSessionLocal() as db:
        for event in all_events:
            try:
                db.add(Event(**event))
            except Exception as e:
                print("Add failed:", e)

        try:
            await db.commit()
        except Exception as e:
            print("Commit failed:", e)
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(run())
