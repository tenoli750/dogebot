#!/usr/bin/env python3
"""
Ultra-simple crypto bot that definitely works
"""

import asyncio
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text("🚀 Crypto Bot is working!\nUse /price bitcoin to test")

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /price command"""
    if not context.args:
        await update.message.reply_text("Please specify a coin. Example: /price bitcoin")
        return
    
    coin = context.args[0].lower()
    
    # Simple price simulation for testing
    if coin in ['bitcoin', 'btc']:
        await update.message.reply_text("💰 Bitcoin: $112,941.00 📈 +2.5%")
    elif coin in ['ethereum', 'eth']:
        await update.message.reply_text("💰 Ethereum: $3,400.50 📉 -1.2%")
    elif coin in ['solana', 'sol']:
        await update.message.reply_text("💰 Solana: $200.30 📈 +5.8%")
    else:
        await update.message.reply_text(f"❌ Unsupported coin: {coin}\nTry: bitcoin, ethereum, solana")

def main():
    """Main function"""
    BOT_TOKEN = "8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("price", price_command))
    
    logger.info("🚀 Simple Crypto Bot started!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
