from transformers import MarianMTModel, MarianTokenizer
import logging
import os
from typing import Dict, List, Tuple
import torch

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class HuggingFaceTranslationService:
    def __init__(self):
        self.models: Dict[str, Tuple[MarianTokenizer, MarianMTModel]] = {}
        self.language_models = settings.HUGGINGFACE_LANGUAGE_MODELS
        self.cache_dir = settings.MODEL_CACHE_DIR
        
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported target languages"""
        return [
            {"code": code, "model": model_name}
            for code, model_name in self.language_models.items()
        ]
    
    def load_model(self, target_lang: str) -> Tuple[MarianTokenizer, MarianMTModel]:
        """Load model and tokenizer for the specified target language"""
        if target_lang not in self.language_models:
            raise ValueError(f"Unsupported target language: {target_lang}")
        
        model_name = self.language_models[target_lang]
        
        if model_name not in self.models:
            logger.info(f"Loading model for {target_lang}: {model_name}")
            try:
                tokenizer = MarianTokenizer.from_pretrained(
                    model_name, 
                    cache_dir=self.cache_dir
                )
                model = MarianMTModel.from_pretrained(
                    model_name, 
                    cache_dir=self.cache_dir
                )
                self.models[model_name] = (tokenizer, model)
                logger.info(f"Successfully loaded model for {target_lang}")
            except Exception as e:
                logger.error(f"Failed to load model for {target_lang}: {str(e)}")
                raise
        
        return self.models[model_name]
    
    def translate(self, text: str, target_lang: str) -> str:
        """Translate text to the specified target language"""
        # Skip empty or whitespace-only strings
        if not text or text.isspace():
            return text
        
        try:
            tokenizer, model = self.load_model(target_lang)
            
            # Handle long text by breaking it into chunks if needed
            max_length = tokenizer.model_max_length
            if len(text) > max_length:
                return self._translate_long_text(text, target_lang, tokenizer, model)
            
            # Tokenize and translate
            inputs = tokenizer(text, return_tensors="pt", padding=True)
            with torch.no_grad():
                translated = model.generate(**inputs)
            
            # Decode and return result
            result = tokenizer.decode(translated[0], skip_special_tokens=True)
            return result
            
        except Exception as e:
            logger.error(f"Translation error for target language {target_lang}: {str(e)}")
            # Return original text on error to avoid breaking the document
            return text
    
    def _translate_long_text(
        self, text: str, target_lang: str, tokenizer: MarianTokenizer, model: MarianMTModel
    ) -> str:
        """Handle translation of long text by breaking it into smaller chunks"""
        # Simple sentence splitting based on common punctuation
        sentences = []
        current = ""
        
        # Split by common sentence terminators
        for char in text:
            current += char
            if char in ['.', '!', '?', ';'] and len(current) > 10:
                sentences.append(current)
                current = ""
        
        if current:
            sentences.append(current)
        
        # Translate each sentence
        translated_parts = []
        for sentence in sentences:
            inputs = tokenizer(sentence, return_tensors="pt", padding=True)
            with torch.no_grad():
                translated = model.generate(**inputs)
            result = tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_parts.append(result)
        
        # Join the translated sentences
        return " ".join(translated_parts)