import json
import logging
import boto3
from typing import Dict, List, Optional
from botocore.exceptions import ClientError

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class BedrockTranslationService:
    def __init__(self):
        self.supported_languages = {
            "fi": "Finnish",
            "sv": "Swedish",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "ja": "Japanese",
            "zh": "Chinese",
            "ko": "Korean",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "ru": "Russian",
            "pl": "Polish",
            "ar": "Arabic",
            "hi": "Hindi",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "tr": "Turkish",
            "cs": "Czech",
            "da": "Danish",
            "no": "Norwegian",
            "el": "Greek"
        }
        
        # Initialize AWS Bedrock client
        self._client = None
        
        # Set the Claude model to use
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # Use the latest Claude model available

    @property
    def client(self):
        """Lazy-loading property for AWS Bedrock client"""
        if self._client is None:
            self._client = self._initialize_bedrock_client()
        return self._client
        

    def _initialize_bedrock_client(self):
        """Initialize and return the AWS Bedrock client"""
        # Check if AWS credentials are available
        if not all([
            settings.AWS_REGION,
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY
        ]):
            logger.error(
                "AWS Bedrock client initialization failed: Missing AWS credentials. "
                "Please set AWS_REGION, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY "
                "environment variables."
            )
            return None
            
        try:
            session = boto3.Session(
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            
            client = session.client(service_name='bedrock-runtime')
            return client
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock client: {str(e)}")
            return None
            
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported target languages"""
        return [
            {"code": code, "name": name}
            for code, name in self.supported_languages.items()
        ]
    
    def translate(self, text: str, target_lang: str) -> str:
        """Translate text to the specified target language using Claude"""
        # Skip empty or whitespace-only strings
        if not text or text.isspace():
            return text
        
        # Check if target language is supported
        if target_lang not in self.supported_languages:
            logger.warning(f"Unsupported target language: {target_lang}")
            return text
            
        # Check if client is initialized
        if not self.client:
            logger.error("AWS Bedrock client is not initialized")
            return text
            
        try:
            # Prepare the prompt for Claude
            language_name = self.supported_languages[target_lang]
            
            prompt = f"""
            Translate the following English text to {language_name}. 
            Maintain the exact meaning and tone. Preserve any HTML/XML tags or placeholders.
            
            Text to translate:
            {text}
            
            Translation:
            """
            
            # Prepare request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Invoke Claude model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            translated_text = response_body['content'][0]['text']
            
            # Clean up the response if needed
            translated_text = translated_text.strip()
            
            return translated_text
            
        except ClientError as e:
            logger.error(f"AWS Bedrock client error: {str(e)}")
            return text
        except Exception as e:
            logger.error(f"Translation error using AWS Bedrock: {str(e)}")
            return text



    def translate(self, text: str, target_lang: str) -> str:
        """Translate text to the specified target language using Claude"""
        # Skip empty or whitespace-only strings
        if not text or text.isspace():
            return text
        
        # Check if target language is supported
        if target_lang not in self.supported_languages:
            logger.warning(f"Unsupported target language: {target_lang}")
            return text
            
        # Check if client is initialized
        if not self.client:
            error_msg = "AWS Bedrock client is not initialized. Check your AWS credentials."
            logger.error(error_msg)
            # Instead of silently falling back, we could raise an exception
            # that would be caught at the endpoint level
            # raise RuntimeError(error_msg)
            return text
        
        try:
            # ... rest of the method remains the same ...
            
        except ClientError as e:
            error_code = e.response['Error']['Code'] if 'Error' in e.response else 'Unknown'
            error_msg = e.response['Error']['Message'] if 'Error' in e.response else str(e)
            
            if error_code == 'ThrottlingException':
                logger.error(f"AWS Bedrock rate limit exceeded: {error_msg}")
            elif error_code in ('AccessDeniedException', 'UnrecognizedClientException'):
                logger.error(f"AWS Bedrock authentication error: {error_msg}")
            elif error_code == 'ValidationException':
                logger.error(f"AWS Bedrock validation error: {error_msg}")
            else:
                logger.error(f"AWS Bedrock error ({error_code}): {error_msg}")
                
            return text

