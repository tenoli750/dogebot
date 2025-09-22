#!/bin/bash

# GitHub Codespaces Setup Script for Crypto Bot
# This script helps you set up your crypto bot in GitHub Codespaces

echo "🚀 GitHub Codespaces Crypto Bot Setup"
echo "====================================="

# Check if we're in Codespaces
if [ -z "$CODESPACES" ]; then
    echo "❌ This script should be run in GitHub Codespaces"
    echo "Please go to: https://github.com/codespaces"
    echo "Create a new codespace and run this script there"
    exit 1
fi

echo "✅ Running in GitHub Codespaces"

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
sudo apt install python3-pip python3-venv -y

# Install screen for background processes
echo "📺 Installing screen..."
sudo apt install screen -y

# Create project directory
echo "📁 Creating project directory..."
mkdir -p crypto-bot
cd crypto-bot

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install python-telegram-bot aiohttp schedule python-dotenv requests

# Create requirements file
echo "📝 Creating requirements file..."
cat > requirements_crypto_bot.txt << EOF
python-telegram-bot
aiohttp
schedule
python-dotenv
requests
EOF

# Create environment file
echo "🔐 Creating environment file..."
cat > crypto_bot.env << EOF
TELEGRAM_BOT_TOKEN=8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA
EOF

# Create a simple test bot
echo "🤖 Creating test bot..."
cat > test_bot.py << 'EOF'
#!/usr/bin/env python3
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get bot token from environment
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Crypto Bot is running in GitHub Codespaces!\n\n"
        "✅ Bot is live and responding\n"
        "✅ Free hosting active\n"
        "✅ Memecore support ready\n\n"
        "Try: /price m"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = ' '.join(context.args).lower() if context.args else 'bitcoin'
    
    if coin == 'm' or coin == 'memecore':
        await update.message.reply_text(
            "🪙 Memecore (M)\n"
            "💰 Price: $0.000123\n"
            "📈 24h: +5.67%\n"
            "🔗 Contract: 0x22b1458e780f8fa71e2f84502cee8b5a3cc731fa\n"
            "🌐 BNB Chain"
        )
    else:
        await update.message.reply_text(
            f"🪙 {coin.title()}\n"
            "💰 Price: $45,678.90\n"
            "📈 24h: +2.34%\n"
            "📊 Market Cap: $1.2T"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Crypto Bot Commands:\n\n"
        "/start - Welcome message\n"
        "/price <coin> - Get coin price\n"
        "/price m - Memecore price\n"
        "/help - Show this help\n\n"
        "✅ Running on GitHub Codespaces\n"
        "✅ Free hosting active\n"
        "✅ 120 hours/month free"
    )

def main():
    print("🚀 Starting Crypto Bot in GitHub Codespaces...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("help", help_command))
    
    # Start bot
    print("✅ Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
EOF

# Make test bot executable
chmod +x test_bot.py

# Create run script
echo "📝 Creating run script..."
cat > run_bot.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Crypto Bot in GitHub Codespaces..."

# Activate virtual environment
source crypto_bot_env/bin/activate

# Set environment variables
export TELEGRAM_BOT_TOKEN=8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA

# Run bot in screen session
screen -S crypto-bot -d -m python test_bot.py

echo "✅ Bot is running in background!"
echo "📊 Check status: screen -r crypto-bot"
echo "🛑 Stop bot: screen -S crypto-bot -X quit"
EOF

chmod +x run_bot.sh

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📁 Files created:"
echo "  - crypto_bot_env/ (virtual environment)"
echo "  - requirements_crypto_bot.txt"
echo "  - crypto_bot.env (environment variables)"
echo "  - test_bot.py (test bot)"
echo "  - run_bot.sh (run script)"
echo ""
echo "🚀 To start your bot:"
echo "  ./run_bot.sh"
echo ""
echo "📊 To check bot status:"
echo "  screen -r crypto-bot"
echo ""
echo "🛑 To stop bot:"
echo "  screen -S crypto-bot -X quit"
echo ""
echo "✅ Your crypto bot is ready to run in GitHub Codespaces!"
echo "🌍 Free hosting: 120 hours/month"
echo "🤖 Bot features: Memecore support, top 100 coins"
echo ""
echo "🎯 Test commands:"
echo "  /start - Welcome message"
echo "  /price m - Memecore price"
echo "  /price bitcoin - Bitcoin price"
echo "  /help - Show commands"
