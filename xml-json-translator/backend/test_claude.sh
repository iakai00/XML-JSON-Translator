#!/bin/bash

# Set environment variables for Claude API testing
export TRANSLATION_SERVICE=claude

# Check if Claude API key is provided
if [ -z "$CLAUDE_API_KEY" ]; then
  echo "Please set the CLAUDE_API_KEY environment variable before running this script."
  echo "Example: CLAUDE_API_KEY=your_api_key_here ./test_claude.sh"
  exit 1
fi

# Restart the backend container with Claude service
echo "Stopping backend container if it's running..."
docker-compose stop backend

echo "Starting backend with Claude API configuration..."
docker-compose up -d backend

# Wait for the backend to be ready
echo "Waiting for backend to be ready..."
attempts=0
max_attempts=30
until $(curl --output /dev/null --silent --head --fail http://localhost:8000/health); do
  if [ ${attempts} -eq ${max_attempts} ]; then
    echo "Max attempts reached. Backend is not responding."
    exit 1
  fi
  
  attempts=$((attempts+1))
  echo "Backend not ready yet, waiting... (Attempt $attempts/$max_attempts)"
  sleep 2
done

echo "Backend is ready! Testing Claude API integration..."

# Test getting supported languages
echo "Testing supported languages endpoint..."
curl -s http://localhost:8000/api/v1/translate/languages?service_type=claude | jq '.'

echo ""
echo "Now you can use the frontend to test Claude translation."
echo "Make sure to select 'Claude AI' as the translation service."
echo ""
echo "To test via CLI, use:"
echo "curl -X POST http://localhost:8000/api/v1/translate/xml -F \"file=@./your_file.xml\" -F \"target_language=fi\" -F \"service_type=claude\" --output translated.xml"