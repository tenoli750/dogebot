#!/bin/bash

# Stop Local Crypto Bot Instances
# This script helps stop any local bot instances that might conflict with Render

echo "🛑 Stopping Local Crypto Bot Instances"
echo "======================================"

# Kill any running crypto bot processes
echo "🔍 Looking for running crypto bot processes..."

# Check for Python processes with crypto bot
CRYPTO_PROCESSES=$(ps aux | grep -i "python.*crypto.*bot" | grep -v grep)

if [ -n "$CRYPTO_PROCESSES" ]; then
    echo "📋 Found running crypto bot processes:"
    echo "$CRYPTO_PROCESSES"
    echo ""
    
    # Kill the processes
    echo "🛑 Stopping processes..."
    pkill -f "python.*crypto.*bot"
    sleep 2
    
    # Check if processes are still running
    REMAINING=$(ps aux | grep -i "python.*crypto.*bot" | grep -v grep)
    if [ -n "$REMAINING" ]; then
        echo "⚠️  Some processes still running, force killing..."
        pkill -9 -f "python.*crypto.*bot"
    fi
    
    echo "✅ Local bot instances stopped"
else
    echo "✅ No local crypto bot processes found"
fi

echo ""
echo "🚀 Your bot should now run properly on Render!"
echo "📱 Test it by sending /start to your bot on Telegram"
echo ""
echo "🔧 If you still get conflicts:"
echo "1. Wait 2-3 minutes for Render to fully restart"
echo "2. Check Render logs for any errors"
echo "3. Make sure only one bot instance is running"
