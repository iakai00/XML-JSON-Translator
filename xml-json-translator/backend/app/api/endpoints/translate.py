import os
import tempfile
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import json

from app.core.config import get_settings, Settings
from app.models.translation import Language, SupportedLanguagesResponse, TranslationResponse
from app.services.huggingface_service import HuggingFaceTranslationService
from app.utils.xml_processor import XMLProcessor

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
translation_service = HuggingFaceTranslationService()
xml_processor = XMLProcessor()

@router.get("/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages(
    settings: Settings = Depends(get_settings)
):
    """
    Get a list of supported target languages for translation
    """
    try:
        languages = translation_service.get_supported_languages()
        return {"languages": languages}
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get supported languages: {str(e)}")


@router.post("/xml", response_model=TranslationResponse)
async def translate_xml_file(
    file: UploadFile = File(...),
    target_language: str = Form(...),
    settings: Settings = Depends(get_settings)
):
    """
    Translate an XML file from English to the specified target language
    """
    # Check file extension
    if not file.filename.lower().endswith('.xml'):
        raise HTTPException(status_code=400, detail="Only XML files are supported")
    
    try:
        # Read file content
        content = await file.read()
        xml_content = content.decode('utf-8')
        
        # Create a translation function that will be called by the XML processor
        def translate_text(text):
            return translation_service.translate(text, target_language)
        
        # Process the XML and translate the text
        translated_xml = xml_processor.process_xml(xml_content, translate_text)
        
        # Create a temporary file to store the translated XML
        target_lang_suffix = target_language.lower()
        fd, temp_path = tempfile.mkstemp(suffix=f'_{target_lang_suffix}.xml')
        with os.fdopen(fd, 'w', encoding='utf-8') as tmp:
            tmp.write(translated_xml)
        
        # Generate output filename
        original_name = os.path.splitext(file.filename)[0]
        output_filename = f"{original_name}_{target_lang_suffix}.xml"
        
        # Return the translated XML file
        return FileResponse(
            path=temp_path,
            media_type='application/xml',
            filename=output_filename,
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
    
    except Exception as e:
        logger.error(f"Error translating XML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")