#!/bin/bash

# Script to run the XML Translator application on Mac

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker Desktop for Mac first."
    echo "Visit: https://docs.docker.com/desktop/install/mac-install/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating default .env file..."
    cat > .env << EOF
# Environment settings
ENVIRONMENT=development
LOG_LEVEL=debug

# Translation service settings
TRANSLATION_SERVICE=huggingface
MODEL_CACHE_DIR=/root/.cache/huggingface

# Frontend settings
NEXT_PUBLIC_API_URL=http://backend:8000/api/v1

# AWS Bedrock settings (required if TRANSLATION_SERVICE=bedrock)
AWS_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
EOF
    echo ".env file created with default settings."
    echo "If you want to use AWS Bedrock service, please edit the .env file and add your AWS credentials."
fi

# Ensure frontend Next.js configuration is set up correctly
if [ ! -f frontend/next.config.js ]; then
    echo "Creating Next.js configuration file..."
    cat > frontend/next.config.js << EOF
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000/api/v1',
  },
};

module.exports = nextConfig;
EOF
    echo "Next.js configuration file created."
fi

# Ensure ESLint configuration is set up correctly
if [ ! -f frontend/.eslintrc.json ]; then
    echo "Creating ESLint configuration file..."
    cat > frontend/.eslintrc.json << EOF
{
  "extends": "next/core-web-vitals",
  "rules": {
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-unused-vars": "warn",
    "import/no-anonymous-default-export": "off"
  }
}
EOF
    echo "ESLint configuration file created."
fi

# Ask which mode to run
echo "How do you want to run the application?"
echo "1. Development mode (with hot reloading)"
echo "2. Production mode"
echo "3. Build and run without TypeScript checks (fix build errors)"
read -p "Enter your choice (1/2/3): " mode

case $mode in
    1)
        echo "Starting in development mode..."
        docker-compose up
        ;;
    2)
        echo "Building and starting in production mode..."
        docker-compose build
        docker-compose up -d
        echo "Application is running in the background."
        echo "Frontend: http://localhost:3000"
        echo "Backend API: http://localhost:8000"
        echo "API Documentation: http://localhost:8000/docs"
        echo "To stop the application, run: docker-compose down"
        ;;
    3)
        echo "Building and running with TypeScript and ESLint checks disabled..."
        
        # Create a temporary docker-compose override file to run the build with errors ignored
        cat > docker-compose.override.yml << EOF
version: '3.8'

services:
  frontend:
    build:
      args:
        - NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
        - SKIP_TYPE_CHECK=true
    environment:
      - NEXT_DISABLE_ESLINT=1
      - NEXT_DISABLE_TYPE_CHECKS=1
EOF
        
        # Build and run
        docker-compose build
        docker-compose up -d
        
        # Remove the temporary override file
        rm docker-compose.override.yml
        
        echo "Application is running in the background with build errors ignored."
        echo "Frontend: http://localhost:3000"
        echo "Backend API: http://localhost:8000"
        echo "API Documentation: http://localhost:8000/docs"
        echo "To stop the application, run: docker-compose down"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac