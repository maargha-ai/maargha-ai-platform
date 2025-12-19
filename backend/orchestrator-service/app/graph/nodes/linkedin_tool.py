# app/graph/nodes/linkedin_tool.py
from app.core.state import AgentState
from app.chains.linkedin_chain import run_linkedin_assistant

async def linkedin_tool(state: AgentState):
    user_message = state["agent_action_input"]["user_message"]

    response = await run_linkedin_assistant(user_message)

    return {
        "tool_result": {
            "type": "linkedin_response",
            "content": response
        },
        "linkedin_mode": True  # lock mode
    }
