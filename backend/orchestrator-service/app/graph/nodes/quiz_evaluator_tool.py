# app/graph/nodes/quiz_evaluator_tool.py
from app.chains.quiz_evaluation_chain import evaluate_quiz
from app.fer.emotion_buffer import summarize as emotion_summary

async def quiz_evaluator_tool(state):
    result = await evaluate_quiz(
        topic=state["quiz_topic"],         
        quiz_answers=state["quiz_answers"],
        emotion_summary=emotion_summary()
    )

    return {
        "tool_result": {
            "type": "quiz_evaluation",
            "result": result
        }
    }
