from app.schemas.cv import CVInput
from langchain_core.messages import HumanMessage
from app.core.llm_client import llm

def build_cv_prompt(data: CVInput) -> str:
    skills_text = "\n".join(f"- {s}" for s in data.skills)
    projects_text = "\n".join(f"- {p}" for p in data.projects)

    return f"""
You are a resume content generator.

IMPORTANT:
- You generate CONTENT ONLY.
- You must NOT invent experience.
- You must NOT change section titles.
- You must NOT add new sections.
- You must NOT remove sections.
- Do NOT add any decorative characters, lines, or symbols.
- Plain text only.

STRICT TEMPLATE (DO NOT MODIFY):

NAME:
{data.name}

TARGET ROLE:
{data.target_role}

SECTION: PROFESSIONAL SUMMARY
{data.self_intro}

SECTION: SKILLS
{skills_text}

SECTION: PROJECTS
{projects_text}

SECTION: EDUCATION
{data.education}

END OF TEMPLATE.

Generate the resume content exactly inside this structure.
"""


# -------- Chain Function --------
async def generate_cv(data: CVInput) -> str:
    prompt = build_cv_prompt(data)
    response = await llm.ainvoke(
        [HumanMessage(content=prompt)]
    )
    return response.content.strip()
