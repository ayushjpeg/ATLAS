# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Create app directory
WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt

# Copy application code
COPY . /app

# Ensure the Atlas.txt file is present (warning only)
RUN if [ ! -f /app/Atlas.txt ]; then echo "Warning: Atlas.txt not found in image. Make sure to include it in build context."; fi

# Download minimal NLTK data used by the app
RUN python -m nltk.downloader punkt -d /usr/local/nltk_data || true
ENV NLTK_DATA=/usr/local/nltk_data

# Expose port and run with gunicorn
EXPOSE ${PORT}

# Use gunicorn to serve the Flask app. The app module is `app:app`.
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "3"]
