from app.core.state import AgentState
import asyncio
from app.workers.networking_events_worker import scrape_devpost

async def networking_events_tool(state: AgentState):
    if state.get("events_completed"):
        return {}

    events = await asyncio.to_thread(scrape_devpost)

    return {
        "tool_result": {
            "type": "networking_events",
            "events": events[:20]
        },
        "events_completed": True
    }
