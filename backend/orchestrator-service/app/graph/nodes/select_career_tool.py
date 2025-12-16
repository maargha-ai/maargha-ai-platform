# app/graph/nodes/select_career_tool.py
from app.core.state import AgentState
from app.crud.career import save_user_career
from app.db.database import get_db

async def select_career_tool(state: AgentState):
    career = state["agent_action_input"]["career"]
    user_id = state["user_id"]

    async for db in get_db():
        await save_user_career(db, user_id, career)

    return {
        "selected_career": career,

        # 🔴 CLEAR CAREER FLOW STATE
        "career_options": None,
        "career_answers": None,
        "career_question_idx": None,

        # Tell agent to stop looping
        "agent_waiting_for_user": True,

        # Message to user
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": (
                f"I've saved **{career}** as your career path.\n\n"
                "What would you like to do next?\n"
                "• Generate a roadmap\n"
                "• Find jobs\n"
                "• Change career"
            )
        }]
    }
