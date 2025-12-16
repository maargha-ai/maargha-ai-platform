# app/storage/local_storage.py
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]
ROADMAP_DIR = BASE_DIR / "static" / "roadmaps"

ROADMAP_DIR.mkdir(parents=True, exist_ok=True)

def save_roadmap_video(temp_path: str, user_id: str) -> str:
    user_dir = ROADMAP_DIR / user_id
    user_dir.mkdir(parents=True, exist_ok=True)

    dest = user_dir / "roadmap.mp4"

    shutil.move(temp_path, dest)

    return f"/static/roadmaps/{user_id}/roadmap.mp4"
