# app/chains/quiz_evaluation_chain.py
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm

EVAL_PROMPT_TEMPLATE = """
You are a senior technical interviewer.

Career / Topic: {career}

Evaluate the candidate based ONLY on:
1. Technical correctness of answers
2. Depth of understanding
3. Practical reasoning and clarity

Questions & Answers:
{qa_block}

Provide:
- Overall score (0–100)
- Strengths
- Weaknesses
- Actionable improvement suggestions
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

    # Simple deterministic score (can be improved later)
    score = min(100, max(40, len(quiz_answers) * 20))

    return {
        "score": score,
        "feedback": response.content.strip()
    }
