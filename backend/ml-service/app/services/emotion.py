from transformers import pipeline

# Load once at startup
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


def detect_text_emotion(text: str, threshold: float = 0.7) -> list[str]:
    try:
        text = text.strip()

        if not text or len(text) < 3:
            return ["Calm"]

        noise_words = {"thank", "thanks", "okay", "ok", "yes", "no", "um", "uh", "yeah", "hmm"}
        words = text.lower().split()

        if all(word in noise_words for word in words):
            return ["Calm"]

        result = emotion_pipeline(text)[0]
        label = result["label"].lower()
        score = result["score"]

        if score < threshold:
            return ["Calm"]

        return FAST_EMOTION_MAP.get(label, ["Calm"])

    except Exception as e:
        print("Emotion error:", e)
        return ["Calm"]