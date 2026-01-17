from collections import deque

# user_id → deque of emotions
EMOTION_BUFFERS = {}

def reset_buffer(user_id: str):
    EMOTION_BUFFERS[user_id] = deque(maxlen=200)

def push_emotion(user_id: str, emotion: str, confidence: float):
    print("[BUFFER] push_emotion:", user_id, emotion, confidence)

    if user_id not in EMOTION_BUFFERS:
        reset_buffer(user_id)

    EMOTION_BUFFERS[user_id].append({
        "emotion": emotion,
        "confidence": confidence
    })

def summarize(user_id: str):
    buf = EMOTION_BUFFERS.get(user_id)

    if not buf:
        return {
            "dominant_emotion": "unknown",
            "focus_score": 0.0
        }

    counts = {}
    for e in buf:
        counts[e["emotion"]] = counts.get(e["emotion"], 0) + 1

    dominant = max(counts, key=counts.get)
    focus_score = round(
        counts.get("neutral", 0) / len(buf),
        2
    )

    return {
        "dominant_emotion": dominant,
        "focus_score": focus_score
    }
