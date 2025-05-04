import xml.etree.ElementTree as ET
from typing import Callable, Dict, List, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)

class XMLProcessor:
    def __init__(self):
        self.cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
    
    def _extract_cdata_content(self, text: str) -> Tuple[bool, str]:
        """Extract content from CDATA section if present"""
        if not text:
            return False, ""
        
        match = self.cdata_pattern.search(text)
        if match:
            return True, match.group(1)
        return False, text
    
    def _wrap_in_cdata(self, text: str) -> str:
        """Wrap text in CDATA section"""
        return f"<![CDATA[{text}]]>"
    
    def _preserve_placeholders(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Preserve placeholders like __name__, __phonePrefix__, etc.
        and replace them with unique identifiers for translation
        """
        placeholders = {}
        placeholder_pattern = re.compile(r'__([a-zA-Z0-9]+)__')
        
        # Find all placeholders and replace them with unique markers
        for idx, match in enumerate(placeholder_pattern.finditer(text)):
            placeholder = match.group(0)
            marker = f"PLACEHOLDER_{idx}"
            placeholders[marker] = placeholder
            text = text.replace(placeholder, marker)
            
        return text, placeholders
    
    def _restore_placeholders(self, text: str, placeholders: Dict[str, str]) -> str:
        """Restore placeholders after translation"""
        for marker, placeholder in placeholders.items():
            text = text.replace(marker, placeholder)
        return text
    
    def process_xml(self, xml_content: str, translate_func: Callable[[str], str]) -> str:
        """
        Process XML and translate text content while preserving structure, IDs, and CDATA
        
        Args:
            xml_content: XML content as string
            translate_func: Function that takes a string and returns translated string
            
        Returns:
            Translated XML content as string
        """
        try:
            # Parse the XML
            root = ET.fromstring(xml_content)
            
            # Extract namespace if present
            namespace = ''
            if '}' in root.tag:
                namespace = root.tag.split('}')[0] + '}'
            
            # Process all TEXT elements
            for elem in root.findall(f".//{namespace}TEXT"):
                text_id = elem.get('id')
                logger.debug(f"Processing element with ID: {text_id}")
                
                # Skip translation if no text content
                if elem.text is None:
                    continue
                
                # Extract text content, handling CDATA if present
                is_cdata, content = self._extract_cdata_content(elem.text)
                
                # Preserve placeholders
                content_for_translation, placeholders = self._preserve_placeholders(content)
                
                # Translate the content
                translated_content = translate_func(content_for_translation)
                
                # Restore placeholders
                translated_content = self._restore_placeholders(translated_content, placeholders)
                
                # Wrap in CDATA if original was in CDATA
                if is_cdata:
                    elem.text = self._wrap_in_cdata(translated_content)
                else:
                    elem.text = translated_content
            
            # Convert back to string with proper XML declaration
            xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n'
            xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
            
            # Add XML declaration if it's not present
            if not xml_string.startswith('<?xml'):
                xml_string = xml_declaration + xml_string
                
            return xml_string
        
        except Exception as e:
            logger.error(f"Error processing XML: {str(e)}")
            raise
            
    def process_json(self, json_data: Dict, translate_func: Callable[[str], str]) -> Dict:
        """
        Process JSON data and translate text values while preserving structure and IDs
        
        Args:
            json_data: JSON data as dictionary
            translate_func: Function that takes a string and returns translated string
            
        Returns:
            Translated JSON data as dictionary
        """
        translated_data = {}
        
        for key, value in json_data.items():
            if isinstance(value, dict):
                # Recursively process nested dictionaries
                translated_data[key] = self.process_json(value, translate_func)
            elif isinstance(value, list):
                # Process lists
                translated_data[key] = [
                    self.process_json(item, translate_func) if isinstance(item, dict) 
                    else translate_func(item) if isinstance(item, str) 
                    else item
                    for item in value
                ]
            elif isinstance(value, str) and key.lower() in ['text', 'content', 'value', 'description']:
                # Translate text fields
                content_for_translation, placeholders = self._preserve_placeholders(value)
                translated_value = translate_func(content_for_translation)
                translated_data[key] = self._restore_placeholders(translated_value, placeholders)
            else:
                # Keep other fields unchanged
                translated_data[key] = value
                
        return translated_data