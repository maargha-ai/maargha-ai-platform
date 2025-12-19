# In app/graph/orchestrator_graph.py
from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.graph.nodes import reasoning_node, action_node, observation_node

graph = StateGraph(AgentState)

graph.add_node("reason", reasoning_node.reasoning_node)
graph.add_node("act", action_node.action_node)
graph.add_node("observe", observation_node.observation_node)

graph.set_entry_point("reason")

graph.add_edge("reason", "act")
graph.add_edge("act", "observe")

graph.add_conditional_edges(
    "observe",
    lambda s: (
        "end"
        if s.get("agent_done") or s.get("agent_waiting_for_user")
        else "reason"
    ),
    {
        "reason": "reason",
        "end": END
    }
)

app = graph.compile()