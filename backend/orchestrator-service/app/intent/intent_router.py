# app/intent/intent_router.py
import json
from typing import Literal
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.llm_client import llm 

IntentType = Literal[
    "career_guidance",
    "roadmap_generation",
    "job_search",
    "cv_matching",
    "networking_events",
    "linkedin_assistant"
    "emotional_support",
    "general_chat",
    "unknown"
]

INTENT_SYSTEM = """You classify user intent.
Reply ONLY with JSON.
"""

INTENT_SYSTEM_PROMPT = """
Classify the user's message into ONE category.

Categories:
- career_guidance
- roadmap_generation
- job_search
- cv_matching
- hackathons
- networking events
- tech meetups
- conferences
- dev events
- linkedin optimization
- grow linkedin
- emotional_support
- general_chat
- unknown

Message:
"{message}"

Respond ONLY with valid JSON:
{{ "intent": "<category>" }}
"""

async def route_intent(message: str) -> IntentType:
    response = await llm.ainvoke([
        SystemMessage(content=INTENT_SYSTEM),
        HumanMessage(content=INTENT_SYSTEM_PROMPT.format(message=message))
    ])

    try:
        data = json.loads(response.content)
        return data.get("intent", "unknown")
    except Exception:
        return "unknown"