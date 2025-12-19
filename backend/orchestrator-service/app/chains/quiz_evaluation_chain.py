# app/chains/quiz_evaluation_chain.py
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm

EVAL_PROMPT_TEMPLATE = """
You are a senior interviewer evaluating a quiz attempt.

Career: {career}

Below are the questions and the user's answers.

Evaluate based on:
- Conceptual understanding
- Practical thinking
- Clarity of explanation

Provide:
1. Overall assessment
2. Strengths
3. Weak areas
4. Suggestions to improve

Questions & Answers:
{qa_block}

Respond in clear professional language.
"""

async def evaluate_quiz(career: str, quiz_answers: dict):
    qa_lines = []
    for q, a in quiz_answers.items():
        qa_lines.append(f"Q: {q}\nA: {a}")

    prompt = EVAL_PROMPT_TEMPLATE.format(
        career=career,
        qa_block="\n\n".join(qa_lines)
    )

    response = await llm.ainvoke([
        HumanMessage(content=prompt)
    ])

    return response.content.strip()
