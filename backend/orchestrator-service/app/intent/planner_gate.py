# app/intent/planner_gate.py
from app.core.state import AgentState
from app.intent.intent_router import IntentType

def should_enter_planner(intent: IntentType, state: AgentState) -> bool:
    # Ongoing structured flows MUST continue
    if state.get("career_question_idx") is not None:
        return True

    if state.get("career_options") and not state.get("selected_career"):
        return True

    if state.get("agent_waiting_for_user"):
        return False

    # Intents that require planning
    if intent in {
        "career_guidance",
        "roadmap_generation",
        "job_search",
        "cv_matching",
        "networking_events",
        "linkedin_assistant",
        "quiz_section",
        "emotional_support"
    }:
        return True

    return False
