# app/graph/nodes/quiz_generator_tool.py
from app.chains.quiz_generation_chain import generate_quiz

async def quiz_generator_tool(state):
    quiz = await generate_quiz(state["selected_career"])

    return {
        "tool_result": {
            "type": "quiz_questions",
            "questions": quiz
        }
    }
