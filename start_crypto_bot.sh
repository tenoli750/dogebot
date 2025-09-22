#!/bin/bash

# Start Crypto Alarm Bot with ROMA Integration
# Make sure ROMA server is running first!

echo "🚀 Starting Crypto Alarm Bot..."
echo "Bot: @dogiris_bot"
echo "Token: 8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
echo ""

# Check if ROMA server is running
echo "🔍 Checking ROMA server status..."
if curl -s http://localhost:5000/api/simple/status > /dev/null; then
    echo "✅ ROMA server is running on localhost:5000"
else
    echo "❌ ROMA server is not running!"
    echo "Please start ROMA server first:"
    echo "  python -m src.sentientresearchagent.server.main --port 5000"
    exit 1
fi

# Install requirements if needed
echo "📦 Installing requirements..."
pip install -r requirements_crypto_bot.txt

# Start the bot
echo "🤖 Starting crypto alarm bot..."
python crypto_alarm_bot.py
