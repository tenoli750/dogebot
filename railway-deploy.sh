#!/bin/bash

# Railway Deployment Script for Crypto Bot
# This script automates the deployment to Railway

echo "🚀 Railway Crypto Bot Deployment"
echo "==============================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway:"
    railway login
fi

echo "✅ Railway CLI is ready"

# Create railway.json if it doesn't exist
if [ ! -f "railway.json" ]; then
    echo "📝 Creating railway.json..."
    cat > railway.json << EOF
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python top100_crypto_bot.py"
  }
}
EOF
fi

# Set environment variables
echo "🔧 Setting environment variables..."
railway variables set TELEGRAM_BOT_TOKEN=8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA

# Deploy the bot
echo "🚀 Deploying crypto bot to Railway..."
railway deploy

echo "✅ Deployment complete!"
echo "🌍 Your bot is now running on Railway!"
echo "📊 Check logs: railway logs"
echo "🔧 Manage: railway dashboard"
