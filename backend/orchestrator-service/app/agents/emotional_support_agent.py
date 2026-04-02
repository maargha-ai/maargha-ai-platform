import io
import os

import numpy as np
import soundfile as sf
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

load_dotenv()

# Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
)

# Load text emotion model ONCE
# text_emotion_pipeline = pipeline(
#     "text-classification",
#     model="bhadresh-savani/distilbert-base-uncased-emotion",
#     device=-1,
# )


# -----------------------------
# # TEXT EMOTION
# # -----------------------------
# def detect_text_emotion(text: str) -> str:
#     try:
#         result = text_emotion_pipeline(text)
#         emotion = result[0]["label"].lower()
#         score = result[0]["score"]

#         if score > 0.6:
#             return emotion
#         return "neutral"

#     except Exception as e:
#         print("[TEXT EMOTION ERROR]", e)
#         return "neutral"

def detect_text_emotion(text: str) -> str:
    try:
        text = text.lower().strip()

        if not text:
            return "neutral"

        if any(word in text for word in ["sad", "depressed", "unhappy", "tired", "lonely"]):
            return "sad"

        if any(word in text for word in ["happy", "great", "excited", "good", "amazing"]):
            return "happy"

        if any(word in text for word in ["angry", "mad", "frustrated", "annoyed"]):
            return "angry"

        if any(word in text for word in ["scared", "afraid", "anxious", "nervous"]):
            return "fear"

        return "neutral"

    except Exception as e:
        print("[TEXT EMOTION ERROR]", e)
        return "neutral"


# -----------------------------
# SPEECH → TEXT
# -----------------------------
async def transcribe_audio(audio: np.ndarray) -> str:
    try:
        audio_int16 = (audio * 32767).astype(np.int16)

        buffer = io.BytesIO()
        sf.write(buffer, audio_int16, 16000, format="WAV", subtype="PCM_16")
        buffer.seek(0)

        transcription = openai_client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=("speech.wav", buffer, "audio/wav"),
            language="en",
            temperature=0.0,
        )

        return transcription.text.strip()

    except Exception as e:
        print("[STT ERROR]", e)
        return ""


# -----------------------------
# LLM RESPONSE
# -----------------------------
def generate_response(text: str, emotion: str) -> str:
    prompt_map = {
        "happy": "Be super cheerful, warm, and uplifting.",
        "sad": "Be deeply empathetic, gentle, and comforting.",
        "angry": "Stay calm, patient, and understanding.",
        "fear": "Be soft, reassuring, and nurturing.",
        "neutral": "Be warm, kind, and natural.",
    }

    system_prompt = (
        "You are a caring female emotional support companion named Emily. "
        "Speak warmly, calmly, and naturally. "
        "Be concise and focused. "
        "Limit responses to a maximum of 2 short sentences. "
        "Avoid repetition, filler, or long explanations. "
        "Ask at most one gentle follow-up question if appropriate. "
        "Do NOT use actions like *smiles*, *hugs*, or emojis. "
        f"{prompt_map.get(emotion, '')}"
    )

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            max_tokens=120,
            temperature=0.85,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("[LLM ERROR]", e)
        return "I'm here for you. You're not alone."
