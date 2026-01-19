# app/graph/nodes/observation_node.py
from app.core.state import AgentState

async def observation_node(state: AgentState):
    print(f"\n[DEBUG observation_node] Entering observation_node with state: {state}")
    updates = {}

    tool_result = state.get("tool_result")

    if not tool_result:
        return updates

    # Career Question
    if tool_result["type"] == "career_question":
        updates["ws_event"] = {
        "type": "NAVIGATE",
        "target": "career"
    }

    # ROADMAP RESULT 
    elif tool_result["type"] == "roadmap_result":
        updates["ws_event"] = {
        "type": "NAVIGATE",
        "target": "roadmap"
    }

    elif tool_result.get("type") == "job_results":
        updates["ws_event"] = {
        "type": "NAVIGATE",
        "target": "jobs"
    }
        
    elif tool_result.get("type") == "networking_events":
        events = tool_result["events"]

        lines = ["Here are upcoming networking events & hackathons:\n"]
        for e in events:
            lines.append(
                f"• **{e['title']}** ({e['type']})\n"
                f"  Mode: {e['mode']}\n"
                f"  Register: {e['registration_url']}\n"
            )

        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": "\n".join(lines)
        }]
        updates["events_completed"] = True
        updates["agent_waiting_for_user"] = True
    
    elif tool_result["type"] == "linkedin_response":
        updates["ws_event"] = {
        "type": "NAVIGATE",
        "target": "linkedin"
    }
        

    elif tool_result["type"] == "quiz_questions":
        questions = tool_result["questions"]

        updates["quiz_questions"] = questions
        updates["quiz_question_idx"] = 1
        updates["quiz_answers"] = {}
        updates["quiz_mode"] = True

        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": f" Quiz started for **{state['selected_career']}**\n\n"
                    f"Question 1:\n{questions[0]['question']}"
        }]
        updates["agent_waiting_for_user"] = True

    if state.get("quiz_mode") and state.get("agent_action") is None:
        idx = state["quiz_question_idx"]
        questions = state["quiz_questions"]

        if idx < len(questions):
            updates["quiz_question_idx"] = idx + 1
            updates["quiz_answers"] = {
                **state["quiz_answers"],
                questions[idx]["question"]: state["messages"][-1]["content"]
            }

            if idx + 1 < len(questions):
                updates["messages"] = state["messages"] + [{
                    "role": "assistant",
                    "content": f"Question {idx+2}:\n{questions[idx+1]['question']}"
                }]
                updates["agent_waiting_for_user"] = True
            else:
                updates["agent_action"] = "QuizEvaluator"

    elif tool_result["type"] == "quiz_evaluation":
        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": f" **Quiz Evaluation Result**\n\n{tool_result['result']}"
        }]

        updates["quiz_mode"] = False
        updates["quiz_completed"] = True
        updates["agent_done"] = True

    elif tool_result["type"] == "tech_news":
        updates["ws_event"] = {
        "type": "NAVIGATE",
        "target": "news"
    }

    # Cleanup
    updates["tool_result"] = None
    updates["agent_action"] = None
    updates["agent_action_input"] = None

    print(f"\n[DEBUG observation_node] Exiting observation_node with updates: {updates}")
    return updates
