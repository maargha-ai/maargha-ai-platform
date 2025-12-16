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
        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": tool_result["question"]
        }]
        updates["career_question_idx"] = tool_result["next_idx"]
        updates["agent_waiting_for_user"] = True

    # Career Result
    elif tool_result["type"] == "career_result":
        careers = tool_result["careers"]
        msg = "Here are your recommended careers:\n\n"
        for i, c in enumerate(careers, 1):
            msg += f"{i}. **{c['title']}**\n"
            msg += f"   {c['reason']}\n"
            msg += f"   Skills: {', '.join(c['skills'])}\n\n"
        msg += "Reply with a number (1–4) to choose."

        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": msg
        }]
        updates["career_options"] = careers
        updates["agent_waiting_for_user"] = True

        # ROADMAP RESULT 
    elif tool_result["type"] == "roadmap_result":
        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": (
                f"**Roadmap Generated for {tool_result['career']}**\n\n"
                f"Video: {tool_result['video_url']}\n\n"
                "What would you like to do next?\n"
                "• Find jobs\n"
                "• Upload CV\n"
                "• Change career"
            )
        }]
        updates["roadmap_generated"] = True
        updates["agent_waiting_for_user"] = True

    elif tool_result.get("type") == "job_results":
        jobs = tool_result["jobs"]

        lines = ["Here are the top job matches for you:\n"]
        for score, job in jobs[:10]:
            lines.append(
                f"• **{job['title']}** at {job['company']}\n"
                f"  Source: {job['source']}\n"
                f"  Link: {job['link']}\n"
            )
            message = "\n".join(lines)

        updates["messages"] = state["messages"] + [{
            "role": "assistant", "content": message
            }]
    
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
        updates["messages"] = state["messages"] + [{
            "role": "assistant",
            "content": tool_result["content"]
        }]
        updates["agent_waiting_for_user"] = True
        
    # Cleanup
    updates["tool_result"] = None
    updates["agent_action"] = None
    updates["agent_action_input"] = None

    print(f"\n[DEBUG observation_node] Exiting observation_node with updates: {updates}")
    return updates
