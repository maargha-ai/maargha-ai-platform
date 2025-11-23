from groq import Groq
from dotenv import load_dotenv
import os
import json
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

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
def generate_slide_audio(slide_text: str, index: int):
    output_path = f"audio_{index}.wav"
    tts = gTTS(text=slide_text, lang="en")
    tts.save(output_path)
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


# Full Pipeline Execution
def generate_career_video(career: str):
    slides = generate_roadmap_script(career)
    slide_assets = []

    for i, slide in enumerate(slides):
        img_path = generate_slide_image(slide["title"], slide["bullets"], i)
        audio_path = generate_slide_audio(slide["voiceover"], i)
        slide_assets.append((img_path, audio_path))

    assemble_video(slide_assets)
    print("Video generated: roadmap_overview.mp4")


if __name__ == "__main__":
    generate_career_video("Data Science")