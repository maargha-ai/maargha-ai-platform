# app/core/langchain_embeddings.py
from app.core.embeddings import embedder

class LangchainSentenceEmbeddings:
    def embed_documents(self, texts):
        return embedder.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        return embedder.encode(text, convert_to_numpy=True).tolist()
