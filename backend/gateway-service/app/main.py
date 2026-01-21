from fastapi import FastAPI
from app.routes import (
    auth, orchestrator_ws, quiz_ws, 
    emotional_support_ws, song_recommend, career_ws,
    roadmap, jobs, news, linkedin, tutor_ws, cv
    )
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MAARGHA Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(orchestrator_ws.router)
app.include_router(quiz_ws.router)
app.include_router(emotional_support_ws.router)
app.include_router(song_recommend.router)
app.include_router(career_ws.router)
app.include_router(roadmap.router)
app.include_router(jobs.router)
app.include_router(news.router)
app.include_router(linkedin.router)
app.include_router(tutor_ws.router)
app.include_router(cv.router)