import os
from pydantic import BaseSettings
from typing import Dict, List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "XML Translator API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
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
    
    # AWS Bedrock configuration (for future use)
    AWS_REGION: Optional[str] = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Service selection (huggingface or bedrock)
    TRANSLATION_SERVICE: str = os.getenv("TRANSLATION_SERVICE", "huggingface")

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()