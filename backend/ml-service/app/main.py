from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.embeddings.embeddings import embed_texts, embed_single
from app.ner.resume_parser import extract_resume_entities
from app.services.emotion import detect_text_emotion

app = FastAPI()


# -----------------------------
# MODELS
# -----------------------------
class EmotionRequest(BaseModel):
    text: str


# -----------------------------
# EMBEDDINGS
# -----------------------------
@app.post("/embed")
async def embed(data: dict):
    texts = data.get("texts")

    if isinstance(texts, list):
        return {"embeddings": embed_texts(texts)}
    elif isinstance(texts, str):
        return {"embedding": embed_single(texts)}
    else:
        return {"error": "Invalid input"}


# -----------------------------
# MALPRACTICE DETECTION
# -----------------------------
@app.post("/detect-malpractice")
async def detect(data: dict):
    from app.monitoring.gaze_detector import is_looking_away

    frame = data.get("frame")
    result = is_looking_away(frame)

    return {"result": result}


# -----------------------------
# RESUME PARSER
# -----------------------------
@app.post("/parse-resume")
async def parse_resume(data: dict):
    text = data.get("text")

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        entities = extract_resume_entities(text)
        return {"entities": entities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# EMOTION DETECTION ✅
# -----------------------------
@app.post("/detect-emotion")
def detect_emotion_api(req: EmotionRequest):
    emotions = detect_text_emotion(req.text)
    return {"emotions": emotions}