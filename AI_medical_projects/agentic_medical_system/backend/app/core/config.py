import os
from enum import Enum
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"

class Settings(BaseSettings):
    # Application Basics
    PROJECT_NAME: str = "Agentic Medical AI System"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    APP_ENV: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True
    ALLOWED_ORIGINS: List[str] = ["*"]

    # LLM
    OPENAI_API_KEY: str
    DEFAULT_LLM_MODEL: str = "gpt-4-turbo-preview"
    DEFAULT_LLM_TEMPERATURE: float = 0.0
    MAX_TOKENS: int = 2000
    MAX_LLM_CALL_RETRIES: int = 3

    # Database
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 10
    
    # MongoDB (Agentic Data)
    MONGO_URI: str = "mongodb://localhost:27017/agentic_health"
    MONGO_DB_NAME: str = "agentic_health"

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_DAYS: int = 30

    # Langfuse
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    # Rate Limiting
    RATE_LIMIT_DEFAULT: List[str] = ["200 per day", "50 per hour"]
    RATE_LIMIT_ENDPOINTS: dict = {
        "chat": ["30 per minute"],
        "chat_stream": ["20 per minute"],
        "auth": ["20 per minute"],
        "root": ["10 per minute"],
        "health": ["20 per minute"],
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
