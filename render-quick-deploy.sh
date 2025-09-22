#!/bin/bash

# Render Quick Deploy Script for Crypto Bot
# This script helps you prepare for Render deployment

echo "🚀 Render Crypto Bot Deployment"
echo "=============================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Crypto bot for Render deployment"
fi

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "📝 Creating render.yaml..."
    cat > render.yaml << EOF
services:
  - type: web
    name: crypto-bot
    env: python
    buildCommand: pip install -r requirements_crypto_bot.txt
    startCommand: python top100_crypto_bot.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        value: 8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA
    healthCheckPath: /health
    autoDeploy: true
EOF
fi

# Check if requirements_crypto_bot.txt exists
if [ ! -f "requirements_crypto_bot.txt" ]; then
    echo "📝 Creating requirements_crypto_bot.txt..."
    cat > requirements_crypto_bot.txt << EOF
python-telegram-bot
aiohttp
schedule
python-dotenv
requests
EOF
fi

# Check if top100_crypto_bot.py exists
if [ ! -f "top100_crypto_bot.py" ]; then
    echo "❌ top100_crypto_bot.py not found!"
    echo "Please make sure your bot file exists."
    exit 1
fi

echo "✅ Files ready for Render deployment!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to: https://render.com/"
echo "2. Sign up with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect your repository"
echo "5. Configure settings:"
echo "   - Name: crypto-bot"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements_crypto_bot.txt"
echo "   - Start Command: python top100_crypto_bot.py"
echo "6. Set environment variable:"
echo "   - Key: TELEGRAM_BOT_TOKEN"
echo "   - Value: 8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
echo "7. Click 'Create Web Service'"
echo ""
echo "🎉 Your bot will be running 24/7 on Render!"
echo "💰 Cost: $0/month (750 hours free)"
echo "🌍 Global access: Worldwide availability"
echo "⏰ Uptime: 24/7 never sleeps"
