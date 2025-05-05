# Use a pre-built PyTorch image to avoid compiling from source
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies with optimizations
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for model cache to persist between container restarts
# This prevents re-downloading models on every container restart
VOLUME /root/.cache/huggingface

# Copy only the application code
COPY ./app /app/app
COPY main.py .

# Set environment variables
ENV PYTHONPATH=/app
ENV MODEL_CACHE_DIR=/root/.cache/huggingface

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]