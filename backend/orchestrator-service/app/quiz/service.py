from app.chains.quiz_generation_chain import generate_quiz_question


def is_similar(q1: str, q2: str) -> bool:
    w1 = set(q1.lower().split())
    w2 = set(q2.lower().split())
    return len(w1 & w2) > 8   # overlap threshold

async def generate_quiz_direct(topic, level, asked_questions):
    for _ in range(5):
        quiz = await generate_quiz_question(
            topic=topic,
            level=level,
            previous_questions=list(asked_questions)
        )

        if not quiz:
            continue

        question = quiz["question"].strip()

        if any(is_similar(question, q) for q in asked_questions):
            continue

        asked_questions.add(question)
        return {"question": question}

    raise ValueError("Unable to generate a unique question")
