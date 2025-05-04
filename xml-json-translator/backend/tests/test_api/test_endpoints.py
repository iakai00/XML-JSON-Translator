import pytest
from fastapi.testclient import TestClient
import os
import io
from unittest.mock import patch, MagicMock

from main import app

client = TestClient(app)

# Sample XML content for testing
SAMPLE_XML = """<?xml version="1.0" encoding="utf-8"?>
<LOCALIZATION version="1.0" id="en" name="English">
  <TEXT id="welcome.title">Welcome to our application</TEXT>
  <TEXT id="button.save">Save</TEXT>
</LOCALIZATION>
"""

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs_url" in response.json()

def test_get_supported_languages():
    """Test getting supported languages"""
    response = client.get("/api/v1/translate/languages")
    assert response.status_code == 200
    assert "languages" in response.json()
    # Check if there are languages returned
    assert len(response.json()["languages"]) > 0

@pytest.mark.skipif(os.environ.get("SKIP_MODEL_TESTS") == "1", reason="Skip tests that require model downloads")
def test_translate_xml_endpoint():
    """Test the XML translation endpoint with a simple file"""
    # Create a file-like object from the sample XML
    xml_file = io.BytesIO(SAMPLE_XML.encode())
    
    # Create form data with the file
    files = {"file": ("test.xml", xml_file, "application/xml")}
    data = {"target_language": "fi"}  # Using Finnish as test target
    
    # Mock the translation service to avoid actual API calls
    with patch("app.services.huggingface_service.HuggingFaceTranslationService.translate") as mock_translate:
        # Mock translation function
        mock_translate.side_effect = lambda text, _: f"[MOCK_TRANSLATED] {text}"
        
        # Make the request
        response = client.post("/api/v1/translate/xml", files=files, data=data)
    
    # Check basic response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "content-disposition" in response.headers