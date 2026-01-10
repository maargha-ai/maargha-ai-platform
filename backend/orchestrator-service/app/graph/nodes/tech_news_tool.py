from app.core.state import AgentState
import asyncio
from app.workers.tech_news_worker import scrape_tech_news

async def tech_news_tool(state: AgentState):
    if state.get("tech_news_completed"):
        return {}

    news = await asyncio.to_thread(scrape_tech_news)

    if not news:
        return {
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": "I couldn’t fetch tech news right now. Please try again later."
            }],
            "type": "tech_news",
            "agent_waiting_for_user": True
        }

    formatted = "\n\n".join(
        f"• {n['title']}\n  🔗 {n['link']}"
        for n in news[:10]
    )

    return {
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": f"📰 **Latest Tech News**\n\n{formatted}"
        }],
        "type": "tech_news",
        "tech_news_completed": True,
        "agent_waiting_for_user": True
    }
