import ast
from typing import List

import pandas as pd


def load_songs_from_excel(path: str) -> List[dict]:
    """Load songs from Excel file, return empty list if path is dummy"""
    if path == "dummy":
        return []

    df = pd.read_excel(path)

    songs = []
    for _, row in df.iterrows():
        songs.append(
            {
                "title": row["Title"],
                "gcs_object": row["Path"],
                "emotion_tags": [
                    e.lower() for e in ast.literal_eval(row["Emotion_Tags"])
                ],
            }
        )

    return songs
