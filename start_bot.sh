#!/bin/bash

# Telegram News Bot Startup Script

set -e

echo "======================================"
echo "   Telegram News Bot Deployment"
echo "======================================"

# Check if .env exists
if [ ! -f .env ]; then
  echo "❌ Error: .env file not found!"
  echo "Please create a .env file with your tokens:"
  echo ""
  echo "TELEGRAM_BOT_TOKEN=your_token_here"
  echo "HF_TOKEN=your_hf_token_here"
  exit 1
fi

# Check if TELEGRAM_BOT_TOKEN is set
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env; then
  echo "❌ Error: TELEGRAM_BOT_TOKEN not found in .env file!"
  exit 1
fi

echo "✅ Environment file found"

# Check if Docker is installed
if ! command -v docker &>/dev/null; then
  echo "❌ Error: Docker is not installed!"
  echo "Please install Docker: https://docs.docker.com/get-docker/"
  exit 1
fi

echo "✅ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &>/dev/null; then
  echo "⚠️  Warning: docker-compose not found, trying 'docker compose'"
  COMPOSE_CMD="docker compose"
else
  COMPOSE_CMD="docker-compose"
fi

echo "✅ Docker Compose is ready"

# Stop existing containers
echo ""
echo "🛑 Stopping existing containers..."
$COMPOSE_CMD down 2>/dev/null || true

# Build the image
echo ""
echo "🔨 Building Docker image..."
$COMPOSE_CMD build

# Start the bot
echo ""
echo "🚀 Starting the bot..."
$COMPOSE_CMD up -d

# Show status
echo ""
echo "📊 Container status:"
$COMPOSE_CMD ps

# Show logs
echo ""
echo "📝 Recent logs (Ctrl+C to exit):"
echo "======================================"
$COMPOSE_CMD logs -f --tail=50

# This will run until user presses Ctrl+C
