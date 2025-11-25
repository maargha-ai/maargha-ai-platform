from groq import Groq
from dotenv import load_dotenv
import os
import json
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from io import BytesIO
import tempfile

load_dotenv()
# Generate Roadmap Script using Groq 
client = Groq(api_key=os.getenv("career-growth"))

def generate_roadmap_script(career: str):
    prompt = f"""
    Create a short 6-slide educational video script explaining the career path of {career}. 
    For each slide include:
    - Title
    - 2-3 bullet points
    - Short voiceover narration

    Return ONLY a JSON array in this format:
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


# Convert Voiceover to Audio (Coqui TTS), this is in memory and not saved
def generate_audio_bytes(slide_text: str):
    audio_bytes = BytesIO()
    tts = gTTS(text=slide_text, lang="en")
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes


# Generate a Cartoon-style Slide with Auto-Text Wrapping (In-Memory)
def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""

    for word in words:
        test_line = current + " " + word
        if draw.textlength(test_line, font=font) <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


# Generate Images for Each Slide (Pillow)
def generate_slide_image(title:str, bullets: list):
    width, height = 1280, 720

    # Cartoon gradient background
    img = Image.new("RGB", (width, height), color=(60, 120, 200))
    draw = ImageDraw.Draw(img)

    # Cartoon fonts (fallback to default if not found)
    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_bullet = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_bullet = ImageFont.load_default()

    # Draw Title
    draw.text((50, 40), title, fill="yellow", font=font_title)

    # Draw bullets with auto-wrap
    max_width = width - 100
    y = 200

    for b in bullets:
        lines = wrap_text(draw, f"- {b}", font_bullet, max_width)
        for line in lines:
            draw.text((80, y), line, fill="white", font=font_bullet)
            y += 60

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


# Combine Audio + Images Into a Video (no temp files saved)
def assemble_video(slides):
    video_clips = []

    for image_bytes, audio_bytes in slides:

        # Write audio to temp file for moviepy
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
            audio_file.write(audio_bytes.read())
            audio_file.seek(0)
            audio_path = audio_file.name

        audio_clip = AudioFileClip(audio_path)

        # Write image to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_file:
            img_file.write(image_bytes.read())
            img_file.seek(0)
            img_path = img_file.name

        image_clip = (
            ImageClip(img_path)
            .with_duration(audio_clip.duration)
            .with_audio(audio_clip)
        )

        video_clips.append(image_clip)

    final = concatenate_videoclips(video_clips)
    final.write_videofile("career_overview.mp4", fps=24)


# Full Pipeline Execution
def generate_career_video(career: str):
    slides_data = generate_roadmap_script(career)
    slide_assets = []

    for slide in slides_data:
        image_bytes = generate_slide_image(slide["title"], slide["bullets"])
        audio_bytes = generate_audio_bytes(slide["voiceover"])
        slide_assets.append((image_bytes, audio_bytes))
    
    assemble_video(slide_assets)
    print("Video generated: career_overview.mp4")


if __name__ == "__main__":
    generate_career_video("Data Science")