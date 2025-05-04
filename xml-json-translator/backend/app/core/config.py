# app/core/config.py
import os
from typing import Dict, List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "XML Translator API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Environment and logging
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Translation model settings
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "/tmp/huggingface")
    
    # Hugging Face models configuration
    HUGGINGFACE_LANGUAGE_MODELS: Dict[str, str] = {
        "fi": "Helsinki-NLP/opus-mt-en-fi",  # English to Finnish
        "sv": "Helsinki-NLP/opus-mt-en-sv",  # English to Swedish
        "de": "Helsinki-NLP/opus-mt-en-de",  # English to German
        "fr": "Helsinki-NLP/opus-mt-en-fr",  # English to French
        "es": "Helsinki-NLP/opus-mt-en-es",  # English to Spanish
    }
    
    # AWS Bedrock configuration - ONLY from environment variables
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # Service selection (huggingface or bedrock)
    TRANSLATION_SERVICE: str = os.getenv("TRANSLATION_SERVICE", "huggingface")

    class Config:
        case_sensitive = True
        env_file = ".env"  # Read from .env file

    def validate(self) -> bool:
        """Validate important configuration settings"""
        if self.TRANSLATION_SERVICE.lower() == "bedrock":
            if not all([
                self.AWS_REGION,
                self.AWS_ACCESS_KEY_ID,
                self.AWS_SECRET_ACCESS_KEY
            ]):
                logger.warning(
                    "AWS Bedrock service selected but credentials are incomplete. "
                    "Make sure AWS_REGION, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY "
                    "are all provided in environment variables."
                )
                return False
        return True


@lru_cache()
def get_settings():
    settings = Settings()
    settings.validate()
    return settings