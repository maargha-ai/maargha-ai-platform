from fastapi import APIRouter
from app.workers.tech_news_worker import scrape_tech_news

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/latest")
async def get_latest_news():
    news = scrape_tech_news()
    return {
        "count": len(news),
        "articles": news
    }
