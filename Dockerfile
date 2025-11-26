# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv pip install --system \
  python-telegram-bot \
  feedparser \
  requests \
  beautifulsoup4 \
  python-dotenv \
  huggingface-hub

# Copy application code
COPY . .

# Create directories for logs and data
RUN mkdir -p /app/logs /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the bot
CMD ["python", "telegram_bot.py"]
