# app/chains/roadmap_chain.py
import json
import os
import tempfile
from app.core.llm_client import llm
from langchain_core.messages import HumanMessage
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

async def generate_roadmap_script(career: str):
    prompt = f"""
    Create a short 6-slide educational video script explaining the career path of {career}. 
    For each slide include:
    - Title
    - 2-3 bullet points
    - Short voiceover narration

    Return ONLY valid JSON:
    [
      {{
        "title": "...",
        "bullets": ["...", "..."],
        "voiceover": "..."
      }}
    ]
    """

    response = await llm.ainvoke([HumanMessage(content=prompt)])

    try:
        return json.loads(response.content)
    except Exception:
        return [
            {
                "title": "Introduction",
                "bullets": ["Welcome", "Overview"],
                "voiceover": "Welcome to your career roadmap."
            }
        ] * 6

def generate_slide_image(title: str, bullets: list, out_path: str):
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), (60, 120, 200))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_bullet = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_bullet = ImageFont.load_default()

    draw.text((50, 40), title, fill="yellow", font=font_title)

    y = 200
    for b in bullets:
        draw.text((80, y), f"• {b}", fill="white", font=font_bullet)
        y += 60

    img.save(out_path)


def generate_audio_file(text: str, out_path: str):
    gTTS(text=text, lang="en").save(out_path)


async def generate_roadmap_video(career: str) -> str:
    slides = await generate_roadmap_script(career)

    clips = []
    temp_files = []

    for slide in slides:
        img_fd, img_path = tempfile.mkstemp(suffix=".png")
        aud_fd, aud_path = tempfile.mkstemp(suffix=".mp3")
        os.close(img_fd)
        os.close(aud_fd)

        generate_slide_image(slide["title"], slide["bullets"], img_path)
        generate_audio_file(slide["voiceover"], aud_path)

        temp_files.extend([img_path, aud_path])

        # Re-open audio AFTER write
        audio_clip = AudioFileClip(aud_path)
        image_clip = ImageClip(img_path)

        image_clip = image_clip.with_audio(audio_clip)
        image_clip = image_clip.with_duration(audio_clip.duration)

        clips.append(image_clip)

    video_fd, temp_video_path = tempfile.mkstemp(suffix=".mp4")
    os.close(video_fd)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(temp_video_path,fps=24,audio_codec="aac")

    # CLEANUP
    for clip in clips:
        clip.audio.close()
        clip.close()

    for f in temp_files:
        try:
            os.unlink(f)
        except:
            pass

    final.close()

    return temp_video_path
