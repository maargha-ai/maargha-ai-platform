# app/core/langchain_embeddings.py
from app.services.ml_client import get_embeddings


class LangchainSentenceEmbeddings:
    def embed_documents(self, texts):
        result = get_embeddings(texts)
        return result["embeddings"]

    def embed_query(self, text):
        result = get_embeddings(text)
        return result["embedding"]

    def __call__(self, input):
        if isinstance(input, str):
            return self.embed_query(input)
        elif isinstance(input, list):
            return self.embed_documents(input)
        else:
            raise ValueError("Input must be str or list of str")