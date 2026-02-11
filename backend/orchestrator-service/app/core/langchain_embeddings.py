# app/core/langchain_embeddings.py
from app.core.embeddings import embedder

class LangchainSentenceEmbeddings:
    def embed_documents(self, texts):
        return embedder.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        return embedder.encode(text, convert_to_numpy=True).tolist()

    def __call__(self, input):
        """Make the class callable like a function for compatibility with FAISS"""
        if isinstance(input, str):
            return self.embed_query(input)
        elif isinstance(input, list):
            return self.embed_documents(input)
        else:
            raise ValueError("Input must be str or list of str")