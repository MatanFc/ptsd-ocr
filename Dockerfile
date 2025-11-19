# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # FFmpeg for image/video conversion
    ffmpeg \
    # Tesseract OCR engine
    tesseract-ocr \
    tesseract-ocr-heb \
    # libmagic for file type detection
    libmagic1 \
    # Other required system libraries
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY ocr_service.py .

# Create a directory for user files
RUN mkdir -p /app/files

# Verify installations
RUN python -c "import pytesseract; print('Tesseract version:', pytesseract.get_tesseract_version())" \
    && tesseract --list-langs | grep heb \
    && ffmpeg -version

# Set default command
CMD ["python", "main.py"]

# Add labels for metadata
LABEL maintainer="PTSD OCR Service" \
      description="OCR service with Hebrew text support and FFmpeg integration" \
      version="1.0"
