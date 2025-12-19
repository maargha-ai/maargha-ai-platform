# app/graph/nodes/jobs_tool.py
from app.core.state import AgentState
from app.chains.jobs_chain import find_jobs_for_cv
from pathlib import Path

BACKEND_CV_PATH = Path(
    "app/static/cvs/test_cv.pdf"  # ← keep your CV here
)

async def jobs_tool(state: AgentState):
    # cv_path = state.get("cv_path")
    job_role = state.get("job_role")
    job_location = state.get("job_location")
    # Use backend CV if user hasn't uploaded one yet
    cv_path = state.get("cv_path") or str(BACKEND_CV_PATH)

    # Tool should NOT ask questions
    if not job_role or not job_location:
        return {
            "tool_error": "Missing required inputs for job search"
        }

    results = await find_jobs_for_cv(
        cv_path=cv_path,
        role=job_role,
        location=job_location,
        max_jobs=200
    )

    if not results:
        return {
            "tool_result": {
                "type": "job_result",
                "message": "No matching jobs found",
                "jobs": []
            }
        }

    return {
        "tool_result": {
            "type": "job_results",
            "count": len(results),
            "jobs": results
        },
        "jobs_completed": True
    }
