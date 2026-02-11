# app/chains/roadmap_chain.py
import json
from app.core.llm_client import llm
from langchain_core.messages import HumanMessage

async def generate_roadmap(career: str):
    prompt = f"""
    You are a senior career architect.

    Generate a clear learning roadmap for:
    "{career}"

    Rules:
    - 6 to 8 steps
    - Each step must have:
      - title
      - description (1–2 concise lines)
    - Cover: fundamentals, tools, projects, specialization, certifications, job prep
    - Return ONLY valid JSON
    - No markdown
    - No explanations

    Format:
    {{
      "career": "{career}",
      "steps": [
        {{
          "title": "...",
          "description": "..."
        }}
      ]
    }}
    """

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return json.loads(response.content)


