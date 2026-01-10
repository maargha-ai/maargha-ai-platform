from transformers import pipeline

emotion_pipeline = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    device=-1
)

def detect_text_emotion(text: str):
    try:
        result = emotion_pipeline(text)
        label = result[0]["label"].lower()
        score = result[0]["score"]
        return label if score > 0.6 else "neutral"
    except Exception:
        return "neutral"
    
    