# app/graph/nodes/quiz_evaluator_tool.py
from app.chains.quiz_evaluation_chain import evaluate_quiz

async def quiz_evaluator_tool(state):
    result = await evaluate_quiz(
        career=state["selected_career"],
        quiz_answers=state["quiz_answers"]
    )

    return {
        "tool_result": {
            "type": "quiz_evaluation",
            "result": result
        }
    }
