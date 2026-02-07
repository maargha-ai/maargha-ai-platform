""" GraphState definitions """

# app/core/state.py
from typing import TypedDict, List, Dict, Optional

class AgentState(TypedDict):
    messages: List[Dict[str, str]]           # Full conversation history
    user_id: str                              # From auth

    # Agent loop
    agent_thought: Optional[str]
    agent_action: Optional[str]
    agent_action_input: Optional[dict]
    agent_observation: Optional[str]
    agent_done: bool
    agent_waiting_for_user: bool
    agent_response: Optional[str]
    
    navigate: Optional[Dict[str, dict]] 
    
    # Career flow
    selected_career: Optional[str]
    career_answers: Optional[Dict[str, str]] = None
    career_question_idx: Optional[int] = 0
    career_suggestions: Optional[List[Dict]]
    awaiting_career_selection: Optional[bool]
    roadmap_generated: Optional[bool]

    # Jobs / CV flow
    awaiting_cv: Optional[bool]
    awaiting_job_role: Optional[bool]
    awaiting_job_location: Optional[bool]
    jobs_completed: bool    
    cv_path: Optional[str]
    job_role: Optional[str]
    job_location: Optional[str]

    tool_result: Optional[str]
    tool_error: Optional[str]
    career_options: Optional[List[Dict]]= None

    # Events
    events_completed: bool
    events_filter: str  # hackathon / meetup / conference

    # LinkedIn
    linkedin_mode: bool = False

    # Quiz config
    quiz_topic: str | None
    quiz_level: str | None
    quiz_active: bool
    asked_questions: set[str]

    # Quiz runtime
    current_question: dict
    quiz_answers: dict
    quiz_question_idx: int

    # FER / attention tracking
    quiz_emotions: list        # [{emotion, confidence, timestamp}]
    quiz_focus_score: float | None

    # Final evaluation
    quiz_evaluation: dict | None

    # News
    tech_news_completed: bool

    # Emotion 
    detected_emotion: Optional[str]

    # Music
    music_recommendation: Optional[List[Dict]]

