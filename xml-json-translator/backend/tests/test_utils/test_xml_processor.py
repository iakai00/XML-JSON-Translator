import pytest
import xml.etree.ElementTree as ET
import json
from app.utils.xml_processor import XMLProcessor

# Sample XML content for testing
SAMPLE_XML = """<?xml version="1.0" encoding="utf-8"?>
<LOCALIZATION version="1.0" id="en" name="English">
  <TEXT id="welcome.title">Welcome to our application</TEXT>
  <TEXT id="welcome.message"><![CDATA[<p>Hello and welcome to our <b>awesome</b> application!</p>]]></TEXT>
  <TEXT id="button.save">Save</TEXT>
  <TEXT id="placeholder.email">Please enter your __email__</TEXT>
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
            {"id": "welcome.message", "text": "Hello and welcome to our awesome application!"},
            {"id": "button.save", "text": "Save"},
            {"id": "placeholder.email", "text": "Please enter your __email__"}
        ]
    }
}


def test_xml_processor_process_xml():
    """Test the XML processor's process_xml method"""
    processor = XMLProcessor()
    
    # Mock translation function
    def mock_translate(text):
        return f"[TRANSLATED] {text}"
    
    # Process the XML
    translated_xml = processor.process_xml(SAMPLE_XML, mock_translate)
    
    # Parse the translated XML
    root = ET.fromstring(translated_xml)
    
    # Check that all TEXT elements have been translated
    for elem in root.findall(".//TEXT"):
        text_id = elem.get('id')
        assert text_id is not None
        
        if elem.text and not elem.text.startswith("<![CDATA["):
            assert elem.text.startswith("[TRANSLATED]")
        else:
            # For CDATA sections, check inside
            assert "[TRANSLATED]" in elem.text
            
    # Check that placeholders are preserved
    email_elem = root.find(".//TEXT[@id='placeholder.email']")
    assert "__email__" in email_elem.text


def test_xml_processor_process_json():
    """Test the XML processor's process_json method"""
    processor = XMLProcessor()
    
    # Mock translation function
    def mock_translate(text):
        return f"[TRANSLATED] {text}"
    
    # Process the JSON
    translated_json = processor.process_json(SAMPLE_JSON, mock_translate)
    
    # Check structure is preserved
    assert "localization" in translated_json
    assert translated_json["localization"]["version"] == "1.0"
    assert translated_json["localization"]["id"] == "en"
    
    # Check texts are translated
    for text_item in translated_json["localization"]["texts"]:
        assert text_item["id"] is not None
        assert text_item["text"].startswith("[TRANSLATED]")
    
    # Check that placeholders are preserved
    email_text = [t for t in translated_json["localization"]["texts"] if t["id"] == "placeholder.email"][0]["text"]
    assert "__email__" in email_text