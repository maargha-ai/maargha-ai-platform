# app/chains/career_chain.py
import json
from typing import Dict, List

from langchain_core.messages import HumanMessage

from app.core.llm_client import llm

QUESTIONS = [
    "Do you enjoy solving mathematical problems? (yes/no)",
    "Are you interested in ethical hacking? (yes/no)",
    "Do you find networking, servers, infrastructure appealing? (yes/no)",
    "Do you like writing code and building software? (yes/no)",
    "Are you interested in databases? (yes/no)",
    "Do you prefer working on UI/UX and front-end design? (yes/no)",
    "Would you enjoy customer-facing and business-oriented IT roles? (yes/no)",
    "Do you like research-focused roles that explore new AI techniques? (yes/no)",
    "Does Linux system administration excite you? (yes/no)",
    "Does forensic analysis of cyber attacks excite you? (yes/no)",
    "Do you prefer mobile development (Android/iOS) or web UI? (yes/no)",
    "Do you enjoy detecting edge cases and breaking applications? (yes/no)",
    "Do you enjoy configuring routers, switches and firewalls? (yes/no)",
    "Are you interested in game engines like Unity or Unreal Engine? (yes/no)",
    "Would you enjoy a role in teaching, mentorship, or educational content creation? (yes/no)",
]


def build_prompt(answers: Dict[str, str]) -> str:
    bullet_text = "\n".join([f"- {q}: {a}" for q, a in answers.items()])
    return f"""
    You are an expert IT career advisor.

    Based on the user's answers, recommend EXACTLY 4 suitable IT careers.
    For each career provide:
    1. Title (example: "Data Engineer")
    2. One-line reason why it matches the user
    3. Top 5 skills to learn

    User responses:
    {bullet_text}

    Respond ONLY in valid JSON as a list of objects:
    [
      {{"title": "...", "reason": "...", "skills": ["...", "..."]}}
    ]
    """


async def predict_careers_from_answers(answers: Dict[str, str]) -> List[Dict]:
    prompt = build_prompt(answers)
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    raw = response.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [
            {
                "title": "Software Engineer",
                "reason": "Versatile role",
                "skills": ["Python", "Git", "DSA"],
            }
        ]
