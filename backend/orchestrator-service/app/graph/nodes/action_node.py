# app/graph/nodes/action_node.py
from app.core.state import AgentState


async def action_node(state: AgentState):
    action = state.get("agent_action")

    print(
        f"[Action Node] Action: {state.get('agent_action')} | "
        f"Agent Response: {state.get('agent_response')}"
    )

    # CHAT → forward response
    if action == "CHAT":
        return {
            "agent_action": "CHAT",
            "agent_response": state.get("agent_response"),
            "agent_done": True,
        }

    # Tool navigation
    return {
        "navigate": {"tool": action, "payload": state.get("agent_action_input") or {}},
        "agent_done": True,
    }
