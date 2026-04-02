def reset_quiz_state(state):
    state["quiz_active"] = True
    state["current_question"] = None
    state["quiz_answers"] = {}
    state["quiz_question_idx"] = 0
    state["quiz_emotions"] = []
    state["quiz_focus_score"] = None
    state["quiz_evaluation"] = None
