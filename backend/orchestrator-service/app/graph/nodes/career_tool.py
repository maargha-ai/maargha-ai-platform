# app/graph/nodes/career_tool.py
from app.core.state import AgentState
from app.chains.career_chain import QUESTIONS, predict_careers_from_answers

async def career_tool(state: AgentState):
    if state.get("career_options"):
        return {}
    
    answers = state.get("career_answers", {})
    question_idx = state.get("career_question_idx", 0)

    if question_idx is None:
        return {
            "agent_observation": "Career quiz is not active.",
            "agent_waiting_for_user": True
        }
    
    # If all questions answered → predict careers
    if question_idx >= len(QUESTIONS):
        careers = await predict_careers_from_answers(answers)
        return {
            "tool_result": {
                "type": "career_result",
                "careers": careers
            }
        }

    return {
        "tool_result": {
            "type": "career_question",
            "question": QUESTIONS[question_idx],
            "next_idx": question_idx + 1
        }
    }