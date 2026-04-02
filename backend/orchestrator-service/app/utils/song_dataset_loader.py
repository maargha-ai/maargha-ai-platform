import ast
from typing import List
import pandas as pd
from io import BytesIO

from google.cloud import storage


def load_songs_from_excel(path: str, bucket_name: str) -> List[dict]:
    """Load songs from Excel stored in GCS"""

    if path == "dummy":
        return []

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(path)

    # 🔥 Download file into memory
    excel_bytes = blob.download_as_bytes()

    # Read using pandas
    df = pd.read_excel(BytesIO(excel_bytes))

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