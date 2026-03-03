# app/chains/jobs_chain.py
import asyncio

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.workers.jobs_scraper_worker import scrape_jobs_sync


def extract_cv_text(path: str):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + ""
        return text.lower()
    except Exception as e:
        print(f"CV Read Error: {e}")
        return ""


def match_and_rank(cv_text: str, jobs: list):
    if not cv_text or not jobs:
        return []
    vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2), max_features=10000
    )
    try:
        texts = [cv_text] + [f"{j['title']} {j['company']}".lower() for j in jobs]
        matrix = vectorizer.fit_transform(texts)
        similarities = cosine_similarity(matrix[0:1], matrix[1:])[0]
        ranked = [(sim, job) for sim, job in zip(similarities, jobs)]
        ranked.sort(key=lambda x: x[0], reverse=True)
        return ranked[:50]
    except Exception:
        return [(0.0, job) for job in jobs[:50]]


async def find_jobs_for_cv(cv_path: str, role: str, location: str, max_jobs: int = 200):
    print("   JOB MATCHER   ")
    cv_text = extract_cv_text(cv_path)
    if not cv_text:
        return []

    jobs = await asyncio.to_thread(scrape_jobs_sync, role, location, 100)
    if not jobs:
        return []
    ranked = match_and_rank(cv_text, jobs)

    return ranked[:20]
