from sentence_transformers import SentenceTransformer

print("Loading sentence embedding model...")

embedder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./models"
)

print("entence embedding model ready")
