# app/graph/nodes/action_node.py
from app.core.state import AgentState
from app.graph.nodes import career_tool, jobs_tool, roadmap_tool, select_career_tool, networking_events_tool, linkedin_tool, quiz_evaluator_tool, quiz_generator_tool

async def action_node(state: AgentState):
    print(f"\n[DEBUG action_node] Entering action_node with action[agent_action]: {state['agent_action']}, input [agent_action_input]: {state.get('agent_action_input')}")
    action = state["agent_action"]
    action_input = state.get("agent_action_input") or {}

    if action == "CareerPredictor":
        return await career_tool.career_tool(state)

    if action == "SelectCareer":
        return await select_career_tool.select_career_tool(state)

    if action == "JobSearch":
        state["job_role"] = action_input.get("job_role")
        state["job_location"] = action_input.get("job_location")
        # state["cv_path"] = action_input.get("cv_path") or state.get("cv_path")
    
        return await jobs_tool.jobs_tool(state)

    if action == "RoadmapGenerator":
        return await roadmap_tool.roadmap_tool(state)
    
    if action == "NetworkingEvents":
        return await networking_events_tool.networking_events_tool(state)

    if action == "LinkedInAssistant":
        return await linkedin_tool.linkedin_tool(state)

    elif action == "QuizGenerator":
        return await quiz_generator_tool.quiz_generator_tool(state)

    elif action == "QuizEvaluator":
        return await quiz_evaluator_tool.quiz_evaluator_tool(state)

    if action == "AskUser":
        # Safe extraction with fallback
        question = "Hello! How can I help you with your career today?"
        
        if isinstance(action_input, dict):
            question = action_input.get("message", question)
        
        return {
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": question
            }],
            "agent_waiting_for_user": True
        }

    if action == "DONE":
        return {"agent_done": True}
    
    return {}
