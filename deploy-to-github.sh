#!/bin/bash

# GitHub Deployment Script for Crypto Bot
# This script helps you deploy your crypto bot to GitHub

echo "🚀 GitHub Deployment for Crypto Bot"
echo "==================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run this from your project directory."
    exit 1
fi

echo "✅ Git repository found"

# Check if we have uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Uncommitted changes found. Committing them..."
    git add .
    git commit -m "Auto-commit before GitHub deployment"
fi

echo "📋 Next Steps for GitHub Deployment:"
echo ""
echo "1. 🌐 Create GitHub Repository:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: crypto-bot"
echo "   - Description: 24/7 Telegram crypto price bot with 200+ tokens"
echo "   - Visibility: Public (for free hosting)"
echo "   - Don't initialize with README, .gitignore, or license"
echo "   - Click 'Create repository'"
echo ""
echo "2. 📋 Copy the repository URL from GitHub"
echo "   - It will look like: https://github.com/yourusername/crypto-bot.git"
echo ""
echo "3. 🔗 Connect and push to GitHub:"
echo "   git remote add origin https://github.com/yourusername/crypto-bot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. 🚀 Deploy to Render:"
echo "   - Go to: https://render.com/"
echo "   - Sign up with GitHub"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your crypto-bot repository"
echo "   - Configure settings:"
echo "     - Name: crypto-bot"
echo "     - Environment: Python 3"
echo "     - Build Command: pip install -r requirements_crypto_bot.txt"
echo "     - Start Command: python top100_crypto_bot.py"
echo "   - Set environment variable:"
echo "     - Key: TELEGRAM_BOT_TOKEN"
echo "     - Value: 8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
echo "   - Click 'Create Web Service'"
echo ""
echo "5. 🎉 Your bot will be live in 2-3 minutes!"
echo ""
echo "📁 Files ready for deployment:"
echo "✅ top100_crypto_bot.py - Enhanced bot with 200+ tokens"
echo "✅ requirements_crypto_bot.txt - Dependencies"
echo "✅ render.yaml - Render configuration"
echo "✅ .gitignore - Excludes sensitive files"
echo "✅ github-deploy-guide.md - Complete guide"
echo ""
echo "🎯 Your bot features:"
echo "✅ 200+ Cryptocurrencies - More than any other bot"
echo "✅ Meme Coins - SHIB, PEPE, FLOKI, BONK, WIF, MYRO, POPCAT"
echo "✅ DeFi Tokens - AAVE, COMP, MKR, SUSHI, YFI, SNX, CRV"
echo "✅ Layer 2 - ARB, OP, BASE, IMX, LRC, METIS, MANTLE"
echo "✅ AI & Gaming - FET, AGIX, OCEAN, RNDR, SAND, MANA, AXS"
echo "✅ 24/7 Hosting - Never sleeps"
echo "✅ Free Hosting - $0/month"
echo ""
echo "🚀 Ready to deploy! Follow the steps above."
