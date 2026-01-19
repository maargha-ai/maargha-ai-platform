# app/chains/tutor_chain.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

from app.core.llm_client import llm
from app.core.langchain_embeddings import LangchainSentenceEmbeddings

_retriever = None
_tutor_chain = None


def build_vector_db(pdf_path="app/static/books/Hands-On-Machine-Learning.pdf"):
    print("[Tutor] Loading textbook...")

    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(docs)

        embeddings = LangchainSentenceEmbeddings()

        vectordb = FAISS.from_documents(chunks, embeddings)

        return vectordb.as_retriever(
            search_type="similarity",
            k=4
        )
    except Exception as e:
        print(f"[Tutor] Failed with exception {e}")


def build_tutor_chain(retriever):
    prompt = PromptTemplate.from_template(
        """
        You are an AI Tutor teaching IT concepts clearly and simply.
        Use ONLY the provided context from the textbook.

        Question: {input}

        CONTEXT:
        {context}

        Your response must include:
        - Beginner-level explanation
        - Real-world analogy
        - 3-step learning plan
        - A short quiz with answers
        """
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, document_chain)


def get_tutor_chain():
    global _retriever, _tutor_chain

    if _tutor_chain is None:
        print("[Tutor] Initializing RAG tutor (one-time)")
        _retriever = build_vector_db()
        print("[Tutor] Sucessfully retrieved vectorDB")
        _tutor_chain = build_tutor_chain(_retriever)
        print("[Tutor] Sucessfully build Tutor Chain")

    return _tutor_chain


def ask_tutor(question: str) -> str:
    chain = get_tutor_chain()
    response = chain.invoke({"input": question})
    return response["answer"]
