# app/graph/nodes/reasoning_node.py
import json
from app.core.state import AgentState
from app.core.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.chains.career_chain import QUESTIONS
from app.intent.intent_router import route_intent

SYSTEM_PROMPT = """
You are a friendly, professional, and patient AI planner agent. You MUST strictly follow these rules.

Your goal is to help the user with:
- Career prediction and guidance
- Generating personalized learning roadmaps
- Helping with job search and CV matching
- Finding Hackathons, Conferences, Ideathons, Summits, Seminars
- Helping to optmize LinkedIn profile using LinkedIn Assistant
- Generating quiz questions and evaluation user based on it

But you are also warm and conversational — you don't push too hard.

CONVERSATIONAL STYLE (IMPORTANT):
- Be friendly, warm, and patient.
- If the user wants casual chat or resists career help:
  - Acknowledge politely ONCE or TWICE (e.g., "Sure, we can chat!" or "No problem!").
  - Then gently bring it back: "Whenever you're ready, I'm here to help with career stuff too 😊"
  - Do not keep repeating the same redirect question.
- If user talks about money, trading, IT, etc. — treat it as potential career interest and offer help.
- You can have 1-2 light exchanges before guiding back.

ERROR AND MISSING DATA HANDLING (MUST OBEY):
- If you see any observation like "Missing career answers", "error", "missing", or tool failure:
  - DO NOT retry the same tool.
  - IMMEDIATELY switch to AskUser.
  - Start collecting the required information (e.g., begin the career quiz by asking the first question).
- Example:
  Observation: Missing career answers
  → Ask the first quiz question politely.

CAREER PREDICTION FLOW (STRICT):
- For career prediction: ALWAYS call CareerPredictor with {} (empty input)
- It will return a question in observation → use AskUser to ask it
- User answers yes/no → call CareerPredictor again to get next question
- After all questions, it returns careers → present them with AskUser
- NEVER predict careers manually

AVAILABLE TOOLS:
1. CareerPredictor → Use when user clearly wants career suggestion/prediction
2. RoadmapGenerator → Requires selected_career
3. JobSearch → Requires cv_path, job_role, job_location
4. NetworkingEvents
5. LinkedInAssistant → Use when user need help in optimizing linkedin profile
6. QuizGenerator

CRITICAL RULES:
- Only one action per step
- If info missing → AskUser
- If error in observation → AskUser for clarification, do not retry
- Do not repeat failed actions
- When task complete → DONE
- Never explain your thought process
- Only call RoadmapGenerator when:
  - state has "selected_career" set
  - OR user explicitly says "give me roadmap for X"
- If user says "game development" but no career_options yet → treat as quiz answer

OUTPUT ONLY with valid JSON:

{
  "thought": "Brief internal reasoning (1-2 sentences max)",
  "action": "CareerPredictor | RoadmapGenerator | JobSearch | NetworkingEvents | AskUser | DONE",
  "action_input": {...}
}

"""

async def reasoning_node(state: AgentState):
    # print(f"\n[DEBUG reasoning_node] Entering reasoning_node with state: {state}")  # Shows full state on entry    
    if state.get("agent_waiting_for_user"):
        print("\n[DEBUG reasoning_node] Agent waiting for user — skipping reasoning")
        return {}
    
    last_msg = state["messages"][-1]["content"].lower().strip()
    
    if state.get("linkedin_mode"):
        intent = route_intent(last_msg)

        if intent not in ["linkedin_assistant", "general_chat"]:
            return {
            "linkedin_mode": False,
            "agent_action": None,
            "agent_action_input": None
        }
        else:
            # Otherwise stay inside LinkedIn Assistant
            return {
                "agent_action": "LinkedInAssistant",
                "agent_action_input": {
                    "user_message": last_msg
                },
            "agent_waiting_for_user": True
            }
        
        
    if any(k in last_msg for k in ["linkedin", "optimize profile"]):
        return {
            "agent_thought": "User wants help with LinkedIn profile optimization",
            "agent_action": "LinkedInAssistant",
            "agent_action_input": {
                "user_message": last_msg
            },
            "linkedin_mode": True
        }
    
    if any(k in last_msg for k in [
        "quiz", "test me", "assessment", "evaluate me", "practice questions"
    ]):
        if not state.get("selected_career"):
            return {
                "agent_action": "AskUser",
                "agent_action_input": {
                    "message": (
                        "I can create a quiz based on your career.\n\n"
                        "Would you like to:\n"
                        " Predict your career first\n"
                        " Tell me your career directly"
                    )
                },
                "agent_waiting_for_user": True
            }

        return {
            "agent_thought": "User wants a quiz based on career",
            "agent_action": "QuizGenerator",
            "agent_action_input": {
                "career": state["selected_career"]
            },
            "quiz_mode": True
        }


    # NETWORKING EVENTS 
    if any(k in last_msg for k in [
        "hackathon", "meetup", "conference", "event", "networking"
    ]):
        if not state.get("events_completed"):
            return {
                "agent_thought": "User wants networking or hackathon events",
                "agent_action": "NetworkingEvents",
                "agent_action_input": {
                    "event_type": "hackathon"
                }
            }

    if state.get("jobs_completed"):
        return {
            "agent_thought": "Job search already completed. Waiting for user.",
            "agent_action": None,
            "agent_action_input": None,
            "agent_done": True,
            "jobs_completed": False
        }

    if (
        state.get("selected_career")
        and not state.get("roadmap_generated")
        and any(k in last_msg for k in ["roadmap", "learning path", "plan"])
    ):
        return {
            "agent_thought": "User wants a roadmap for the selected career",
            "agent_action": "RoadmapGenerator",
            "agent_action_input": {
                "selected_career": state["selected_career"]
            }
        }

    # Handle yes/no answers 
    if last_msg in ["yes", "no"] and state.get("career_question_idx", 0) > 0:
        idx = state["career_question_idx"] - 1
        answers = state.get("career_answers", {})
        answers[QUESTIONS[idx]] = last_msg
        print(f"\n[DEBUG reasoning_node] Exiting reasoning_node with state: {state}") 
        return {
            "career_answers": answers,
            "agent_action": "CareerPredictor"
        }

    # Handle career selection
    if last_msg.isdigit() and state.get("career_options"):
        idx = int(last_msg) - 1
        options = state["career_options"]
        if 0 <= idx < len(options):
            print(f"\n[DEBUG reasoning_node] Exiting reasoning_node with state: {state}") 
            return {
                "agent_action": "SelectCareer",
                "agent_action_input": {
                    "career": options[idx]["title"]
                }
            }

    # Otherwise let LLM plan
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(
        HumanMessage(content=m["content"])
        for m in state["messages"]
        if m["role"] == "user"
    )

    response = await llm.ainvoke(messages)
    raw = (response.content or "").strip()
    plan = safe_json_parse(raw)

    if plan is None:
        # Planner failed → graceful fallback
        return {
            "agent_thought": "Planner returned invalid or non-JSON output",
            "agent_action": "AskUser",
            "agent_action_input": {
                "message": "What job role are you looking for and in which location?"
            },
            "agent_done": False,
        }


    print(f"\n[DEBUG reasoning_node] Exiting reasoning_node with state: {state}") 
    return {
        "agent_thought": plan["thought"],
        "agent_action": plan["action"],
        "agent_action_input": plan.get("action_input", {})
    }

def safe_json_parse(text: str):
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
