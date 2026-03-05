import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "mock-key")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "https://mock.openai.azure.com/")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    API_VERSION: str = "2024-02-15-preview"
    
    SQL_SERVER_CONNECTION_STRING: str = os.getenv("SQL_SERVER_CONNECTION_STRING", "sqlite:///./mock_enterprise.db")
    
    class Config:
        env_file = ".env"

settings = Settings()
