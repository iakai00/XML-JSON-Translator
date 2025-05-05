# XML & JSON Translator

A web application that translates XML and JSON files from English to multiple languages using machine learning models.

## Features

- Upload and translate XML and JSON files
- Preserve structure, IDs, and CDATA sections in XML files
- Support for placeholders in the form of `__name__`
- Choose from multiple target languages
- Two translation engines:
  - **Hugging Face** (free): Uses Helsinki-NLP models
  - **AWS Bedrock** (premium): Uses Claude AI for better translations

## Project Structure

```
xml-translator/
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── api/        # API endpoints
│   │   ├── core/       # Core configurations
│   │   ├── models/     # Pydantic models
│   │   ├── services/   # Translation services
│   │   └── utils/      # Utility functions
│   ├── tests/          # Backend tests
│   ├── Dockerfile      # Backend Docker configuration
│   └── ...             # Other backend files
├── frontend/           # Next.js frontend
│   ├── src/
│   │   ├── app/        # Next.js app directory
│   │   ├── components/ # React components
│   │   ├── services/   # API service layer
│   │   ├── styles/     # CSS styles
│   │   └── types/      # TypeScript types
│   ├── Dockerfile      # Frontend Docker configuration
│   └── ...             # Other frontend files
├── docker-compose.yml  # Docker Compose configuration
├── .env                # Environment variables
└── run.sh              # Script to run the application
```

## Requirements

- Docker and Docker Compose
- For AWS Bedrock service: AWS credentials

## Getting Started

### Quick Start for Mac

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/xml-translator.git
   cd xml-translator
   ```

2. Run the application:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

### Manual Setup

1. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file to set required variables
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Stop the application:
   ```bash
   docker-compose down
   ```

## Development

### Backend Development

The backend is built with FastAPI and provides endpoints for:
- Getting supported languages
- Translating XML files
- Translating JSON files

To run the backend in development mode:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development

The frontend is built with Next.js and Tailwind CSS:

```bash
cd frontend
npm install
npm run dev
```

## Using AWS Bedrock

To use the AWS Bedrock service for higher quality translations:

1. Set up AWS credentials in the `.env` file:
   ```
   AWS_REGION=us-east-1  # Your AWS region
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   TRANSLATION_SERVICE=bedrock
   ```

2. Restart the application

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## License

MIT