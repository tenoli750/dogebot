#!/usr/bin/env python3
"""
Working Crypto Price Bot for Telegram
Fixed event loop issues
"""

import asyncio
import aiohttp
import signal
import sys
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkingCryptoBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.session = None
        self.supported_coins = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'binancecoin': 'binancecoin', 'bnb': 'binancecoin',
            'cardano': 'cardano', 'ada': 'cardano',
            'solana': 'solana', 'sol': 'solana',
            'polkadot': 'polkadot', 'dot': 'polkadot',
            'chainlink': 'chainlink', 'link': 'chainlink',
            'litecoin': 'litecoin', 'ltc': 'litecoin',
            'bitcoin-cash': 'bitcoin-cash', 'bch': 'bitcoin-cash',
            'stellar': 'stellar', 'xlm': 'stellar'
        }
    
    async def start_session(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def get_crypto_price(self, symbol: str):
        """Get current crypto price from CoinGecko API"""
        if not self.session:
            await self.start_session()
        
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': symbol,
                'vs_currencies': 'usd,eur,btc',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if symbol in data:
                        return data[symbol]
                return None
                
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🚀 **Crypto Price Bot**

Get real-time cryptocurrency prices!

**Commands:**
/price <coin> - Get current price
/help - Show this help

**Supported Coins:**
BTC, ETH, BNB, ADA, SOL, DOT, LINK, LTC, BCH, XLM

**Examples:**
/price bitcoin
/price ethereum
/price solana
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /price command"""
        if not context.args:
            await update.message.reply_text("Please specify a coin. Example: /price bitcoin")
            return
        
        coin = context.args[0].lower()
        if coin not in self.supported_coins:
            await update.message.reply_text(f"❌ Unsupported coin: {coin}\nSupported: BTC, ETH, BNB, ADA, SOL, DOT, LINK, LTC, BCH, XLM")
            return
        
        symbol = self.supported_coins[coin]
        await update.message.reply_text(f"🔍 Fetching {coin.upper()} price...")
        
        price_data = await self.get_crypto_price(symbol)
        if not price_data:
            await update.message.reply_text(f"❌ Could not fetch price for {coin.upper()}")
            return
        
        current_price = price_data.get('usd', 0)
        change_24h = price_data.get('usd_24h_change', 0)
        volume_24h = price_data.get('usd_24h_vol', 0)
        
        change_emoji = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
        
        message = f"""
💰 **{coin.upper()} Price**

💵 **Current:** ${current_price:,.2f}
{change_emoji} **24h Change:** {change_24h:+.2f}%
📊 **24h Volume:** ${volume_24h:,.0f}

🕐 {datetime.now().strftime('%H:%M:%S')}
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Crypto Price Bot Help**

**Commands:**
/start - Welcome message
/price <coin> - Get current price
/help - Show this help

**Supported Coins:**
Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB)
Cardano (ADA), Solana (SOL), Polkadot (DOT)
Chainlink (LINK), Litecoin (LTC), Bitcoin Cash (BCH), Stellar (XLM)

**Examples:**
/price bitcoin
/price ethereum
/price solana

**Group Usage:**
Just use the commands normally in groups!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general messages - only respond to direct mentions in groups"""
        message = update.message.text
        
        # In groups, only respond to direct mentions or commands
        if update.message.chat.type in ['group', 'supergroup']:
            if not (message.startswith('/') or 
                   (context.bot.username and f"@{context.bot.username}" in message)):
                return
        
        # Handle price requests in natural language
        if any(word in message.lower() for word in ['price', 'cost', 'value', 'worth']):
            # Extract coin name from message
            for coin in self.supported_coins.keys():
                if coin in message.lower():
                    context.args = [coin]
                    await self.price_command(update, context)
                    return
        
        # Default response
        await update.message.reply_text(
            "Use /price <coin> to get crypto prices!\n"
            "Example: /price bitcoin"
        )

def main():
    """Main function to run the bot"""
    BOT_TOKEN = "8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
    
    # Create bot instance
    bot = WorkingCryptoBot(BOT_TOKEN)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("price", bot.price_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Start bot
    async def run_bot():
        await bot.start_session()
        logger.info("🚀 Crypto Bot started!")
        
        try:
            await application.run_polling()
        finally:
            await bot.close_session()
    
    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Stopping bot...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the bot
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
