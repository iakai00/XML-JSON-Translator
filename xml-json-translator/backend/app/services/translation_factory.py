from typing import List, Dict, Union
import logging

from app.core.config import get_settings
from app.services.huggingface_service import HuggingFaceTranslationService
from app.services.claude_service import ClaudeTranslationService

logger = logging.getLogger(__name__)
settings = get_settings()

class TranslationServiceFactory:
    """Factory for creating translation service instances based on configuration"""
    
    _huggingface_instance = None
    _claude_instance = None
    
    @classmethod
    def get_service(cls, service_type: str = None):
        """
        Get the translation service based on the specified type or default configuration
        
        Args:
            service_type: Optional service type override ('huggingface' or 'claude')
        
        Returns:
            A translation service instance
        """
        # Use the specified service type or the configured default
        service_type = service_type or settings.TRANSLATION_SERVICE
        service_type = service_type.lower()
        
        if service_type == "huggingface":
            if cls._huggingface_instance is None:
                logger.info("Creating HuggingFace translation service")
                cls._huggingface_instance = HuggingFaceTranslationService()
            return cls._huggingface_instance
            
        elif service_type == "claude":
            if cls._claude_instance is None:
                logger.info("Creating Claude API translation service")
                cls._claude_instance = ClaudeTranslationService()
            return cls._claude_instance
            
        else:
            logger.warning(f"Unknown service type: {service_type}, falling back to HuggingFace")
            if cls._huggingface_instance is None:
                cls._huggingface_instance = HuggingFaceTranslationService()
            return cls._huggingface_instance
    
    @classmethod
    def get_supported_languages(cls, service_type: str = None) -> List[Dict[str, str]]:
        """
        Get supported languages from the specified service
        
        Args:
            service_type: Optional service type override
        
        Returns:
            List of supported languages with their codes and names/models
        """
        service = cls.get_service(service_type)
        return service.get_supported_languages()
    
    @classmethod
    def translate(cls, text: str, target_lang: str, service_type: str = None) -> str:
        """
        Translate text using the specified service
        
        Args:
            text: Text to translate
            target_lang: Target language code
            service_type: Optional service type override
        
        Returns:
            Translated text
        """
        service = cls.get_service(service_type)
        return service.translate(text, target_lang)
    
    @classmethod
    def translate_json_field(cls, text: str, target_lang: str, service_type: str = None) -> str:
        """
        Translate JSON field specifically, with special handling for different services
        
        Args:
            text: Text to translate
            target_lang: Target language code
            service_type: Optional service type override
        
        Returns:
            Translated text optimized for JSON fields
        """
        service = cls.get_service(service_type)
        
        # Use specialized method if available (for Claude)
        if service_type == "claude" and hasattr(service, 'translate_json_field'):
            return service.translate_json_field(text, target_lang)
        else:
            # Fall back to regular translation for other services
            return service.translate(text, target_lang)