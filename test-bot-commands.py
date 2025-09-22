#!/usr/bin/env python3

"""
Test Bot Commands
This script helps verify that the bot commands are working correctly
"""

import asyncio
import aiohttp
import os

async def test_bot_commands():
    """Test if the bot is responding to commands"""
    
    # Your bot token
    BOT_TOKEN = "8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
    
    print("🤖 Testing Bot Commands")
    print("======================")
    
    # Test bot info
    async with aiohttp.ClientSession() as session:
        try:
            # Get bot info
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('ok'):
                        bot_info = data['result']
                        print(f"✅ Bot is active: @{bot_info.get('username', 'Unknown')}")
                        print(f"✅ Bot name: {bot_info.get('first_name', 'Unknown')}")
                        print(f"✅ Bot ID: {bot_info.get('id', 'Unknown')}")
                    else:
                        print(f"❌ Bot error: {data.get('description', 'Unknown error')}")
                else:
                    print(f"❌ HTTP error: {response.status}")
                    
        except Exception as e:
            print(f"❌ Connection error: {e}")
    
    print("\n📱 Commands to test:")
    print("===================")
    print("1. Send /start to your bot")
    print("2. Send /p btc to test the new shortcut")
    print("3. Send /p eth to test Ethereum")
    print("4. Send /p m to test Memecore")
    print("5. Send /help to see all commands")
    
    print("\n🔧 If /p command doesn't work:")
    print("=============================")
    print("1. Wait 2-3 minutes for Render to restart")
    print("2. Try /price btc instead of /p btc")
    print("3. Check Render logs for errors")
    print("4. Restart Render service if needed")

if __name__ == "__main__":
    asyncio.run(test_bot_commands())
