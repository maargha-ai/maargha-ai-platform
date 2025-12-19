# app/chains/quiz_generation_chain.py
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm

QUIZ_PROMPT_TEMPLATE = """
You are an expert technical interviewer.

Generate a short quiz to assess a candidate's knowledge for the career:
"{career}"

Rules:
- Generate exactly 5 questions
- Questions should be open-ended (not MCQ)
- Questions should progressively increase in difficulty
- Keep questions concise and practical
- Do NOT include answers

Return the output strictly as JSON in this format:

[
  {{
  "question": "...",
  "options": []
}}
]
"""

async def generate_quiz(career: str):
    prompt = QUIZ_PROMPT_TEMPLATE.format(career=career)

    response = await llm.ainvoke([
        HumanMessage(content=prompt)
    ])

    raw = response.content.strip()

    try:
        import json
        quiz = json.loads(raw)
        return quiz
    except Exception:
        # Fallback safety
        return [
            {"question": "Explain the core responsibilities of a " + career},
            {"question": "What tools are commonly used in this role?"},
            {"question": "Explain a common real-world problem faced in this role."},
            {"question": "How would you troubleshoot an issue in this domain?"},
            {"question": "How do you keep your skills updated in this field?"}
        ]
