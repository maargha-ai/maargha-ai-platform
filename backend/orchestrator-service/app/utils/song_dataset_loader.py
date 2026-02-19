import ast

import pandas as pd


def load_songs_from_excel(path: str):
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
