from app.schemas.cv import CVInput
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm

# Prompt Builder
def build_cv_prompt(data: CVInput) -> str:
    skills_text = "\n".join(f"- {s}" for s in data.skills)
    projects_text = "\n".join(f"- {p}" for p in data.projects)

    return f"""
You are a senior resume writer and ATS optimization expert.

Your task is to generate a HIGHLY ATS-FRIENDLY resume.

STRICT RULES:
- Plain text only
- No tables, no columns, no icons, no emojis
- Use standard section headings exactly as written
- Bullet points must start with strong action verbs
- Optimize for ATS parsing (simple structure, keywords naturally placed)
- Do NOT invent fake experience
- Keep it professional and concise

Use the following format EXACTLY:

==============================
{data.name}
Target Role: {data.target_role}

PROFESSIONAL SUMMARY
{data.self_intro}

SKILLS
{skills_text}

PROJECTS
{projects_text}

EDUCATION
{data.education}
==============================

Generate the resume now.
"""


# -------- Chain Function --------
async def generate_cv(data: CVInput) -> str:
    prompt = build_cv_prompt(data)
    response = await llm.ainvoke(
        [HumanMessage(content=prompt)]
    )
    return response.content.strip()
