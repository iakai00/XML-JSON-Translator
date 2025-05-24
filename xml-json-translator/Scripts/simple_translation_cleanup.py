#!/usr/bin/env python3
"""
Simple Translation Cleanup Script

This script processes XML or JSON translation files to clean common issues
in machine-translated content, improving output quality and functionality.

Usage:
    python cleanup_translation.py input_file output_file [--format=xml|json]
"""

import re
import sys
import json
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

def clean_text(text):
    """Clean a text segment by removing common translation artifacts."""
    if not text or text.isspace():
        return text
    
    # Preserve placeholders and HTML tags with simple regex
    placeholders = {}
    tags = {}
    
    # Find and temporarily replace placeholders (__name__, {var}, %s, etc.)
    placeholder_pattern = re.compile(r'(__[a-zA-Z0-9_]+__|%[sdioxXfFeEgGaAcpn]|\{[a-zA-Z0-9_]+\})')
    i = 0
    for match in placeholder_pattern.finditer(text):
        placeholder = match.group(0)
        key = f"__PH{i}__"
        placeholders[key] = placeholder
        i += 1
    
    # Find and temporarily replace HTML tags
    tag_pattern = re.compile(r'<[^>]*>')
    i = 0
    for match in tag_pattern.finditer(text):
        tag = match.group(0)
        key = f"__TAG{i}__"
        tags[key] = tag
        i += 1
    
    # Replace placeholders and tags with temporary keys
    for key, value in placeholders.items():
        text = text.replace(value, key)
    
    for key, value in tags.items():
        text = text.replace(value, key)
    
    # Clean up repetitions (more than 2 of the same content in a row)
    text = re.sub(r'(.{5,}?)\1{2,}', r'\1', text)
    
    # Fix excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Fix repeated punctuation
    text = re.sub(r'([.,!?;:])\1+', r'\1', text)
    
    # Fix excessive dots
    text = re.sub(r'\.{4,}', '...', text)
    
    # Restore tags and placeholders
    for key, value in tags.items():
        text = text.replace(key, value)
    
    for key, value in placeholders.items():
        text = text.replace(key, value)
    
    return text

def clean_xml_file(input_file, output_file):
    """Clean an XML translation file."""
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Process all text elements
        for elem in root.iter():
            if elem.text and elem.text.strip():
                elem.text = clean_text(elem.text)
            
            # Also clean tail text if present
            if elem.tail and elem.tail.strip():
                elem.tail = clean_text(elem.tail)
        
        # Convert to string and pretty-print
        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove empty lines from pretty print
        pretty_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
            
        print(f"XML file cleaned and saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing XML file: {e}")
        return False
    
    return True

def clean_json_file(input_file, output_file):
    """Clean a JSON translation file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process JSON recursively
        def clean_json_object(obj):
            if isinstance(obj, dict):
                # Clean dictionary values
                for key, value in obj.items():
                    if isinstance(value, str):
                        obj[key] = clean_text(value)
                    elif isinstance(value, (dict, list)):
                        clean_json_object(value)
            
            elif isinstance(obj, list):
                # Clean list items
                for i, item in enumerate(obj):
                    if isinstance(item, str):
                        obj[i] = clean_text(item)
                    elif isinstance(item, (dict, list)):
                        clean_json_object(item)
        
        # Start the cleaning process
        clean_json_object(data)
        
        # Write the cleaned JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"JSON file cleaned and saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing JSON file: {e}")
        return False
    
    return True

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Clean machine translation artifacts from XML or JSON files.')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--format', choices=['xml', 'json'], default='xml', help='File format (xml or json)')
    
    args = parser.parse_args()
    
    if args.format.lower() == 'xml':
        return clean_xml_file(args.input, args.output)
    elif args.format.lower() == 'json':
        return clean_json_file(args.input, args.output)
    else:
        print(f"Unsupported format: {args.format}")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
