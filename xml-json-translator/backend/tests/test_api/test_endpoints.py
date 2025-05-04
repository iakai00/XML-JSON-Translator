import pytest
from fastapi.testclient import TestClient
import os
import io
import json
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

# Sample JSON content for testing
SAMPLE_JSON = {
    "localization": {
        "version": "1.0",
        "id": "en",
        "name": "English",
        "texts": [
            {"id": "welcome.title", "text": "Welcome to our application"},
            {"id": "button.save", "text": "Save"}
        ]
    }
}

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
    with patch("app.services.translation_factory.TranslationServiceFactory.translate") as mock_translate:
        # Mock translation function
        mock_translate.side_effect = lambda text, target_lang, service_type: f"[MOCK_TRANSLATED] {text}"
        
        # Make the request
        response = client.post("/api/v1/translate/xml", files=files, data=data)
    
    # Check basic response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "content-disposition" in response.headers

@pytest.mark.skipif(os.environ.get("SKIP_MODEL_TESTS") == "1", reason="Skip tests that require model downloads")
def test_translate_json_endpoint():
    """Test the JSON translation endpoint with a simple file"""
    # Create a file-like object from the sample JSON
    json_file = io.BytesIO(json.dumps(SAMPLE_JSON).encode())
    
    # Create form data with the file
    files = {"file": ("test.json", json_file, "application/json")}
    data = {"target_language": "fi"}  # Using Finnish as test target
    
    # Mock the translation service to avoid actual API calls
    with patch("app.services.translation_factory.TranslationServiceFactory.translate") as mock_translate:
        # Mock translation function
        mock_translate.side_effect = lambda text, target_lang, service_type: f"[MOCK_TRANSLATED] {text}"
        
        # Make the request
        response = client.post("/api/v1/translate/json", files=files, data=data)
    
    # Check basic response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "content-disposition" in response.headers
    
    # Parse the response content
    response_json = json.loads(response.content)
    
    # Check structure is preserved
    assert "localization" in response_json
    assert response_json["localization"]["version"] == "1.0"
    assert response_json["localization"]["id"] == "en"
    
    # Check texts are translated
    for text_item in response_json["localization"]["texts"]:
        assert text_item["id"] is not None
        assert "[MOCK_TRANSLATED]" in text_item["text"]