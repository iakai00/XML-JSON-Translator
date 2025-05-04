# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from transformers import pipeline, AutoTokenizer, MarianMTModel
import torch
import xml.etree.ElementTree as ET
import tempfile
import os
import logging
import warnings

# Filter out specific warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize translator
translator = None
MODEL_NAME = "Helsinki-NLP/opus-mt-en-es"

def load_model_safely():
    """Safely load the translation model with proper security settings"""
    try:
        logger.info(f"Loading model: {MODEL_NAME}")
        
        # Use simpler pipeline initialization
        return pipeline(
            "translation",
            model=MODEL_NAME,
            torch_dtype=torch.float32
        )
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def get_translator():
    """Initialize or return the translation model"""
    global translator
    if translator is None:
        try:
            translator = load_model_safely()
            logger.info("Translation model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load translator: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize translation service: {str(e)}"
            )
    return translator

def sanitize_text(text: str) -> str:
    """Sanitize input text"""
    if not text:
        return ""
    # Remove any control characters except newlines and tabs
    return ''.join(char for char in text if char.isprintable() or char in '\n\t')

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Try to load the model during health check
        get_translator()
        return {
            "status": "healthy",
            "model": "loaded",
            "model_name": MODEL_NAME
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model": "not loaded",
            "error": str(e)
        }

@app.post("/translate/")
async def translate_file(file: UploadFile = File(...)):
    """Translate XML file from English to Spanish"""
    try:
        logger.info(f"Received file: {file.filename}")
        
        # Read the uploaded file
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Parse XML
        try:
            root = ET.fromstring(content_str)
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid XML format")
        
        # Get translator
        translator = get_translator()
        
        # Translate each TEXT element
        logger.info("Starting translation...")
        translation_stats = {"success": 0, "failed": 0}
        
        for text_elem in root.findall(".//TEXT"):
            # Handle CDATA sections if present
            if len(text_elem) > 0 and text_elem[0].tag == ET.Comment:
                original_text = text_elem[0].text
            else:
                original_text = text_elem.text
                
            if original_text and original_text.strip():
                try:
                    # Sanitize input text
                    sanitized_text = sanitize_text(original_text)
                    logger.info(f"Translating: {sanitized_text[:50]}...")
                    
                    # Perform translation
                    translated = translator(
                        sanitized_text,
                        max_length=512,
                    )[0]['translation_text']
                    
                    logger.info(f"Translated to: {translated[:50]}...")
                    
                    # Update the element with translated text
                    if len(text_elem) > 0 and text_elem[0].tag == ET.Comment:
                        text_elem[0].text = translated
                    else:
                        text_elem.text = translated
                        
                    translation_stats["success"] += 1
                    
                except Exception as e:
                    logger.error(f"Translation error for text: {original_text[:50]}... Error: {str(e)}")
                    translation_stats["failed"] += 1
                    continue
        
        # Convert back to string
        translated_content = ET.tostring(root, encoding='unicode', method='xml')
        
        # Create temporary file for response
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp_file:
            tmp_file.write(translated_content.encode('utf-8'))
            tmp_path = tmp_file.name
        
        logger.info(f"Translation completed. Stats: {translation_stats}")
        
        # Return the translated file
        response = FileResponse(
            path=tmp_path,
            filename=f"translated_{file.filename}",
            media_type='application/xml',
            headers={
                "X-Translation-Success": str(translation_stats["success"]),
                "X-Translation-Failed": str(translation_stats["failed"])
            }
        )
        
        # Clean up temp file after response is sent
        response.background = lambda: os.unlink(tmp_path)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting translation service...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")