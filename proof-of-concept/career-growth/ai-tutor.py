from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from sentence_transformers import SentenceTransformer

PDF_PATH = "books/Hands-On-Machine-Learning.pdf"
VECTOR_DB_PATH = "vectordb/tutor_faiss"


class LocalSentenceEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            cache_folder="./models"
        )

    def embed_documents(self, texts):
        return self.model.encode(
            texts,
            convert_to_numpy=True
        ).tolist()

    def embed_query(self, text):
        return self.model.encode(
            text,
            convert_to_numpy=True
        ).tolist()


def build_and_save_vectordb():
    print("[POC] Loading textbook PDF...")

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    embeddings = LocalSentenceEmbeddings()

    print("[POC] Creating FAISS index...")
    vectordb = FAISS.from_documents(chunks, embeddings)

    print("[POC] Saving FAISS index to disk...")
    vectordb.save_local(VECTOR_DB_PATH)

    print("[POC] Vector DB build complete ✅")


if __name__ == "__main__":
    build_and_save_vectordb()
