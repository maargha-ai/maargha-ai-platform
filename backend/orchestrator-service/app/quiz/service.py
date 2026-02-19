import re

from app.chains.quiz_generation_chain import generate_quiz_question


def is_similar(q1: str, q2: str) -> bool:
    # Compare normalized content words to avoid false duplicates.
    w1 = {w for w in re.findall(r"[a-z0-9]+", q1.lower()) if len(w) > 3}
    w2 = {w for w in re.findall(r"[a-z0-9]+", q2.lower()) if len(w) > 3}
    if not w1 or not w2:
        return False
    jaccard = len(w1 & w2) / max(1, len(w1 | w2))
    return jaccard >= 0.65


def _shorten_question(question: str, max_words: int = 24) -> str:
    words = question.split()
    if len(words) <= max_words:
        return question.strip()
    trimmed = " ".join(words[:max_words]).rstrip(",;:")
    if not trimmed.endswith("?"):
        trimmed += "?"
    return trimmed


async def generate_quiz_direct(topic, level, asked_questions):
    for _ in range(3):
        quiz = await generate_quiz_question(
            topic=topic, level=level, previous_questions=list(asked_questions)
        )

        if not quiz:
            continue

        question = _shorten_question(quiz["question"].strip())

        if any(is_similar(question, q) for q in asked_questions):
            continue

        asked_questions.add(question)
        return {"question": question}

    # Resilient fallback so quiz never gets blocked on uniqueness.
    fallback = f"In one concise scenario, explain a key theoretical trade-off in {topic} and justify your reasoning at {level} level."
    if fallback not in asked_questions:
        asked_questions.add(fallback)
        return {"question": fallback}

    raise ValueError("Unable to generate a unique question")


def generate_fallback_question(topic, level, asked_questions, offset=0):
    candidates = [
        f"Explain the core theoretical principles behind {topic} for a {level} learner.",
        f"What are the key conceptual trade-offs in {topic}, and why do they matter?",
        f"Describe one important failure mode in {topic} and the theory behind mitigating it.",
        f"How would you reason about constraints and assumptions in {topic} from first principles?",
    ]
    if candidates:
        shift = offset % len(candidates)
        candidates = candidates[shift:] + candidates[:shift]
    for q in candidates:
        if q not in asked_questions:
            asked_questions.add(q)
            return {"question": q}

    backup = f"What is the most important theoretical concept in {topic}, and how does it influence design decisions?"
    asked_questions.add(backup)
    return {"question": backup}
