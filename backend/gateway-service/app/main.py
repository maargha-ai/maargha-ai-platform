from fastapi import FastAPI
from app.routes import auth, orchestrator_ws
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
