#!/bin/bash

# Create model cache directory if it doesn't exist
mkdir -p ./model_cache

# Check if Docker volume exists
if ! docker volume inspect huggingface_cache >/dev/null 2>&1; then
    echo "Creating Docker volume for model cache..."
    docker volume create huggingface_cache
fi
# Check if Claude API key is set
if [ -z "$CLAUDE_API_KEY" ] && [ -n "$(grep -E '^CLAUDE_API_KEY=' .env)" ]; then
    # Load from .env file if it exists and has the key
    export $(grep -E '^CLAUDE_API_KEY=' .env | xargs)
    echo "Loaded Claude API key from .env file"
fi

# Check if we want to build with pre-downloaded models
if [ "$1" == "--with-models" ]; then
    # Run model download script for selected languages
    echo "Pre-downloading models to speed up container startup..."
    python download_models.py --cache-dir ./model_cache --languages fi sv de
    
    # Copy models to Docker volume
    echo "Copying models to Docker volume..."
    # Create a temporary container to copy files
    docker run -d --name temp-container -v huggingface_cache:/cache busybox sleep 30
    docker cp ./model_cache/. temp-container:/cache/
    docker stop temp-container
    docker rm temp-container
fi

# Build and start only the backend for faster iteration
echo "Starting backend service..."
docker-compose up -d backend

# Wait for backend to be healthy
echo "Waiting for backend to be ready..."
while ! curl -s http://localhost:8000/health | grep -q "healthy"; do
    echo "Backend not ready yet, waiting..."
    sleep 2
done

echo "Backend is ready! Starting frontend..."
cd ../frontend && npm run dev