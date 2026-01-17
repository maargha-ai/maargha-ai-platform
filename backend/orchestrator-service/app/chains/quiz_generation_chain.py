# app/chains/quiz_generation_chain.py
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm
import json

QUIZ_PROMPT_TEMPLATE = """
You are an expert interviewer.

Generate ONE question for the topic:
"{topic}"

Difficulty level: {level}

Rules:
- Open-ended question
- No multiple choice
- No answer
- Practical if possible
- Difficulty must match the level

Return JSON only:
{{
  "question": "..."
}}
"""

async def generate_quiz_question(topic: str, level: str):
    prompt = QUIZ_PROMPT_TEMPLATE.format(
        topic=topic,
        level=level
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    raw = response.content.strip()

    try:
        return json.loads(raw)
    except Exception:
        return {"question": f"Explain {topic} concepts ({level} level)."}
