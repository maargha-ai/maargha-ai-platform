# app/chains/quiz_generation_chain.py
import json
import re

from langchain_core.messages import HumanMessage

from app.core.llm_client import llm

QUIZ_PROMPT_TEMPLATE = """
You are a senior technical interviewer.

Generate ONE UNIQUE THEORY-ORIENTED interview question for the topic:
"{topic}"

Difficulty level: {level}

Previously asked questions (DO NOT repeat or paraphrase these):
{previous_questions}

CRITICAL RULES:
- The question MUST be substantially different from previous questions
- Keep the question conceptual/theoretical, even if scenario-based
- Do NOT ask the candidate to build, implement, or write code
- Focus on ONE distinct conceptual angle only:
  - principles and fundamentals
  - architectural reasoning
  - trade-offs and decision criteria
  - failure modes and conceptual mitigation
  - assumptions and constraints analysis
  - system behavior and expected outcomes

Question rules:
- Open-ended
- No multiple choice
- Do NOT include the answer
- Scenario-based is allowed but must remain theory-first
- Difficulty must strictly match the level
- Keep it concise: maximum 24 words, single sentence

Return ONLY valid JSON:
{{
  "question": "..."
}}
"""


async def generate_quiz_question(topic: str, level: str, previous_questions: list[str]):
    previous_block = (
        "\n".join(f"- {q}" for q in previous_questions)
        if previous_questions
        else "None"
    )

    prompt = QUIZ_PROMPT_TEMPLATE.format(
        topic=topic,
        level=level,
        previous_questions=previous_block,
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    raw = response.content.strip()

    try:
        return json.loads(raw)
    except Exception:
        # Fallback: extract first JSON object if model wraps output in prose/code fences.
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        # Final fallback: treat plain text as question.
        if raw:
            clean = raw.replace("```json", "").replace("```", "").strip()
            return {"question": clean}
        return None
