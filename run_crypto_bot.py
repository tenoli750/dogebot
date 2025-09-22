#!/usr/bin/env python3
"""
Simple script to run the crypto alarm bot
"""

import asyncio
import sys
import os
from crypto_alarm_bot import main

if __name__ == "__main__":
    print("🚀 Starting @dogiris_bot - Crypto Price Alarm Bot")
    print("=" * 60)
    print("Bot Features:")
    print("• Real-time crypto price monitoring")
    print("• Custom price alerts")
    print("• AI-powered market analysis")
    print("• Background price checking")
    print("=" * 60)
    print("Commands available:")
    print("/start - Welcome message")
    print("/price <coin> - Get current price")
    print("/setalert <coin> <price> <above/below> - Set price alert")
    print("/myalerts - View your alerts")
    print("/analysis <coin> - Get AI market analysis")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
