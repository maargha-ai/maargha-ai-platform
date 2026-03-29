import random

from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.core.embeddings import embedder  # shared model
from app.utils.gcs import generate_signed_url
from app.utils.song_dataset_loader import load_songs_from_excel


class MusicRecommendationChain:
    def __init__(self):
        self.songs = load_songs_from_excel(settings.SONG_PATH)

        # Pre-compute embeddings ONCE
        self.song_embeddings = [
            embedder.encode(song["emotion_tags"]) for song in self.songs
        ]

    def recommend(self, emotions: list[str]):
        user_embs = embedder.encode(emotions)

        scored_songs = []

        for song, song_embs in zip(self.songs, self.song_embeddings):
            total_score = 0.0
            count = 0

            for u_emb in user_embs:
                for s_emb in song_embs:
                    total_score += cosine_similarity([u_emb], [s_emb])[0][0]
                    count += 1

            avg_score = total_score / count if count else 0.0
            scored_songs.append((avg_score, song))

        scored_songs.sort(key=lambda x: x[0], reverse=True)

        selected_score, selected_song = random.choice(scored_songs[:3])

        return {
            "title": selected_song["title"],
            "audio_url": generate_signed_url(
                settings.GCP_BUCKET_NAME, selected_song["gcs_object"]
            ),
            "score": float(selected_score),
            "song_emotions": selected_song["emotion_tags"],
        }
