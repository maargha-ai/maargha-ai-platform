from transformers import pipeline

emotion_pipeline = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    device=-1,
)

FAST_EMOTION_MAP = {
    "sadness": ["Sadness", "Anxiety", "Stress", "Longing", "Nostalgia"],
    "joy": ["Joy", "Excitement", "Hope", "Motivation"],
    "anger": ["Anger", "Stress", "Tension"],
    "fear": ["Anxiety", "Nervousness", "Stress"],
    "surprise": ["Excitement", "Curiosity"],
    "love": ["Love", "Calm", "Caring", "Comfort", "Hope"],
}


def detect_text_emotion(text: str, threshold: float = 0.6) -> list[str]:
    try:
        result = emotion_pipeline(text)[0]
        label = result["label"].lower()
        score = result["score"]

        print(f"[Emotion Detector] Text input: {text}")
        print(f"[Emotion Detector] Detected emotion: {result}")
        if score < threshold:
            return ["Calm"]

        return FAST_EMOTION_MAP.get(label, ["Calm"])

    except Exception:
        return ["Calm"]
