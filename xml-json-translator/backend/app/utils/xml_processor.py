
import xml.etree.ElementTree as ET
from typing import Callable, Dict, List, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)

class XMLProcessor:
    def __init__(self):
        self.cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
        # HTML tag pattern to identify tags that should be preserved
        self.html_tag_pattern = re.compile(r'<[^>]*>|<\/[^>]*>')
        # HTML attribute pattern
        self.html_attribute_pattern = re.compile(r'(\s+)([a-zA-Z0-9_-]+)(="[^"]*")')
        
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
    
    def _preserve_html_tags(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Preserve HTML tags by replacing them with markers for translation
        """
        preserved_tags = {}
        
        # Find and replace all HTML tags with markers
        for idx, match in enumerate(self.html_tag_pattern.finditer(text)):
            tag = match.group(0)
            marker = f"HTML_TAG_{idx}"
            preserved_tags[marker] = tag
            text = text.replace(tag, marker)
            
        return text, preserved_tags
    
    def _preserve_html_attributes(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Preserve HTML attributes by replacing them with markers for translation
        """
        preserved_attrs = {}
        
        # Find and replace all HTML attributes with markers
        for idx, match in enumerate(self.html_attribute_pattern.finditer(text)):
            space, attr_name, attr_value = match.groups()
            full_attr = space + attr_name + attr_value
            marker = f"HTML_ATTR_{idx}"
            preserved_attrs[marker] = full_attr
            text = text.replace(full_attr, marker)
            
        return text, preserved_attrs
    
    def _restore_preserved_content(self, text: str, preserved_dict: Dict[str, str]) -> str:
        """Restore preserved content (tags, attributes, placeholders)"""
        for marker, original in preserved_dict.items():
            text = text.replace(marker, original)
        return text
    
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
    
    def process_xml(self, xml_content: str, translate_func: Callable[[str], str]) -> str:
        """
        Process XML and translate text content while preserving structure, IDs, CDATA, and HTML elements
        
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
                
                # Preserve HTML tags
                content_with_tags_preserved, preserved_tags = self._preserve_html_tags(content)
                
                # Preserve HTML attributes
                content_with_attrs_preserved, preserved_attrs = self._preserve_html_attributes(content_with_tags_preserved)
                
                # Preserve placeholders
                content_for_translation, placeholders = self._preserve_placeholders(content_with_attrs_preserved)
                
                # Translate the content
                translated_content = translate_func(content_for_translation)
                
                # Restore placeholders, HTML tags and attributes in reverse order
                restored_content = self._restore_preserved_content(translated_content, placeholders)
                restored_content = self._restore_preserved_content(restored_content, preserved_attrs)
                restored_content = self._restore_preserved_content(restored_content, preserved_tags)
                
                # Wrap in CDATA if original was in CDATA
                if is_cdata:
                    elem.text = self._wrap_in_cdata(restored_content)
                else:
                    elem.text = restored_content
            
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
    
    def process_json(self, json_data: Dict, translate_func: Callable[[str], str], is_claude: bool = False) -> Dict:
        """
        Process JSON data and translate text values while preserving structure
        
        Args:
            json_data: JSON data as dictionary
            translate_func: Function that takes a string and returns translated string
            is_claude: Whether we're using Claude API (affects translation method)
            
        Returns:
            Translated JSON data as dictionary
        """
        # If using Claude, we'll use the specialized translate_json_field method
        if is_claude:
            from app.services.translation_factory import TranslationServiceFactory
            
            # Get current target language and service type from the context
            # This depends on how your translate_func is set up
            # You might need to adapt this based on your implementation
            
            # Create a wrapper function to redirect to JSON-specific translation
            def translate_json_field_wrapper(text):
                if not text or text.isspace():
                    return text
                    
                # Extract target language and service type from context
                # This is a simplified example - you'll need to adapt it
                target_lang = getattr(translate_func, 'target_lang', None)
                service_type = getattr(translate_func, 'service_type', 'claude')
                
                if target_lang:
                    return TranslationServiceFactory.translate_json_field(text, target_lang, 'claude')
                else:
                    # Fallback to regular translation if we couldn't get context
                    return translate_func(text)
                    
            # Use our wrapper for translation
            return self._process_json_internal(json_data, translate_json_field_wrapper)
        else:
            # For other services, use the regular translation
            return self._process_json_internal(json_data, translate_func)
    
    # This is the internal implementation that does the actual recursion
    def _process_json_internal(self, json_data: Dict, translate_func: Callable[[str], str]) -> Dict:
        """Internal implementation of JSON processing"""
        translated_data = {}
        
        for key, value in json_data.items():
            if isinstance(value, dict):
                # Recursively process nested dictionaries
                translated_data[key] = self._process_json_internal(value, translate_func)
            elif isinstance(value, list):
                # Process lists
                if all(isinstance(item, str) for item in value):
                    # If all items are strings, translate each one
                    translated_data[key] = [translate_func(item) for item in value]
                else:
                    # Process lists of mixed/complex types
                    translated_data[key] = [
                        self._process_json_internal(item, translate_func) if isinstance(item, dict) 
                        else translate_func(item) if isinstance(item, str) and self._should_translate_key(key)
                        else item
                        for item in value
                    ]
            elif isinstance(value, str) and self._should_translate_key(key):
                # Translate text fields
                content_for_translation, placeholders = self._preserve_placeholders(value)
                
                # Preserve HTML tags if present
                content_with_tags_preserved, preserved_tags = self._preserve_html_tags(content_for_translation)
                content_with_attrs_preserved, preserved_attrs = self._preserve_html_attributes(content_with_tags_preserved)
                
                # Translate the processed content
                translated_content = translate_func(content_with_attrs_preserved)
                
                # Restore placeholders, HTML tags and attributes in reverse order
                restored_content = self._restore_preserved_content(translated_content, preserved_attrs)
                restored_content = self._restore_preserved_content(restored_content, preserved_tags)
                restored_content = self._restore_preserved_content(restored_content, placeholders)
                
                translated_data[key] = restored_content
            else:
                # Keep other fields unchanged
                translated_data[key] = value
                    
        return translated_data

    def _should_translate_key(self, key: str) -> bool:
        """Determine if a JSON key likely contains translatable content"""
        # Common field names that typically contain translatable text
        translatable_keys = [
            'text', 'title', 'description', 'name', 'label', 'message', 
            'content', 'body', 'summary', 'caption', 'heading', 'subheading',
            'error', 'warning', 'info', 'note', 'tooltip', 'placeholder',
            'button', 'link', 'menu', 'option', 'help', 'hint', 'confirmation'
        ]
        
        # Check if the lowercase key is in our list of translatable keys
        key_lower = key.lower()
        
        # Direct match with common text field names
        if key_lower in translatable_keys:
            return True
        
        # Check for keys ending with common text field suffixes
        for translatable_key in translatable_keys:
            if key_lower.endswith(f"_{translatable_key}") or key_lower.endswith(f"{translatable_key}s"):
                return True
                
        # Check for keys containing 'text', 'message', 'title', etc.
        for text_indicator in ['text', 'message', 'title', 'description', 'label']:
            if text_indicator in key_lower:
                return True
        
        # Additional checks for special formats like i18n identifiers
        if 'i18n' in key_lower or 'label' in key_lower or 'msg' in key_lower:
            return True
            
        return False
    
    def _translate_text_with_preservation(self, text: str, translate_func: Callable[[str], str]) -> str:
        """Helper method to translate text while preserving HTML and placeholders"""
        if not text:
            return text
            
        # Preserve HTML tags
        text_with_tags_preserved, preserved_tags = self._preserve_html_tags(text)
        
        # Preserve HTML attributes
        text_with_attrs_preserved, preserved_attrs = self._preserve_html_attributes(text_with_tags_preserved)
        
        # Preserve placeholders
        text_for_translation, placeholders = self._preserve_placeholders(text_with_attrs_preserved)
        
        # Translate the text
        translated_text = translate_func(text_for_translation)
        
        # Restore placeholders, HTML tags and attributes in reverse order
        restored_text = self._restore_preserved_content(translated_text, placeholders)
        restored_text = self._restore_preserved_content(restored_text, preserved_attrs)
        restored_text = self._restore_preserved_content(restored_text, preserved_tags)
        
        return restored_text