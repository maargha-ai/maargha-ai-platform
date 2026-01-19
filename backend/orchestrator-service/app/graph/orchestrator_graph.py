# app/graph/orchestrator_graph.py
from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.graph.nodes.reasoning_node import reasoning_node
from app.graph.nodes.action_node import action_node

graph = StateGraph(AgentState)

graph.add_node("reason", reasoning_node)
graph.add_node("act", action_node)

graph.set_entry_point("reason")
graph.add_edge("reason", "act")
graph.add_edge("act", END)

app = graph.compile()
