from fastapi import FastAPI
from app.routes import auth
from app.ws import orchestrator

app = FastAPI(title="MAARGHA Gateway")

app.include_router(auth.router)
app.include_router(orchestrator.router)
