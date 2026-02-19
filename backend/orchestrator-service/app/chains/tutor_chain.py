# app/chains/tutor_chain.py

from pathlib import Path

import requests
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate

from app.core.config import settings
from app.core.langchain_embeddings import LangchainSentenceEmbeddings
from app.core.llm_client import llm
from app.utils.gcs import generate_signed_url

GCP_BUCKET_NAME = settings.GCP_TUTOR_BUCKET
GCP_VECTOR_DB_PREFIX = "tutor_faiss"

LOCAL_VECTOR_DB_PATH = Path("app/static/vectordb/tutor_faiss")
LOCAL_VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

_retriever = None


PROMPT_TEMPLATE = PromptTemplate.from_template("""
    You are an AI Tutor teaching IT concepts clearly and simply.
    Use ONLY the provided context from the textbook.

    Question:
    {question}

    CONTEXT:
    {context}

    Your response must include:
    - Beginner-level explanation
    - Real-world analogy
    - 3-step learning plan
    - A short quiz with answers
    """)


def download_vector_db():
    for filename in ["index.faiss", "index.pkl"]:
        local_file = LOCAL_VECTOR_DB_PATH / filename
        if local_file.exists():
            continue

        signed_url = generate_signed_url(
            GCP_BUCKET_NAME, f"{GCP_VECTOR_DB_PREFIX}/{filename}"
        )

        response = requests.get(signed_url, timeout=60)
        response.raise_for_status()

        with open(local_file, "wb") as f:
            f.write(response.content)


def get_retriever():
    global _retriever

    if _retriever is None:
        print("[Tutor] Loading FAISS vector DB")
        download_vector_db()

        embeddings = LangchainSentenceEmbeddings()

        vectordb = FAISS.load_local(
            folder_path=str(LOCAL_VECTOR_DB_PATH),
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )

        _retriever = vectordb.as_retriever(search_type="similarity", k=4)

        print("[Tutor] Successfully loaded vectorDB")

    return _retriever


async def ask_tutor(question: str) -> str:
    retriever = get_retriever()

    # Retrieve context
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Build prompt
    prompt = PROMPT_TEMPLATE.format(question=question, context=context)

    # Call LLM (same style as roadmap_chain)
    response = await llm.ainvoke([HumanMessage(content=prompt)])

    return response.content
