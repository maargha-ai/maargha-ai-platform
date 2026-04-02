from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.middleware import logging_middleware
from app.monitoring.health import router as health_router

# Import monitoring and logging
from app.monitoring.logger import LoggingMiddleware
from app.routes import (
    auth,
    career_ws,
    cv,
    emotional_support_ws,
    jobs,
    linkedin,
    news,
    orchestrator_ws,
    quiz_ws,
    resume_parser,
    roadmap,
    song_recommend,
    tutor_ws,
)

app = FastAPI(title="MAARGHA Gateway")

# Middleware
app.middleware("http")(logging_middleware)

# Add structured logging middleware
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health check endpoints
app.include_router(health_router)

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
app.include_router(resume_parser.router)

# Monitoring
Instrumentator().instrument(app).expose(app)
