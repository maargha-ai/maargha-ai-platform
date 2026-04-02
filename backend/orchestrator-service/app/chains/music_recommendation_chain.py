import random
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.services.ml_client import get_embeddings
from app.utils.gcs import generate_signed_url
from app.utils.song_dataset_loader import load_songs_from_excel


class MusicRecommendationChain:
    def __init__(self):
        self.songs = load_songs_from_excel(
                    settings.SONG_PATH,
                    settings.GCP_BUCKET_NAME
                )
        self.song_embeddings = []

        self._initialize_embeddings()  # 🔥 Precompute once

    def _initialize_embeddings(self):
        print("⚡ Precomputing song embeddings...")

        # Collect all emotion tags
        all_tags = [song["emotion_tags"] for song in self.songs]

        # 🔥 Batch embedding (FAST)
        results = get_embeddings(all_tags)["embeddings"]

        # Convert to numpy for faster computation later
        self.song_embeddings = [np.array(emb) for emb in results]

        print(f"✅ Loaded embeddings for {len(self.song_embeddings)} songs")

    async def recommend(self, emotions: list[str]):

        # 🔥 Embed user emotions (small → fine to do per request)
        user_embs = get_embeddings(emotions)["embeddings"]
        user_embs = [np.array(e) for e in user_embs]

        scored_songs = []

        for song, song_emb in zip(self.songs, self.song_embeddings):

            total_score = 0.0
            count = 0

            for u_emb in user_embs:
                score = cosine_similarity([u_emb], [song_emb])[0][0]
                total_score += score
                count += 1

            avg_score = total_score / count if count else 0.0
            scored_songs.append((avg_score, song))

        # Sort by score
        scored_songs.sort(key=lambda x: x[0], reverse=True)

        # Pick randomly from top 3
        selected_score, selected_song = random.choice(scored_songs[:3])

        return {
            "title": selected_song["title"],
            "audio_url": generate_signed_url(
                settings.GCP_BUCKET_NAME,
                selected_song["gcs_object"]
            ),
            "score": float(selected_score),
            "song_emotions": selected_song["emotion_tags"],
        }