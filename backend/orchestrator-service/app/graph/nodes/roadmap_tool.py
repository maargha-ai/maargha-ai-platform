# app/graph/nodes/roadmap_tool.py
from app.core.state import AgentState
from app.chains.roadmap_chain import generate_roadmap_video
from app.storage.local_storage import save_roadmap_video

async def roadmap_tool(state: AgentState):
    selected_career = state.get("selected_career")
    user_id = state.get("user_id")

    if not selected_career:
        return {
            "tool_error": "No career selected"
        }
    
    # 1. Generate video (TEMP path)
    temp_video_path = await generate_roadmap_video(
        career=selected_career
    )

    # 2. Persist video
    video_url = save_roadmap_video(
        temp_path=temp_video_path,
        user_id=user_id
    )

    return {
        "tool_result": {
            "type": "roadmap_result",
            "career": selected_career,
            "video_url": video_url
        }
    }
