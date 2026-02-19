# app/intent/intent_router.py
import json
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm_client import llm

IntentType = Literal[
    "career_guidance",
    "roadmap_generation",
    "job_search",
    "linkedin_assistant",
    "quiz_section",
    "tech_news",
    "emotional_support",
    "general_chat",
    "unknown",
]

INTENT_PROMPT = """
Classify the user's message into ONE intent.

Intents:
- career_guidance
- roadmap_generation
- job_search
- linkedin_assistant
- quiz_section
- tech_news
- emotional_support
- general_chat
- unknown

Message:
"{message}"

Reply ONLY as JSON:
{{ "intent": "<intent>" }}
"""


async def route_intent(message: str) -> IntentType:
    response = await llm.ainvoke(
        [
            SystemMessage(content="You are an intent classifier."),
            HumanMessage(content=INTENT_PROMPT.format(message=message)),
        ]
    )

    try:
        return json.loads(response.content).get("intent", "unknown")
    except Exception:
        return "unknown"
