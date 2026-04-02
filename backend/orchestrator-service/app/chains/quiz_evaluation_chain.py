# app/chains/quiz_evaluation_chain.py
import asyncio
import json
import re

from langchain_core.messages import HumanMessage

from app.core.llm_client import llm

EVAL_PROMPT_TEMPLATE = """
You are a senior technical interviewer.

Career / Topic: {career}

Evaluate the candidate based ONLY on:
1. Technical correctness
2. Depth of understanding
3. Conceptual clarity
4. Relevance to the question

Questions & Answers:
{qa_block}

Scoring rubric:
- 0-30: mostly missing, incorrect, or very vague answers
- 31-50: basic awareness with major gaps
- 51-70: fair understanding with partial depth
- 71-85: strong understanding with minor gaps
- 86-100: excellent and consistently deep responses

Return ONLY valid JSON with this shape:
{{
  "overall_score": <integer 0-100>,
  "summary": "2-3 sentence overall assessment",
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "suggestions": ["...", "..."]
}}
"""


def _quality_cap(quiz_answers: dict) -> int:
    answered = [str(a).strip() for a in quiz_answers.values() if str(a).strip()]
    if not answered:
        return 0

    total_words = sum(len(re.findall(r"\w+", a)) for a in answered)
    avg_words = total_words / max(1, len(answered))

    cap = 100
    if len(answered) == 1:
        cap = min(cap, 45)
    elif len(answered) == 2:
        cap = min(cap, 65)

    if total_words < 20:
        cap = min(cap, 35)
    elif total_words < 50:
        cap = min(cap, 55)
    elif total_words < 100:
        cap = min(cap, 70)

    if avg_words < 8:
        cap = min(cap, 45)
    elif avg_words < 15:
        cap = min(cap, 60)

    return cap


def _level_from_score(score: int) -> str:
    if score >= 85:
        return "Expert"
    if score >= 65:
        return "Intermediate"
    return "Beginner"


async def evaluate_quiz(career: str, quiz_answers: dict):
    qa_lines = [f"Q: {q}\nA: {a}" for q, a in quiz_answers.items()]

    if not qa_lines:
        return {
            "score": 0,
            "level": "Beginner",
            "summary": "No answers were submitted.",
            "strengths": [],
            "weaknesses": ["No evaluable response content provided."],
            "suggestions": [
                "Attempt at least 3 concise, relevant answers before terminating."
            ],
            "feedback": "No answers were submitted.",
        }

    prompt = EVAL_PROMPT_TEMPLATE.format(career=career, qa_block="\n\n".join(qa_lines))
    try:
        response = await asyncio.wait_for(
            llm.ainvoke([HumanMessage(content=prompt)]),
            timeout=12,
        )
        raw = str(response.content).strip()
    except Exception:
        raw = ""

    parsed = None
    try:
        parsed = json.loads(raw)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except Exception:
                parsed = None

    if not isinstance(parsed, dict):
        parsed = {
            "overall_score": 50,
            "summary": raw[:600] if raw else "Evaluation generated.",
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
        }

    raw_score = parsed.get("overall_score", 50)
    try:
        model_score = int(raw_score)
    except (TypeError, ValueError):
        model_score = 50
    model_score = max(0, min(100, model_score))

    final_score = min(model_score, _quality_cap(quiz_answers))

    strengths = (
        parsed.get("strengths") if isinstance(parsed.get("strengths"), list) else []
    )
    weaknesses = (
        parsed.get("weaknesses") if isinstance(parsed.get("weaknesses"), list) else []
    )
    suggestions = (
        parsed.get("suggestions") if isinstance(parsed.get("suggestions"), list) else []
    )
    summary = str(parsed.get("summary", "")).strip() or "Evaluation generated."

    # Backward-compatible text block for any old UI paths.
    feedback_parts = [
        f"Summary: {summary}",
        "Strengths: " + ("; ".join(strengths) if strengths else "None highlighted."),
        "Weaknesses: " + ("; ".join(weaknesses) if weaknesses else "None highlighted."),
        "Suggestions: "
        + (
            "; ".join(suggestions)
            if suggestions
            else "Keep practicing with deeper, structured answers."
        ),
    ]

    return {
        "score": final_score,
        "level": _level_from_score(final_score),
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "feedback": "\n".join(feedback_parts),
    }
