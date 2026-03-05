from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentic SQL Assistant"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    DEBUG: bool = False
    
    # App State DB (Postgres)
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    
    # Target SQL Server (Read Only)
    SQL_SERVER_HOST: str
    SQL_SERVER_DB: str
    SQL_SERVER_USER: str
    SQL_SERVER_PASSWORD: str
    SQL_SERVER_DRIVER: str = "ODBC Driver 17 for SQL Server"
    
    # AI
    OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_DEPLOYMENT_NAME: str = "gpt-4"
    MAX_TOKENS: int = 4000
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "100/minute"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
