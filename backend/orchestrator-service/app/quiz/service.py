from app.chains.quiz_generation_chain import generate_quiz_question

async def generate_quiz_direct(topic: str, level: str):
    quiz = await generate_quiz_question(topic, level)

    if not quiz:
        print(quiz)
        raise ValueError("Quiz generation failed")


    return quiz