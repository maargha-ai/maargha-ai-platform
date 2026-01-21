# app/graph/nodes/reasoning_node.py
import json
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.llm_client import llm
from app.graph.nodes.intent_router import route_intent
from app.core.state import AgentState

SYSTEM_PROMPT = """
You are a conversational AI agent for a career platform.

You must decide ONE action:
- CHAT → if user is casually talking
- CareerPredictor
- RoadmapGenerator
- JobSearch
- LinkedInAssistant
- TechNews
- QuizGenerator
- MusicRecommender
- NetworkingEvents
- EmotionalSupport
- CVGeneration
- DONE

Rules:
- Default behavior is CHAT
- Use tools ONLY when clearly relevant
- Never explain your reasoning
- Output ONLY valid JSON

Format:
{
  "action": "<ACTION>",
  "action_input": {...} | null,
  "response": "<chat message if action=CHAT>"
}
"""

async def reasoning_node(state: AgentState):
    user_msg = state["messages"][-1]["content"]

    # Optional hint (NOT authority)
    intent_hint = await route_intent(user_msg)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
                    User message:
                    {user_msg}

                    Intent hint (may be wrong):
                    {intent_hint}

                    Decide next action.
                    """
                    )
                ]

    response = await llm.ainvoke(messages)

    try:
        plan = json.loads(response.content)
    except Exception:
        # Fallback to safe chat
        return {
            "agent_action": "CHAT",
            "agent_response": "I'm here 😊 How can I help you today?"
        }

    action = plan.get("action", "CHAT")

    if action == "CHAT":
        return {
            "agent_action": "CHAT",
            "agent_response": plan.get("response", "Got it 🙂")
        }
    return {
        "agent_action": action,
        "agent_action_input": plan.get("action_input") or {}
    }
