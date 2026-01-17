from app.chains.quiz_generation_chain import generate_quiz_question

async def quiz_generator_tool(state):
    question = await generate_quiz_question(
        topic=state["quiz_topic"],
        level=state["quiz_level"]
    )

    state["quiz_questions"].append(question["question"])

    return {
        "tool_result": {
            "type": "quiz_question",
            "question": question["question"]
        }
    }
