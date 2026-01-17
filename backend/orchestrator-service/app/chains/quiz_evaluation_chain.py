# app/chains/quiz_evaluation_chain.py
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm

EVAL_PROMPT_TEMPLATE = """
You are a senior interviewer.

Career/Topic: {career}

Evaluate the candidate using:
1. Answer quality
2. Emotional confidence
3. Focus consistency

Emotion summary:
- Dominant emotion: {emotion_summary[dominant_emotion]}
- Focus score: {emotion_summary[focus_score]}

Questions & Answers:
{qa_block}

Provide:
- Knowledge score
- Confidence assessment
- Attention insights
- Suggestions
"""


async def evaluate_quiz(career: str, quiz_answers: dict, emotion_summary: dict):
    qa_lines = []
    for q, a in quiz_answers.items():
        qa_lines.append(f"Q: {q}\nA: {a}")

    prompt = EVAL_PROMPT_TEMPLATE.format(
        career=career,
        qa_block="\n\n".join(qa_lines),
        emotion_summary=emotion_summary
    )

    response = await llm.ainvoke([
        HumanMessage(content=prompt)
    ])

    return response.content.strip()
