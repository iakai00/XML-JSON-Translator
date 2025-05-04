#!/bin/bash
# docker-run.sh

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "Docker does not seem to be running. Please start Docker Desktop first."
        exit 1
    fi
}

# Check if input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: ./docker-run.sh <path_to_xml_file>"
    exit 1
fi

# Check if Docker is running
check_docker

# Get absolute path of input file
INPUT_FILE=$(realpath "$1")
INPUT_DIR=$(dirname "$INPUT_FILE")
INPUT_FILENAME=$(basename "$INPUT_FILE")

echo "Creating output directory..."
mkdir -p output

echo "Building Docker image (this might take a few minutes)..."
docker build -t translation-service . || {
    echo "Docker build failed"
    exit 1
}

echo "Running translation service in Docker..."
docker run --rm \
    --name translation-service \
    --memory=4g \
    --cpus=2 \
    -v "$INPUT_DIR:/app/input:ro" \
    -v "$(pwd)/output:/app/output" \
    -p 8000:8000 \
    translation-service

echo "Checking output directory for translated file..."
if [ -f "output/translated_$INPUT_FILENAME" ]; then
    echo "Translation completed successfully!"
    echo "Output file is in: output/translated_$INPUT_FILENAME"
else
    echo "Translation failed or output file not found."
fi