import logging
import requests
import json
import os
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

class ClaudeTranslationService:
    def __init__(self):
        self.supported_languages = {
            "fi": "Finnish",
            "sv": "Swedish",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "it": "Italian",
            "pt": "Portuguese", 
            "nl": "Dutch",
            "ru": "Russian",
            "pl": "Polish",
            "ja": "Japanese",
            "zh": "Chinese"
        }
        
        # Get API key from environment variable
        from app.core.config import get_settings
        settings = get_settings()
        self.api_key = settings.CLAUDE_API_KEY or os.environ.get("CLAUDE_API_KEY", "")
        
        # Use a simpler model name - more likely to work
        self.model = settings.CLAUDE_MODEL or "claude-3-sonnet"
        
        # Increased timeout for API calls (120 seconds)
        self.timeout = 120
        
        # Patterns to detect and remove common Claude explanations
        self.explanation_patterns = [
            r"^Here\'s the (English|text) translated to [^:]+:(\s*)",
            r"^Here is the translation( to [^:]+)?:(\s*)",
            r"^Translated to [^:]+:(\s*)",
            r"^Translation:(\s*)",
            r"^Here\'s the translation:(\s*)",
            r"^I've translated the (English text|text|content) (into|to) [^:.]+:?(\s*)",
            r"^The (XML|translation|text) translated to [^:]+:(\s*)",
        ]
        
        # Compile the patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in self.explanation_patterns]
        
        if not self.api_key:
            logger.error("No Claude API key found! Translation will not work.")
        else:
            logger.info(f"Claude service initialized with model: {self.model}")
            logger.info(f"Using timeout of {self.timeout} seconds")
        
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported target languages"""
        return [
            {"code": code, "name": name}
            for code, name in self.supported_languages.items()
        ]
    
    def _clean_response(self, text: str) -> str:
        """Remove explanatory text that Claude might add to translations"""
        # Apply all the patterns to remove any explanatory text
        cleaned_text = text
        
        for pattern in self.compiled_patterns:
            match = pattern.match(cleaned_text)
            if match:
                # Remove the matched pattern from the start of the text
                logger.debug(f"Removing explanatory text: {cleaned_text[:match.end()]}")
                cleaned_text = cleaned_text[match.end():]
                break  # Stop after first match
        
        # Also remove any final "Here's the translated XML:" type text if present
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text
    
    def translate(self, text: str, target_lang: str) -> str:
        """Translate text to the specified target language using Claude"""
        # Skip empty strings
        if not text or text.isspace():
            return text
        
        # Check if target language is supported
        if target_lang not in self.supported_languages:
            logger.warning(f"Unsupported target language: {target_lang}")
            return text
            
        # Check if API key is available
        if not self.api_key:
            logger.error("Claude API key is not set")
            return text
        
        try:
            # Get language name
            language_name = self.supported_languages[target_lang]
            logger.info(f"Translating to {language_name}, text length: {len(text)}")
            
            # For small texts, we can translate directly
            if len(text) < 4000:
                return self._translate_chunk(text, target_lang, language_name)
                
            # For larger texts, we need to split into chunks
            logger.info(f"Text is too long ({len(text)} chars), splitting into chunks")
            chunks = self._split_text(text)
            translated_chunks = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Translating chunk {i+1} of {len(chunks)}")
                translated_chunk = self._translate_chunk(chunk, target_lang, language_name)
                translated_chunks.append(translated_chunk)
                
            # Join the translated chunks
            result = " ".join(translated_chunks)
            logger.info(f"Finished translating all chunks, final length: {len(result)}")
            return result
                
        except Exception as e:
            logger.exception(f"Error in translation: {str(e)}")
            return text
            
    def _split_text(self, text: str, max_chunk_size: int = 3500) -> List[str]:
        """Split text into chunks, trying to preserve XML structure"""
        chunks = []
        current_chunk = ""
        
        # Try to split at XML tag boundaries
        import re
        parts = re.split(r'(<[^>]*>)', text)
        
        for part in parts:
            # If adding this part would exceed the limit, start a new chunk
            if len(current_chunk) + len(part) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = part
            else:
                current_chunk += part
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
            
    def _translate_chunk(self, text: str, target_lang: str, language_name: str = None) -> str:
        """Translate a single chunk of text using Claude"""
        if language_name is None:
            language_name = self.supported_languages[target_lang]
            
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Use a very explicit prompt to avoid Claude adding explanations
        data = {
            "model": self.model,
            "max_tokens": 4000,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Translate this English text to {language_name}.
                    DO NOT add any introduction, explanation, or comments.
                    DO NOT include phrases like "Here's the translation".
                    DO NOT modify any XML tags or placeholders.
                    ONLY return the translated content, nothing else.
                    
                    Text to translate:
                    {text}
                    """
                }
            ]
        }
        
        logger.info(f"Sending request to Claude API with {self.timeout}s timeout")
        try:
            # Use increased timeout
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Claude API error ({response.status_code}): {response.text}")
                return text
                
            logger.info("Received response from Claude API")
            try:
                response_data = response.json()
                
                if 'content' in response_data and len(response_data['content']) > 0:
                    translated = response_data['content'][0]['text'].strip()
                    logger.debug(f"Raw translation response: {translated[:100]}...")
                    
                    # Clean the response to remove explanatory text
                    cleaned_translation = self._clean_response(translated)
                    logger.info(f"Cleaned translation, before: {len(translated)} chars, after: {len(cleaned_translation)} chars")
                    
                    return cleaned_translation
                else:
                    logger.error(f"Unexpected response format: {json.dumps(response_data)}")
                    return text
                    
            except json.JSONDecodeError:
                logger.error(f"Failed to parse response JSON: {response.text[:500]}")
                return text
                
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.timeout} seconds")
            return text
            
        except Exception as e:
            logger.exception(f"Unexpected error calling Claude API: {str(e)}")
            return text
            
    def translate_json_field(self, text: str, target_lang: str) -> str:
        """
        Special handling for JSON field translation to ensure cleaner output
        and better formatting for JSON specific content
        """
        # Skip empty strings
        if not text or text.isspace():
            return text
        
        # Check if target language is supported
        if target_lang not in self.supported_languages:
            logger.warning(f"Unsupported target language: {target_lang}")
            return text
            
        # Check if API key is available
        if not self.api_key:
            logger.error("Claude API key is not set")
            return text
        
        try:
            language_name = self.supported_languages[target_lang]
            
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            # JSON-specific prompt with extra emphasis on clean output
            data = {
                "model": self.model,
                "max_tokens": 1000,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        You are a specialized JSON field translator.
                        Translate this JSON text from English to {language_name}:
                        
                        {text}
                        
                        IMPORTANT: Return ONLY the translated text.
                        - NO introduction or explanation
                        - NO phrases like "Here's the translation"
                        - NO additional formatting
                        - Preserve any placeholders (like {{variable}} or __name__)
                        - Preserve any HTML/XML tags
                        """
                    }
                ]
            }
            
            logger.debug(f"Sending JSON field translation request: {text[:50]}...")
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Claude API error ({response.status_code}): {response.text}")
                return text
                
            response_data = response.json()
            
            if 'content' in response_data and len(response_data['content']) > 0:
                translated = response_data['content'][0]['text'].strip()
                
                # Extra cleaning for JSON fields
                cleaned = self._clean_json_response(translated)
                
                logger.debug(f"JSON field translation result: {cleaned[:50]}...")
                return cleaned
            else:
                logger.error(f"Unexpected response format: {json.dumps(response_data)}")
                return text
                
        except Exception as e:
            logger.exception(f"Error translating JSON field: {str(e)}")
            return text
    
    def _clean_json_response(self, text: str) -> str:
        """Extra cleaning for JSON field translations"""
        
        # First apply the standard cleaning
        cleaned = self._clean_response(text)
        
        # These patterns are more aggressive than the standard ones
        json_patterns = [
            # Remove any remaining quotes around the text
            r'^["\'](.*)["\'](\.?)$',
            # Remove any code-style formatting
            r'^```(?:json)?(.*?)```$',
            # Remove any bullet points
            r'^[-*•] (.*?)$',
            # Remove any numbering
            r'^\d+\.\s+(.*?)$'
        ]
        
        # Apply each pattern
        for pattern_str in json_patterns:
            pattern = re.compile(pattern_str, re.DOTALL)
            match = pattern.match(cleaned)
            if match:
                # Keep the period from the end if it was there
                period = match.group(2) if len(match.groups()) > 1 else ''
                cleaned = match.group(1).strip() + period
        
        return cleaned