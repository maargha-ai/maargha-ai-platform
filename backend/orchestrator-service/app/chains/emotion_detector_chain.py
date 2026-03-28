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


def detect_text_emotion(text: str, threshold: float = 0.7) -> list[str]:
    """
    Robust emotion detection with strict validation to avoid false positives
    """
    try:
        # 🔥 CLEAN TEXT INPUT
        text = text.strip()
        if not text or len(text) < 3:
            return ["Calm"]
        
        # 🔥 NOISE DETECTION - Skip obvious background noise
        noise_words = {"thank", "thanks", "okay", "ok", "yes", "no", "um", "uh", "yeah", "hmm"}
        words = text.lower().split()
        
        # If all words are noise indicators, return calm
        if all(word in noise_words for word in words):
            print(f"[Emotion Detector] Noise detected: '{text}' -> Calm")
            return ["Calm"]
        
        result = emotion_pipeline(text)[0]
        label = result["label"].lower()
        score = result["score"]

        print(f"[Emotion Detector] Text input: '{text}'")
        print(f"[Emotion Detector] Raw emotion: {result}")
        
        # 🔥 STRICT THRESHOLD - Higher threshold to avoid false positives
        if score < threshold:
            print(f"[Emotion Detector] Low confidence ({score:.3f}) -> Calm")
            return ["Calm"]

        emotions = FAST_EMOTION_MAP.get(label, ["Calm"])
        print(f"[Emotion Detector] Final emotions: {emotions}")
        return emotions

    except Exception as e:
        print(f"[Emotion Detector] Error: {e}")
        return ["Calm"]
