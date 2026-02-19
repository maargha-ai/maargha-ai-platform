from typing import List

from pydantic import BaseModel


class CVInput(BaseModel):
    name: str
    target_role: str
    self_intro: str
    skills: List[str]
    education: str
    projects: List[str]
