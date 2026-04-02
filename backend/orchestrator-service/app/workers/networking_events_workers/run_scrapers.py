import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import AsyncSessionLocal
from app.models.event import Event
from app.workers.networking_events_workers.devpost_scraper import fetch_devpost_events

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("event_refresh")


async def run():
    logger.info("Starting daily event refresh job...")

    # -------- Fetch events --------
    try:
        devpost_events = await asyncio.to_thread(fetch_devpost_events)
        logger.info(f"Fetched {len(devpost_events)} events")
    except Exception:
        logger.exception("Failed to fetch events")
        return

    if not devpost_events:
        logger.warning("No events fetched — skipping DB update")
        return

    # -------- Update DB --------
    async with AsyncSessionLocal() as db:
        try:
            logger.info("Clearing old events...")
            await db.execute(text("TRUNCATE TABLE events RESTART IDENTITY"))
            await db.commit()

            logger.info("Inserting new events...")
            await db.execute(Event.__table__.insert(), devpost_events)
            await db.commit()

            logger.info("Event refresh completed successfully!")

        except SQLAlchemyError:
            logger.exception("Database error — rollback")
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(run())
