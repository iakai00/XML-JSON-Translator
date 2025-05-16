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
        "it": "Helsinki-NLP/opus-mt-en-it",  # English to Italian
        "nl": "Helsinki-NLP/opus-mt-en-nl",  # English to Dutch
        "pl": "Helsinki-NLP/opus-mt-en-pl",  # English to Polish
        "pt": "Helsinki-NLP/opus-mt-en-pt",  # English to Portuguese
        "ru": "Helsinki-NLP/opus-mt-en-ru",  # English to Russian
    }
    
    # Claude API configuration
    CLAUDE_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    # Service selection (huggingface or claude)
    TRANSLATION_SERVICE: str = os.getenv("TRANSLATION_SERVICE", "huggingface")

    class Config:
        case_sensitive = True
        env_file = ".env"  # Read from .env file

    def validate(self) -> bool:
        """Validate important configuration settings"""
        if self.TRANSLATION_SERVICE.lower() == "claude":
            if not self.CLAUDE_API_KEY:
                logger.warning(
                    "Claude API service selected but API key is missing. "
                    "Make sure CLAUDE_API_KEY is provided in environment variables."
                )
                return False
        return True

@lru_cache()
def get_settings():
    settings = Settings()
    settings.validate()
    return settings