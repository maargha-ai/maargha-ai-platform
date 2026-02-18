from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import (
    auth, orchestrator_ws, quiz_ws, 
    emotional_support_ws, song_recommend, career_ws,
    roadmap, jobs, news, linkedin, tutor_ws, cv, resume_parser
    )
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import logging_middleware
from app.core.logger import logger
import time

# Import monitoring and logging
from app.monitoring.logger import LoggingMiddleware, performance_monitor, gateway_logger
from app.monitoring.health import router as health_router

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