# XML/JSON Translator with FastAPI and Next.js

A modern web application for translating XML and JSON files from English to multiple languages while preserving structure, tags, and attributes.

## Key Features

- **Structure Preservation**: Maintains XML/JSON hierarchy and special elements
- **Multiple Translation Engines**:
  - **Hugging Face** (Free): Helsinki NLP models for offline translation
  - **Claude AI** (Premium): High-quality translation via Anthropic's API
- **Format Support**:
  - XML with CDATA sections, placeholders, and embedded HTML
  - JSON with automatic field detection
- **User-Friendly Interface**:
  - Drag-and-drop file upload
  - Multiple file batch processing
  - Clear progress indicators and download management

## Technology Stack

- **Backend**: Python FastAPI
- **Frontend**: Next.js with React
- **Translation**: Helsinki NLP and Claude API
- **Deployment**: Docker containerization

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Claude API key (for premium translation)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/xml-translator.git
   cd xml-translator
   ```

2. Configure environment variables:
   ```bash
   # Create .env file in backend directory
   echo "CLAUDE_API_KEY=your_api_key_here" > backend/.env
   ```

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. Access the web interface at http://localhost:3000

## Usage Guide

1. **Upload Files**: Drag & drop or select XML or JSON files
2. **Choose Language**: Select your desired target language
3. **Select Service**: Choose between Hugging Face (free) or Claude (premium)
4. **Translate**: Click the translate button and monitor progress
5. **Download**: Download translated files when ready

## Supported Languages

- **Hugging Face**: Finnish, Swedish, German, French, Spanish and more
- **Claude API**: 20+ languages including Asian languages (Japanese, Chinese, Korean)

## Translation Quality

- **Hugging Face**: Good quality for basic content, runs locally
- **Claude API**: Higher quality with better context understanding, requires API key

## Development

### Local Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Configuration Options

Edit `config.py` to modify:
- Available language models
- CORS settings
- Logging configuration
- API endpoints

## Docker Deployment

The application is containerized for easy deployment:

```bash
# Start all services
docker-compose up -d

# Backend only
docker-compose up -d backend

# View logs
docker-compose logs -f
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Helsinki NLP](https://huggingface.co/Helsinki-NLP) for their open-source translation models
- [Anthropic](https://anthropic.com) for the Claude API
- The FastAPI and Next.js communities for excellent documentation