import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
    ORCHESTRATOR_SERVICE_URL = os.getenv("ORCHESTRATOR_SERVICE_URL")
    ORCHESTRATOR_SERVICE_WS_URL = os.getenv("ORCHESTRATOR_SERVICE_WS_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = "HS256"


settings = Settings()