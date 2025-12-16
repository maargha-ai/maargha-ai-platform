""" Settings loader """

from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Orchestrator-service"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # User service
    USER_SERVICE_URL: AnyUrl = Field(env="USER_SERVICE_URL")
    USER_SERVICE_API_KEY: Optional[str] = None

    DATABASE_URL: str = Field(env="DATABASE_URL")
    GROQ_API_KEY: str

    # LLM / AI provider
    LLM_PROVIDER: str = Field(env="LLM_PROVIDER")
    OPENAI_API_KEY: Optional[str] = Field(env="OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = Field(env="GROQ_API_KEY")
    LLM_BASE_URL: Optional[AnyUrl] = None  # if using custom endpoint

    # Playwright / scraping config
    PLAYWRIGHT_HEADLESS: bool = True

    # Timeouts & retries
    HTTP_TIMEOUT_SECONDS: int = 30
    HTTP_RETRIES: int = 2

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()