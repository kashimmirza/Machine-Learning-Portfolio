from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Test loading .env manually first
load_dotenv()
print("Direct os.getenv check:")
print(f"GEMINI_API_KEY from os.getenv: {os.getenv('GEMINI_API_KEY')}")
print(f"GEMINI_MODEL from os.getenv: {os.getenv('GEMINI_MODEL')}")

# Now test settings
from app.core.config import settings
print("\nFrom settings object:")
print(f"gemini_api_key: {settings.gemini_api_key}")
print(f"gemini_model: {settings.gemini_model}")
print(f"ocr_provider: {settings.ocr_provider}")
