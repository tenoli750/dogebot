#!/usr/bin/env python3

"""
Check Bot Status
Simple script to check if the bot is working
"""

import requests
import json

def check_bot_status():
    """Check if the bot is responding"""
    
    BOT_TOKEN = "8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
    
    print("🤖 Checking Bot Status")
    print("====================")
    
    try:
        # Get bot info
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Bot is active: @{bot_info.get('username', 'Unknown')}")
                print(f"✅ Bot name: {bot_info.get('first_name', 'Unknown')}")
                print(f"✅ Bot ID: {bot_info.get('id', 'Unknown')}")
                print(f"✅ Bot can read messages: {bot_info.get('can_read_all_group_messages', False)}")
                print(f"✅ Bot supports inline queries: {bot_info.get('supports_inline_queries', False)}")
            else:
                print(f"❌ Bot error: {data.get('description', 'Unknown error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print("\n📱 Test Commands:")
    print("================")
    print("1. Send /start to your bot")
    print("2. Send /p btc to test the new shortcut")
    print("3. Send /price btc if /p doesn't work")
    print("4. Send /help to see all commands")
    
    print("\n🔧 Troubleshooting:")
    print("===================")
    print("1. Wait 2-3 minutes for Render to restart")
    print("2. Check Render logs for errors")
    print("3. Try /price instead of /p")
    print("4. Restart Render service if needed")

if __name__ == "__main__":
    check_bot_status()
