# download_models.py
import os
import argparse
from transformers import MarianMTModel, MarianTokenizer

# Default model mapping
DEFAULT_MODELS = {
    "fi": "Helsinki-NLP/opus-mt-en-fi",  # English to Finnish
    "sv": "Helsinki-NLP/opus-mt-en-sv",  # English to Swedish
    "de": "Helsinki-NLP/opus-mt-en-de",  # English to German
    "fr": "Helsinki-NLP/opus-mt-en-fr",  # English to French
    "es": "Helsinki-NLP/opus-mt-en-es",  # English to Spanish
}

def download_models(cache_dir, languages=None):
    """Download specified models to cache directory"""
    os.makedirs(cache_dir, exist_ok=True)
    
    models_to_download = DEFAULT_MODELS
    if languages:
        models_to_download = {lang: DEFAULT_MODELS[lang] for lang in languages if lang in DEFAULT_MODELS}
    
    for lang, model_name in models_to_download.items():
        print(f"Downloading model for {lang}: {model_name}")
        
        # Download tokenizer
        tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        
        # Download model
        model = MarianMTModel.from_pretrained(model_name, cache_dir=cache_dir)
        
        print(f"Successfully downloaded model for {lang}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download translation models')
    parser.add_argument('--cache-dir', default='./model_cache', help='Cache directory for models')
    parser.add_argument('--languages', nargs='*', help='Language codes to download (default: all)')
    
    args = parser.parse_args()
    
    download_models(args.cache_dir, args.languages)