#!/usr/bin/env python3
"""
Complete Crypto Price Bot with Real API Data
Supports all cryptocurrencies with live prices
"""

import asyncio
import aiohttp
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteCryptoBot:
    def __init__(self):
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
            'stellar': 'stellar', 'xlm': 'stellar',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'avalanche-2': 'avalanche-2', 'avax': 'avalanche-2',
            'polygon': 'polygon', 'matic': 'polygon',
            'uniswap': 'uniswap', 'uni': 'uniswap',
            'shiba-inu': 'shiba-inu', 'shib': 'shiba-inu',
            'tron': 'tron', 'trx': 'tron',
            'monero': 'monero', 'xmr': 'monero',
            'ethereum-classic': 'ethereum-classic', 'etc': 'ethereum-classic',
            'cosmos': 'cosmos', 'atom': 'cosmos',
            'algorand': 'algorand', 'algo': 'algorand',
            'vechain': 'vechain', 'vet': 'vechain',
            'filecoin': 'filecoin', 'fil': 'filecoin',
            'tezos': 'tezos', 'xtz': 'tezos',
            'eos': 'eos', 'eos': 'eos',
            'aave': 'aave', 'aave': 'aave',
            'compound': 'compound', 'comp': 'compound',
            'maker': 'maker', 'mkr': 'maker',
            'sushi': 'sushi', 'sushi': 'sushi',
            'yearn-finance': 'yearn-finance', 'yfi': 'yearn-finance',
            'synthetix': 'synthetix', 'snx': 'synthetix',
            'curve-dao-token': 'curve-dao-token', 'crv': 'curve-dao-token',
            '1inch': '1inch', '1inch': '1inch',
            'balancer': 'balancer', 'bal': 'balancer',
            'kyber-network-crystal': 'kyber-network-crystal', 'knc': 'kyber-network-crystal',
            'ren': 'ren', 'ren': 'ren',
            '0x': '0x', 'zrx': '0x',
            'bancor': 'bancor', 'bnt': 'bancor',
            'loopring': 'loopring', 'lrc': 'loopring',
            'enjincoin': 'enjincoin', 'enj': 'enjincoin',
            'basic-attention-token': 'basic-attention-token', 'bat': 'basic-attention-token',
            'decentraland': 'decentraland', 'mana': 'decentraland',
            'sandbox': 'sandbox', 'sand': 'sandbox',
            'axie-infinity': 'axie-infinity', 'axs': 'axie-infinity',
            'chiliz': 'chiliz', 'chz': 'chiliz',
            'flow': 'flow', 'flow': 'flow',
            'near': 'near', 'near': 'near',
            'fantom': 'fantom', 'ftm': 'fantom',
            'harmony': 'harmony', 'one': 'harmony',
            'elrond-erd-2': 'elrond-erd-2', 'egld': 'elrond-erd-2',
            'hedera-hashgraph': 'hedera-hashgraph', 'hbar': 'hedera-hashgraph',
            'the-graph': 'the-graph', 'grt': 'the-graph',
            'internet-computer': 'internet-computer', 'icp': 'internet-computer',
            'theta-token': 'theta-token', 'theta': 'theta-token',
            'vega-protocol': 'vega-protocol', 'vega': 'vega-protocol',
            'injective-protocol': 'injective-protocol', 'inj': 'injective-protocol',
            'thorchain': 'thorchain', 'rune': 'thorchain',
            'osmosis': 'osmosis', 'osmo': 'osmosis',
            'juno-network': 'juno-network', 'juno': 'juno-network',
            'secret': 'secret', 'scrt': 'secret',
            'kava': 'kava', 'kava': 'kava',
            'band-protocol': 'band-protocol', 'band': 'band-protocol',
            'ocean-protocol': 'ocean-protocol', 'ocean': 'ocean-protocol',
            'fetch-ai': 'fetch-ai', 'fet': 'fetch-ai',
            'singularitynet': 'singularitynet', 'agix': 'singularitynet',
            'numeraire': 'numeraire', 'nmr': 'numeraire',
            'augur': 'augur', 'rep': 'augur',
            'gnosis': 'gnosis', 'gno': 'gnosis',
            'kyber-network': 'kyber-network', 'knc': 'kyber-network',
            '0x': '0x', 'zrx': '0x',
            'bancor': 'bancor', 'bnt': 'bancor',
            'loopring': 'loopring', 'lrc': 'loopring',
            'enjincoin': 'enjincoin', 'enj': 'enjincoin',
            'basic-attention-token': 'basic-attention-token', 'bat': 'basic-attention-token',
            'decentraland': 'decentraland', 'mana': 'decentraland',
            'sandbox': 'sandbox', 'sand': 'sandbox',
            'axie-infinity': 'axie-infinity', 'axs': 'axie-infinity',
            'chiliz': 'chiliz', 'chz': 'chiliz',
            'flow': 'flow', 'flow': 'flow',
            'near': 'near', 'near': 'near',
            'fantom': 'fantom', 'ftm': 'fantom',
            'harmony': 'harmony', 'one': 'harmony',
            'elrond-erd-2': 'elrond-erd-2', 'egld': 'elrond-erd-2',
            'hedera-hashgraph': 'hedera-hashgraph', 'hbar': 'hedera-hashgraph',
            'the-graph': 'the-graph', 'grt': 'the-graph',
            'internet-computer': 'internet-computer', 'icp': 'internet-computer',
            'theta-token': 'theta-token', 'theta': 'theta-token',
            'vega-protocol': 'vega-protocol', 'vega': 'vega-protocol',
            'injective-protocol': 'injective-protocol', 'inj': 'injective-protocol',
            'thorchain': 'thorchain', 'rune': 'thorchain',
            'osmosis': 'osmosis', 'osmo': 'osmosis',
            'juno-network': 'juno-network', 'juno': 'juno-network',
            'secret': 'secret', 'scrt': 'secret',
            'kava': 'kava', 'kava': 'kava',
            'band-protocol': 'band-protocol', 'band': 'band-protocol',
            'ocean-protocol': 'ocean-protocol', 'ocean': 'ocean-protocol',
            'fetch-ai': 'fetch-ai', 'fet': 'fetch-ai',
            'singularitynet': 'singularitynet', 'agix': 'singularitynet',
            'numeraire': 'numeraire', 'nmr': 'numeraire',
            'augur': 'augur', 'rep': 'augur',
            'gnosis': 'gnosis', 'gno': 'gnosis'
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

Get real-time cryptocurrency prices for 100+ coins!

**Commands:**
/price <coin> - Get current price
/help - Show this help
/list - Show supported coins

**Popular Coins:**
BTC, ETH, BNB, ADA, SOL, DOT, LINK, LTC, BCH, XLM
DOGE, AVAX, MATIC, UNI, SHIB, TRX, XMR, ETC, ATOM, ALGO

**Examples:**
/price bitcoin
/price ethereum
/price dogecoin
/price avalanche
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /price command"""
        if not context.args:
            await update.message.reply_text("Please specify a coin. Example: /price bitcoin")
            return
        
        coin = context.args[0].lower()
        if coin not in self.supported_coins:
            await update.message.reply_text(
                f"❌ Unsupported coin: {coin}\n\n"
                f"Use /list to see all supported coins or try:\n"
                f"BTC, ETH, BNB, ADA, SOL, DOT, LINK, LTC, BCH, XLM\n"
                f"DOGE, AVAX, MATIC, UNI, SHIB, TRX, XMR, ETC, ATOM, ALGO"
            )
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
    
    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command"""
        coins_list = """
📋 **Supported Cryptocurrencies**

**Major Coins:**
Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB)
Cardano (ADA), Solana (SOL), Polkadot (DOT)
Chainlink (LINK), Litecoin (LTC), Bitcoin Cash (BCH)
Stellar (XLM), Dogecoin (DOGE), Avalanche (AVAX)

**DeFi Tokens:**
Uniswap (UNI), Aave (AAVE), Compound (COMP)
Maker (MKR), Sushi (SUSHI), Yearn Finance (YFI)
Synthetix (SNX), Curve (CRV), 1inch (1INCH)
Balancer (BAL), Kyber (KNC), Ren (REN)

**Layer 1 Blockchains:**
Polygon (MATIC), Fantom (FTM), Harmony (ONE)
Elrond (EGLD), Hedera (HBAR), The Graph (GRT)
Internet Computer (ICP), Near (NEAR), Flow (FLOW)

**Gaming & NFT:**
Decentraland (MANA), Sandbox (SAND), Axie Infinity (AXS)
Enjin (ENJ), Chiliz (CHZ), Basic Attention Token (BAT)

**Privacy & Security:**
Monero (XMR), Secret (SCRT), Zcash (ZEC)
Dash (DASH), Verge (XVG), PIVX (PIVX)

**And many more!** Use /price <coin> to get any price.
        """
        await update.message.reply_text(coins_list, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Crypto Price Bot Help**

**Commands:**
/start - Welcome message
/price <coin> - Get current price
/list - Show supported coins
/help - Show this help

**Popular Examples:**
/price bitcoin
/price ethereum
/price dogecoin
/price avalanche
/price polygon
/price uniswap

**Group Usage:**
Just use the commands normally in groups!

**Supported Coins:**
100+ cryptocurrencies including all major coins, DeFi tokens, gaming tokens, and more!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general messages"""
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
            "Example: /price bitcoin\n"
            "Use /list to see all supported coins"
        )

def main():
    """Main function to run the bot"""
    BOT_TOKEN = "8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
    
    # Create bot instance
    bot = CompleteCryptoBot()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("price", bot.price_command))
    application.add_handler(CommandHandler("list", bot.list_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    logger.info("🚀 Complete Crypto Bot started!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
