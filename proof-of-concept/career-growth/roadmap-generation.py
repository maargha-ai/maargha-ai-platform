from groq import Groq
from dotenv import load_dotenv
import os
import json
from TTS.api import TTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# Generate Roadmap Script using Groq 
client = Groq(api_key=os.getenv("career-growth"))

def generate_roadmap_script(career: str):
    prompt = f"""
    Create a short 6-slide educational video script explaining the career path of {career}. 
    For each slide include:
    - Title
    - 2-3 bullet points
    - Short voiceover narration

    Respond in JSON:
    [
     {{
        "title": "...",
        "bullets": ["...", "..."],
        "voiceover": "..."
     }}
    ]
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return json.loads(response.choices[0].message.content)


# Convert Voiceover to Audio (Coqui TTS)
tts = TTS(modelname="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def generate_slide_audio(slide_text: str, index: int):
    output_path = f"audio_{index}.wav"
    tts.tts_to_file(text=slide_text, file_path=output_path)
    return output_path


# Generate Images for Each Slide (Pillow)
def generate_slide_image(title:str, bullets: list, index: int):
    img = Image.new("RGB", (1280, 720), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("arial.ttf", 60)
    font_text = ImageFont.truetype("arial.ttf", 40)

    # Title
    draw.text((50, 50), title, fill="white", font=font_title)

    # Bullets
    y = 200
    for b in bullets:
        draw.text((80, y), f"- {b}", fill="white", font=font_text)
        y+= 80

    filepath = f"slide_{index}.png"
    img.save(filepath)
    return filepath


# Combine Audio + Images Into a Video
def assemble_video(slide_assets):
    clips = []
    for img_path, audio_path in slide_assets:
        audio = AudioFileClip(audio_path)
        clip = ImageClip(img_path).set_duration(audio.duration).set_audio(audio)
        clips.append(clip)

    final = concatenate_videoclips(clips)
    final.write_videofile("career_overview.mp4", fps=24)