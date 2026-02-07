# app/chains/quiz_generation_chain.py
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm
import json

QUIZ_PROMPT_TEMPLATE = """
You are a senior technical interviewer.

Generate ONE UNIQUE interview question for the topic:
"{topic}"

Difficulty level: {level}

CRITICAL RULES:
- The question MUST be substantially different from the above questions
- Avoid generic or textbook-style questions
- Focus on ONE distinct angle ONLY:
  • real-world application
  • debugging / troubleshooting
  • performance optimization
  • edge cases and failure scenarios
  • architectural or design decisions
  • trade-offs and reasoning
  • scalability or constraints

Question rules:
- Open-ended
- No multiple choice
- Do NOT include the answer
- Scenario-based if possible
- Difficulty must strictly match the level

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
        previous_questions=previous_block
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    raw = response.content.strip()

    try:
        return json.loads(raw)
    except Exception:
        return None