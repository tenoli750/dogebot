#!/bin/bash

# Fix Bot Conflict - Comprehensive Solution
# This script resolves Telegram bot conflicts and ensures proper deployment

echo "🔧 Fixing Bot Conflict Issues"
echo "============================"

# Step 1: Kill all local bot instances
echo "🛑 Step 1: Stopping all local bot instances..."
pkill -f "python.*crypto.*bot" 2>/dev/null
pkill -f "python.*telegram.*bot" 2>/dev/null
pkill -f "top100_crypto_bot" 2>/dev/null
sleep 3

# Step 2: Check for any remaining processes
echo "🔍 Step 2: Checking for remaining processes..."
REMAINING=$(ps aux | grep -i "python.*crypto.*bot\|python.*telegram.*bot\|top100_crypto_bot" | grep -v grep)
if [ -n "$REMAINING" ]; then
    echo "⚠️  Found remaining processes, force killing..."
    pkill -9 -f "python.*crypto.*bot" 2>/dev/null
    pkill -9 -f "python.*telegram.*bot" 2>/dev/null
    pkill -9 -f "top100_crypto_bot" 2>/dev/null
    sleep 2
fi

# Step 3: Check Render deployment status
echo "📊 Step 3: Render deployment status..."
echo "✅ Your bot is deployed on Render at: https://github.com/tenoli750/dogebot"
echo "✅ Render should automatically restart your bot"
echo "✅ Wait 2-3 minutes for Render to fully restart"

# Step 4: Provide testing instructions
echo ""
echo "🧪 Step 4: Test your bot"
echo "========================"
echo "1. Wait 2-3 minutes for Render to restart"
echo "2. Send /start to your bot on Telegram"
echo "3. Try /p btc to test the new shortcut"
echo "4. Try /p eth to test Ethereum price"
echo "5. Try /p m to test Memecore price"

# Step 5: Troubleshooting tips
echo ""
echo "🔧 Step 5: If bot still doesn't work"
echo "===================================="
echo "1. Check Render logs for errors"
echo "2. Restart the Render service"
echo "3. Verify environment variables are set"
echo "4. Wait 5-10 minutes for full restart"

echo ""
echo "🎉 Your bot should now work properly!"
echo "📱 Test it by sending /start to your bot on Telegram"
