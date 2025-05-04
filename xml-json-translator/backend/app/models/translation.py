from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class Language(BaseModel):
    """Language model for API responses"""
    code: str
    name: Optional[str] = None
    model: Optional[str] = None


class SupportedLanguagesResponse(BaseModel):
    """Response model for supported languages endpoint"""
    languages: List[Language]


class TranslationRequest(BaseModel):
    """Request model for translation"""
    target_language: str = Field(..., description="Target language code")
    service_type: Optional[str] = Field(None, description="Translation service type (huggingface or bedrock)")


class TranslationResponse(BaseModel):
    """Response model for translation"""
    success: bool = True
    message: str = "Translation successful"
    filename: Optional[str] = None
    download_url: Optional[str] = None