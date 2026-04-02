import os
import numpy as np
import asyncio, io, queue, time, librosa, pyaudio, pyttsx3
import soundfile as sf
from groq import Groq
from openai import OpenAI
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
)

# Global state
state = {
    "current_emotion": "neutral",
    "audio_queue": queue.Queue(),
    "is_listening": False,
    "is_speaking": False,
    "silence_started_at": None,
    "ignore_until": 0.0,  # ← NEW: Don't detect speech until this time
}

# Load text emotion model once
text_emotion_pipeline = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    device=-1,
)


def detect_text_emotion(text: str):
    try:
        result = text_emotion_pipeline(text)
        emotion = result[0]["label"].lower()
        score = result[0]["score"]

        # Debug: Show what it detected
        print(f"[DEBUG] Text Emotion: {emotion.upper()} (confidence: {score:.2f})")

        if score > 0.6:
            return emotion
        return "neutral"
    except Exception as e:
        print(f"[Text Emotion Error] {e}")
        return "neutral"


async def transcribe_audio(audio: np.ndarray):
    try:
        # Convert float32 → int16 (Whisper expects this)
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
        print(f"[STT Error] {e}")
        return ""


def generate_response(text: str, emotion: str):
    prompt_map = {
        "happy": "Be super cheerful, warm, and uplifting!",
        "sad": "Be deeply empathetic, gentle, and comforting",
        "angry": "Stay calm, patient, and understanding",
        "fear": "Be soft, reassuring, and nurturing",
        "neutral": "Be warm, kind, and natural",
    }
    prompt = prompt_map.get(emotion, "Be warm and supportive")

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a caring female emotional support companion, and your name is Emily. Respond naturally and warmly. Do NOT use *actions* like *smiles*, *nods*, or (takes your hand). Just speak directly and kindly. {prompt}",
                },
                {"role": "user", "content": text},
            ],
            max_tokens=100,
            temperature=0.85,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[LLM Error] {e}")
        return "I'm here for you. You're not alone."


async def speak_text(text: str):
    engine = pyttsx3.init()
    for v in engine.getProperty("voices"):
        if any(x in v.name.lower() for x in ["zira", "female", "emma"]):
            engine.setProperty("voice", v.id)
            break
    engine.setProperty("rate", 160)
    engine.say(text)
    engine.runAndWait()


def audio_callback(in_data, frame_count, time_info, status):
    audio = np.frombuffer(in_data, dtype=np.float32)
    rms = librosa.feature.rms(y=audio).mean()
    now = time.time()

    if now < state["ignore_until"]:
        return (in_data, pyaudio.paContinue)

    if rms > 0.025:
        if not state["is_speaking"]:
            print("[Speech Started] Listening...")
        state["is_speaking"] = True
        state["silence_started_at"] = None
        state["audio_queue"].put(audio.copy())

    else:  # Silence
        if state["is_speaking"]:
            if state["silence_started_at"] is None:
                state["silence_started_at"] = now

            if state["silence_started_at"] and (
                now - state["silence_started_at"] >= 4.0
            ):
                state["is_speaking"] = False
                state["audio_queue"].put(None)
                state["silence_started_at"] = None
                state["ignore_until"] = now + 5.0

    return (in_data, pyaudio.paContinue)


async def process_speech():
    current_utterance = []

    while state["is_listening"]:
        chunk = state["audio_queue"].get()  # Blocks until something arrives

        if chunk is None:  # User stopped speaking
            if current_utterance:
                full_audio = np.concatenate(current_utterance)

                # Ignore very short recordings (background noise)
                if len(full_audio) < 12000:  # < ~0.75 sec
                    current_utterance.clear()
                    continue

                print("You finished speaking → Transcribing...")
                text = await transcribe_audio(full_audio)
                # 2. Ignore Whisper hallucinations on near-silence
                if (
                    not text
                    or len(text) <= 4
                    or text.lower() in {"thank you", "yeah", "okay", "yes", "no", "um"}
                ):
                    print("→ Too short or hallucinated – ignoring")
                    current_utterance.clear()
                    continue
                state["ignore_until"] = 0.0
                # ← NEW: Detect emotion from TEXT here
                state["current_emotion"] = detect_text_emotion(text)

                print(f"USER: {text} | Emotion: {state['current_emotion'].upper()}")
                response = generate_response(text, state["current_emotion"])
                print(f"AGENT: {response}")
                await speak_text(response)
                current_utterance = []  # Reset
        else:
            if chunk is not None:
                current_utterance.append(chunk)

        await asyncio.sleep(0.01)


def start_agent():
    global loop
    state["is_listening"] = True
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Create task and keep reference
    task = loop.create_task(process_speech())

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
        stream_callback=audio_callback,
    )
    stream.start_stream()

    print("\nFEMALE EMOTIONAL SUPPORT AI IS READY")
    print("Speak naturally — I wait 4 seconds of silence")
    print("Press Ctrl+C to stop\n")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Take care of yourself")
    finally:
        state["is_listening"] = False
        # Stop audio
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        p.terminate()

        # Cancel task WITHOUT restarting the loop
        task.cancel()

        loop.stop()  # ← Stop any running
        loop.close()  # ← Close cleanly


if __name__ == "__main__":
    start_agent()
