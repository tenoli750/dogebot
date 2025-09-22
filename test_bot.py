#!/usr/bin/env python3
"""
Test script to verify the crypto bot setup
"""

import asyncio
import aiohttp
import sqlite3
from crypto_alarm_bot import CryptoAlarmBot

async def test_bot():
    """Test the crypto bot functionality"""
    print("🧪 Testing Crypto Alarm Bot...")
    
    # Test bot initialization
    bot = CryptoAlarmBot("8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA")
    print("✅ Bot initialized successfully")
    
    # Test database
    try:
        conn = sqlite3.connect('crypto_alerts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Database tables: {[table[0] for table in tables]}")
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Test price fetching
    await bot.start_session()
    try:
        price_data = await bot.get_crypto_price('bitcoin')
        if price_data:
            print(f"✅ Bitcoin price: ${price_data.get('usd', 0):,.2f}")
        else:
            print("❌ Could not fetch Bitcoin price")
    except Exception as e:
        print(f"❌ Price fetching error: {e}")
    finally:
        await bot.close_session()
    
    print("🎉 Bot test completed!")

if __name__ == "__main__":
    asyncio.run(test_bot())
