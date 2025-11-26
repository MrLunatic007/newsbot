#!/bin/bash

# Setup script for subscription system

echo "======================================"
echo "  Setting up Subscription System"
echo "======================================"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p src/subscription
mkdir -p data
mkdir -p logs

echo "✅ Directories created"

# Check if subscription_manager.py exists
if [ ! -f "src/subscription/subscription_manager.py" ]; then
  echo "❌ subscription_manager.py not found in src/subscription/"
  echo "Please save the subscription_manager.py file first"
  exit 1
fi

echo "✅ subscription_manager.py found"

# Create __init__.py files for Python packages
touch src/__init__.py
touch src/subscription/__init__.py
touch src/getter/__init__.py
touch src/parser/__init__.py
touch src/source/__init__.py
touch src/summarizer/__init__.py
touch src/generation/__init__.py

echo "✅ Package files created"

# Check if telegram_bot.py exists and is updated
if [ ! -f "telegram_bot.py" ]; then
  echo "❌ telegram_bot.py not found"
  echo "Please save the updated telegram_bot.py file"
  exit 1
fi

echo "✅ telegram_bot.py found"

# Make admin tool executable
if [ -f "admin_tool.py" ]; then
  chmod +x admin_tool.py
  echo "✅ admin_tool.py made executable"
else
  echo "⚠️  admin_tool.py not found (optional)"
fi

# Test import
echo ""
echo "🧪 Testing imports..."
python3 -c "from src.subscription.subscription_manager import SubscriptionManager; print('✅ Import successful')" 2>/dev/null

if [ $? -ne 0 ]; then
  echo "❌ Import test failed"
  echo "Make sure all files are in the correct locations"
  exit 1
fi

echo ""
echo "======================================"
echo "  ✅ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Update your .env file with TELEGRAM_BOT_TOKEN"
echo "2. Run: ./start_bot.sh"
echo "3. Test with /start command in Telegram"
echo "4. Use admin_tool.py to manage subscriptions"
echo ""
echo "Admin tool usage:"
echo "  python admin_tool.py"
echo ""
echo "Documentation:"
echo "  - SUBSCRIPTION_GUIDE.md - Full subscription guide"
echo "  - DEPLOYMENT.md - Deployment instructions"
echo ""
