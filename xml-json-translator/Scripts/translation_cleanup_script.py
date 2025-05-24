#!/usr/bin/env python3
"""
Translation Content Cleanup Script

This script processes XML and JSON translations to correct common issues
encountered in machine-translated content, including:
- Removal of repeated content or artifacts
- Whitespace normalization
- Line ending standardization
- Tag and placeholder preservation
- Character encoding normalization

Usage:
    python3 translation_cleanup.py --input=translated_file.xml --output=cleaned_file.xml [--format=xml|json]

Author: [Your Name]
Date: May 2025
"""

import os
import re
import json
import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from collections import defaultdict

# Regular expressions for common cleanup operations
REPEATED_CONTENT_PATTERN = re.compile(r'(.{5,}?)\1+')  # Detect repeated phrases (5+ chars)
WHITESPACE_PATTERN = re.compile(r'\s+')  # Detect multiple whitespace
EXTRA_PUNCTUATION_PATTERN = re.compile(r'([.,!?;:])\1+')  # Detect repeated punctuation
EXTRA_DOTS_PATTERN = re.compile(r'\.{4,}')  # Replace excessive dots with ellipsis
LINE_BREAK_PATTERN = re.compile(r'\r\n|\r')  # Standardize line breaks
PLACEHOLDER_PATTERN = re.compile(r'(__[a-zA-Z0-9_]+__|%[sdioxXfFeEgGaAcpn]|\{[a-zA-Z0-9_]+\})')
HTML_TAG_PATTERN = re.compile(r'<[^>]*>')

# CDATA pattern for XML cleanup
CDATA_PATTERN = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)

def load_frequency_dict(language_code):
    """
    Load a frequency dictionary for the given language for better cleanup heuristics.
    This can help determine if a translation looks reasonable.
    
    Returns a dummy frequency dict if language-specific resource isn't available.
    """
    # This would ideally load language-specific frequency data
    # For now, we'll use a minimal approach with common words
    common_words = {
        'fi': {'ja', 'ei', 'on', 'se', 'että', 'olla', 'joka', 'hän', 'tämä'},
        'sv': {'och', 'att', 'det', 'i', 'är', 'en', 'som', 'för', 'på'},
        'de': {'und', 'der', 'die', 'das', 'in', 'ist', 'zu', 'den', 'mit'},
        'fr': {'le', 'la', 'les', 'un', 'une', 'et', 'est', 'pour', 'ce'},
        'es': {'el', 'la', 'los', 'las', 'un', 'una', 'y', 'es', 'en'}
    }
    
    return common_words.get(language_code, set())

def detect_language(text, common_words_dict):
    """
    Simple language detection to ensure the text is in the expected language.
    """
    words = set(re.findall(r'\b\w+\b', text.lower()))
    scores = {}
    
    for lang, common_words in common_words_dict.items():
        overlap = words.intersection(common_words)
        scores[lang] = len(overlap) / max(1, len(words))
    
    return max(scores.items(), key=lambda x: x[1])[0] if scores else None

def clean_text(text, language_code):
    """
    Clean a single text segment based on detected issues.
    Preserves placeholders, HTML tags, and other special content.
    """
    if not text or text.isspace():
        return text
        
    # Extract and store placeholders and HTML tags to protect them
    placeholders = {}
    html_tags = {}
    
    # Save placeholders
    def replace_placeholder(match):
        placeholder = match.group(0)
        key = f"__PH{len(placeholders)}__"
        placeholders[key] = placeholder
        return key
        
    # Save HTML tags
    def replace_html(match):
        tag = match.group(0)
        key = f"__HTML{len(html_tags)}__"
        html_tags[key] = tag
        return key
    
    # First save all special content
    protected_text = re.sub(PLACEHOLDER_PATTERN, replace_placeholder, text)
    protected_text = re.sub(HTML_TAG_PATTERN, replace_html, protected_text)
    
    # Clean up repeated content (likely artifacts from translation services)
    cleaned_text = re.sub(REPEATED_CONTENT_PATTERN, r'\1', protected_text)
    
    # Normalize whitespace
    cleaned_text = re.sub(WHITESPACE_PATTERN, ' ', cleaned_text).strip()
    
    # Fix punctuation issues
    cleaned_text = re.sub(EXTRA_PUNCTUATION_PATTERN, r'\1', cleaned_text)
    cleaned_text = re.sub(EXTRA_DOTS_PATTERN, '...', cleaned_text)
    
    # Standardize line endings to LF
    cleaned_text = re.sub(LINE_BREAK_PATTERN, '\n', cleaned_text)
    
    # Restore HTML tags and placeholders
    for key, tag in html_tags.items():
        cleaned_text = cleaned_text.replace(key, tag)
    
    for key, placeholder in placeholders.items():
        cleaned_text = cleaned_text.replace(key, placeholder)
    
    return cleaned_text.strip()

def clean_cdata_content(cdata_text, language_code):
    """
    Specially handle CDATA sections, preserving their HTML content.
    """
    if not cdata_text:
        return cdata_text
        
    # Process the CDATA content while carefully preserving HTML structure
    lines = cdata_text.strip().split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Split by HTML tags
        parts = re.split(r'(<[^>]*>)', line)
        cleaned_parts = []
        
        for part in parts:
            if re.match(r'<[^>]*>', part):  # This is an HTML tag
                cleaned_parts.append(part)
            else:  # This is content between tags
                cleaned_parts.append(clean_text(part, language_code))
                
        cleaned_lines.append(''.join(cleaned_parts))
    
    return '\n'.join(cleaned_lines)

def clean_xml_file(input_file, output_file, language_code):
    """
    Process and clean an XML translation file, preserving structure and attributes.
    """
    try:
        # Parse the XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Load a frequency dictionary for the target language
        common_words = load_frequency_dict(language_code)
        
        # Track potential issues for reporting
        issues = defaultdict(int)
        
        # Process all TEXT elements
        for text_elem in root.findall(".//TEXT"):
            if text_elem.text is None:
                continue
                
            # Check if we have CDATA content
            cdata_match = CDATA_PATTERN.search(text_elem.text)
            if cdata_match:
                # Extract and clean CDATA content while preserving HTML
                original_cdata = cdata_match.group(1)
                cleaned_cdata = clean_cdata_content(original_cdata, language_code)
                
                # If changed, record the issue
                if cleaned_cdata != original_cdata:
                    issues['cdata_cleaned'] += 1
                
                # Replace the CDATA content in the element text
                text_elem.text = text_elem.text.replace(cdata_match.group(1), cleaned_cdata)
            else:
                # Regular text content
                original_text = text_elem.text
                cleaned_text = clean_text(original_text, language_code)
                
                # If changed, record the issue
                if cleaned_text != original_text:
                    issues['text_cleaned'] += 1
                
                text_elem.text = cleaned_text
        
        # Write the cleaned XML with proper formatting
        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
        
        # Clean up excessive newlines in the formatted XML
        pretty_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
            
        print(f"XML cleaning completed. Issues found and corrected:")
        for issue_type, count in issues.items():
            print(f"- {issue_type}: {count}")
            
        return issues
            
    except Exception as e:
        print(f"Error cleaning XML file: {str(e)}")
        raise

def clean_json_file(input_file, output_file, language_code):
    """
    Process and clean a JSON translation file, preserving structure.
    """
    try:
        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Load a frequency dictionary for the target language
        common_words = load_frequency_dict(language_code)
        
        # Track potential issues for reporting
        issues = defaultdict(int)
        
        # Process the JSON data recursively
        def process_json_object(obj):
            if isinstance(obj, dict):
                # Process each key-value pair
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        # Recursively process nested structures
                        process_json_object(value)
                    elif isinstance(value, str) and value.strip():
                        # Clean string values
                        cleaned_value = clean_text(value, language_code)
                        if cleaned_value != value:
                            obj[key] = cleaned_value
                            issues['text_cleaned'] += 1
            
            elif isinstance(obj, list):
                # Process each item in the list
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        # Recursively process nested structures
                        process_json_object(item)
                    elif isinstance(item, str) and item.strip():
                        # Clean string values
                        cleaned_item = clean_text(item, language_code)
                        if cleaned_item != item:
                            obj[i] = cleaned_item
                            issues['text_cleaned'] += 1
        
        # Start processing the root object
        process_json_object(data)
        
        # Write the cleaned JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"JSON cleaning completed. Issues found and corrected:")
        for issue_type, count in issues.items():
            print(f"- {issue_type}: {count}")
            
        return issues
        
    except Exception as e:
        print(f"Error cleaning JSON file: {str(e)}")
        raise

def analyze_translations(input_file, format_type='xml'):
    """
    Analyze a translation file to detect potential issues without modifying it.
    Returns statistics about detected issues.
    """
    issues = defaultdict(int)
    
    try:
        if format_type.lower() == 'xml':
            # Parse the XML file
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            # Detect language based on content
            all_text = ""
            
            # Collect text for language detection and scan for issues
            for text_elem in root.findall(".//TEXT"):
                if text_elem.text:
                    all_text += " " + text_elem.text
                    
                    # Check for potential issues
                    if re.search(REPEATED_CONTENT_PATTERN, text_elem.text):
                        issues['repeated_content'] += 1
                        
                    if re.search(r'\s{2,}', text_elem.text):
                        issues['extra_whitespace'] += 1
                        
                    if re.search(EXTRA_PUNCTUATION_PATTERN, text_elem.text):
                        issues['repeated_punctuation'] += 1
                        
                    if re.search(EXTRA_DOTS_PATTERN, text_elem.text):
                        issues['excessive_dots'] += 1
                        
                    # Check for placeholders
                    placeholders = re.findall(PLACEHOLDER_PATTERN, text_elem.text)
                    if placeholders:
                        # Verify placeholder format integrity
                        original_id = text_elem.get('id', '')
                        if any(ph for ph in placeholders if ph.startswith('__') and not ph.endswith('__')):
                            issues['broken_placeholder'] += 1
                            
            # Estimate language
            language = detect_language(all_text, {
                lang: load_frequency_dict(lang) for lang in ['fi', 'sv', 'de', 'fr', 'es']
            })
            
        elif format_type.lower() == 'json':
            # Load the JSON data
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Collect all string values for language detection and issue scanning
            all_text = ""
            
            def scan_json_object(obj):
                nonlocal all_text
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, (dict, list)):
                            scan_json_object(value)
                        elif isinstance(value, str) and value.strip():
                            all_text += " " + value
                            
                            # Check for potential issues
                            if re.search(REPEATED_CONTENT_PATTERN, value):
                                issues['repeated_content'] += 1
                                
                            if re.search(r'\s{2,}', value):
                                issues['extra_whitespace'] += 1
                                
                            if re.search(EXTRA_PUNCTUATION_PATTERN, value):
                                issues['repeated_punctuation'] += 1
                                
                            if re.search(EXTRA_DOTS_PATTERN, value):
                                issues['excessive_dots'] += 1
                                
                            # Check for placeholders
                            placeholders = re.findall(PLACEHOLDER_PATTERN, value)
                            if placeholders:
                                # Verify placeholder format integrity
                                if any(ph for ph in placeholders if ph.startswith('__') and not ph.endswith('__')):
                                    issues['broken_placeholder'] += 1
                
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, (dict, list)):
                            scan_json_object(item)
                        elif isinstance(item, str) and item.strip():
                            all_text += " " + item
                            
                            # Same issue checks as above
                            if re.search(REPEATED_CONTENT_PATTERN, item):
                                issues['repeated_content'] += 1
                            
                            if re.search(r'\s{2,}', item):
                                issues['extra_whitespace'] += 1
                            
                            if re.search(EXTRA_PUNCTUATION_PATTERN, item):
                                issues['repeated_punctuation'] += 1
                            
                            if re.search(EXTRA_DOTS_PATTERN, item):
                                issues['excessive_dots'] += 1
                                
                            # Check for placeholders
                            placeholders = re.findall(PLACEHOLDER_PATTERN, item)
                            if placeholders:
                                # Verify placeholder format integrity
                                if any(ph for ph in placeholders if ph.startswith('__') and not ph.endswith('__')):
                                    issues['broken_placeholder'] += 1
            
            # Start scanning the JSON
            scan_json_object(data)
            
            # Estimate language
            language = detect_language(all_text, {
                lang: load_frequency_dict(lang) for lang in ['fi', 'sv', 'de', 'fr', 'es']
            })
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
        # Add language detection to issues dict
        issues['detected_language'] = language
        
        return issues
        
    except Exception as e:
        print(f"Error analyzing file: {str(e)}")
        return {'error': str(e)}

def main():
    """
    Main function to handle command line arguments and process files.
    """
    parser = argparse.ArgumentParser(description='Clean and optimize machine-translated content.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--format', default='xml', choices=['xml', 'json'], help='File format (xml or json)')
    parser.add_argument('--lang', default='', help='Target language code (fi, sv, de, fr, es)')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze the file without cleaning')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        return 1
        
    # Determine language code if not provided
    language_code = args.lang
    if not language_code:
        # Try to extract from filename
        filename = os.path.basename(args.input).lower()
        for code in ['fi', 'sv', 'de', 'fr', 'es']:
            if f"_{code}" in filename or f"_{code}." in filename:
                language_code = code
                break
    
    if not language_code:
        print("Warning: Language code not provided and couldn't be determined from filename.")
        print("Analyzing file to detect language...")
        issues = analyze_translations(args.input, args.format)
        language_code = issues.get('detected_language')
        print(f"Detected language: {language_code}")
    
    # Just analyze the file if requested
    if args.analyze_only:
        print(f"Analyzing file: {args.input}")
        issues = analyze_translations(args.input, args.format)
        
        print("\nAnalysis Results:")
        for issue_type, count in issues.items():
            print(f"- {issue_type}: {count}")
        return 0
    
    # Process the file based on format
    try:
        if args.format.lower() == 'xml':
            clean_xml_file(args.input, args.output, language_code)
        elif args.format.lower() == 'json':
            clean_json_file(args.input, args.output, language_code)
        else:
            print(f"Unsupported format: {args.format}")
            return 1
            
        print(f"Cleaned content written to: {args.output}")
        return 0
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
