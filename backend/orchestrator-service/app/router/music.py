from fastapi import APIRouter
from pydantic import BaseModel
from app.chains.emotion_detector_chain import detect_text_emotion
from app.chains.music_recommendation_chain import MusicRecommendationChain

router = APIRouter(prefix="/music", tags=["Music"])

music_chain = MusicRecommendationChain()

class MusicRequest(BaseModel):
    user_text: str

@router.post("/recommend")
def recommend_music(req: MusicRequest):
    emotion = detect_text_emotion(req.user_text)
    print(f"[Music Route]: Emotion returned {emotion}")
    song = music_chain.recommend(emotion)
    print(f"[Music Route]: Song {song}")
    if not song:
        return {
            "emotion": emotion,
            "message": "No matching song found"
        }

    return {
        "emotion": emotion,
        "song": song
    }
