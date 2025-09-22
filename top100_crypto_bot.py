#!/usr/bin/env python3
"""
Top 100 Crypto Price Bot - Clean and Simple
No conflicts, no loops, just works!
"""

import asyncio
import aiohttp
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Top100CryptoBot:
    def __init__(self):
        self.session = None
        # Top 100 cryptocurrencies by market cap
        self.supported_coins = {
            # Top 20
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'tether': 'tether', 'usdt': 'tether',
            'binancecoin': 'binancecoin', 'bnb': 'binancecoin',
            'solana': 'solana', 'sol': 'solana',
            'usd-coin': 'usd-coin', 'usdc': 'usd-coin',
            'xrp': 'xrp', 'xrp': 'xrp',
            'staked-ether': 'staked-ether', 'steth': 'staked-ether',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'memecore': 'memecore', 'm': 'memecore',
            'cardano': 'cardano', 'ada': 'cardano',
            'tron': 'tron', 'trx': 'tron',
            'avalanche-2': 'avalanche-2', 'avax': 'avalanche-2',
            'chainlink': 'chainlink', 'link': 'chainlink',
            'polkadot': 'polkadot', 'dot': 'polkadot',
            'bitcoin-cash': 'bitcoin-cash', 'bch': 'bitcoin-cash',
            'near': 'near', 'near': 'near',
            'polygon': 'polygon', 'matic': 'polygon',
            'litecoin': 'litecoin', 'ltc': 'litecoin',
            'internet-computer': 'internet-computer', 'icp': 'internet-computer',
            'uniswap': 'uniswap', 'uni': 'uniswap',
            'ethereum-classic': 'ethereum-classic', 'etc': 'ethereum-classic',
            
            # 21-40
            'stellar': 'stellar', 'xlm': 'stellar',
            'monero': 'monero', 'xmr': 'monero',
            'cosmos': 'cosmos', 'atom': 'cosmos',
            'aptos': 'aptos', 'apt': 'aptos',
            'filecoin': 'filecoin', 'fil': 'filecoin',
            'hedera-hashgraph': 'hedera-hashgraph', 'hbar': 'hedera-hashgraph',
            'vechain': 'vechain', 'vet': 'vechain',
            'cronos': 'cronos', 'cro': 'cronos',
            'arbitrum': 'arbitrum', 'arb': 'arbitrum',
            'algorand': 'algorand', 'algo': 'algorand',
            'the-graph': 'the-graph', 'grt': 'the-graph',
            'optimism': 'optimism', 'op': 'optimism',
            'fantom': 'fantom', 'ftm': 'fantom',
            'apecoin': 'apecoin', 'ape': 'apecoin',
            'elrond-erd-2': 'elrond-erd-2', 'egld': 'elrond-erd-2',
            'the-sandbox': 'the-sandbox', 'sand': 'the-sandbox',
            'decentraland': 'decentraland', 'mana': 'decentraland',
            'axie-infinity': 'axie-infinity', 'axs': 'axie-infinity',
            'chiliz': 'chiliz', 'chz': 'chiliz',
            'flow': 'flow', 'flow': 'flow',
            'tezos': 'tezos', 'xtz': 'tezos',
            'eos': 'eos', 'eos': 'eos',
            'aave': 'aave', 'aave': 'aave',
            'quant-network': 'quant-network', 'qnt': 'quant-network',
            'theta-token': 'theta-token', 'theta': 'theta-token',
            'bitcoin-sv': 'bitcoin-sv', 'bsv': 'bitcoin-sv',
            'maker': 'maker', 'mkr': 'maker',
            'compound': 'compound', 'comp': 'compound',
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
            'harmony': 'harmony', 'one': 'harmony',
            'dash': 'dash', 'dash': 'dash',
            'zcash': 'zcash', 'zec': 'zcash',
            'neo': 'neo', 'neo': 'neo',
            'waves': 'waves', 'waves': 'waves',
            'qtum': 'qtum', 'qtum': 'qtum',
            'icon': 'icon', 'icx': 'icon',
            'ontology': 'ontology', 'ont': 'ontology',
            'nano': 'nano', 'nano': 'nano',
            'decred': 'decred', 'dcr': 'decred',
            'verge': 'verge', 'xvg': 'verge',
            'siacoin': 'siacoin', 'sc': 'siacoin',
            'steem': 'steem', 'steem': 'steem',
            'augur': 'augur', 'rep': 'augur',
            'golem': 'golem', 'gnt': 'golem',
            'status': 'status', 'snt': 'status',
            'district0x': 'district0x', 'dnt': 'district0x',
            'civic': 'civic', 'cvc': 'civic',
            'funfair': 'funfair', 'fun': 'funfair',
            'salt': 'salt', 'salt': 'salt',
            'power-ledger': 'power-ledger', 'powr': 'power-ledger',
            'cindicator': 'cindicator', 'cnd': 'cindicator',
            'wax': 'wax', 'waxp': 'wax',
            'dentacoin': 'dentacoin', 'dnt': 'dentacoin',
            'dent': 'dent', 'dent': 'dent',
            'adx-net': 'adx-net', 'adx': 'adx-net',
            'melon': 'melon', 'mln': 'melon',
            'gnosis': 'gnosis', 'gno': 'gnosis',
            'numeraire': 'numeraire', 'nmr': 'numeraire',
            'augur': 'augur', 'rep': 'augur',
            'golem': 'golem', 'gnt': 'golem',
            'status': 'status', 'snt': 'status',
            'district0x': 'district0x', 'dnt': 'district0x',
            'civic': 'civic', 'cvc': 'civic',
            'funfair': 'funfair', 'fun': 'funfair',
            'salt': 'salt', 'salt': 'salt',
            'power-ledger': 'power-ledger', 'powr': 'power-ledger',
            'cindicator': 'cindicator', 'cnd': 'cindicator',
            'wax': 'wax', 'waxp': 'wax',
            'dentacoin': 'dentacoin', 'dnt': 'dentacoin',
            'dent': 'dent', 'dent': 'dent',
            'adx-net': 'adx-net', 'adx': 'adx-net',
            'melon': 'melon', 'mln': 'melon',
            'gnosis': 'gnosis', 'gno': 'gnosis',
            'numeraire': 'numeraire', 'nmr': 'numeraire'
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
🚀 **Top 100 Crypto Price Bot**

Get real-time prices for the top 100 cryptocurrencies!

**Commands:**
/price <coin> - Get current price
/top10 - Show top 10 coins
/top20 - Show top 20 coins
/help - Show this help

**Popular Examples:**
/price bitcoin
/price ethereum
/price solana
/price dogecoin
/price memecore
/price m
/price cardano
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
                f"Try popular coins like:\n"
                f"BTC, ETH, SOL, DOGE, ADA, AVAX, LINK, DOT, BCH, NEAR, MATIC, LTC, ICP, UNI, ETC"
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
    
    async def top10_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /top10 command"""
        top10_coins = [
            'bitcoin', 'ethereum', 'tether', 'binancecoin', 'solana',
            'usd-coin', 'xrp', 'staked-ether', 'dogecoin', 'cardano'
        ]
        
        await update.message.reply_text("🔍 Fetching top 10 crypto prices...")
        
        results = []
        for coin in top10_coins:
            price_data = await self.get_crypto_price(coin)
            if price_data:
                current_price = price_data.get('usd', 0)
                change_24h = price_data.get('usd_24h_change', 0)
                change_emoji = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
                
                coin_name = coin.replace('-', ' ').title()
                results.append(f"{coin_name}: ${current_price:,.2f} {change_emoji} {change_24h:+.2f}%")
        
        if results:
            message = "🏆 **Top 10 Cryptocurrencies**\n\n" + "\n".join(results)
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Could not fetch top 10 prices")
    
    async def top20_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /top20 command"""
        top20_coins = [
            'bitcoin', 'ethereum', 'tether', 'binancecoin', 'solana',
            'usd-coin', 'xrp', 'staked-ether', 'dogecoin', 'cardano',
            'tron', 'avalanche-2', 'chainlink', 'polkadot', 'bitcoin-cash',
            'near', 'polygon', 'litecoin', 'internet-computer', 'uniswap'
        ]
        
        await update.message.reply_text("🔍 Fetching top 20 crypto prices...")
        
        results = []
        for coin in top20_coins:
            price_data = await self.get_crypto_price(coin)
            if price_data:
                current_price = price_data.get('usd', 0)
                change_24h = price_data.get('usd_24h_change', 0)
                change_emoji = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
                
                coin_name = coin.replace('-', ' ').title()
                results.append(f"{coin_name}: ${current_price:,.2f} {change_emoji} {change_24h:+.2f}%")
        
        if results:
            message = "🏆 **Top 20 Cryptocurrencies**\n\n" + "\n".join(results)
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Could not fetch top 20 prices")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Top 100 Crypto Bot Help**

**Commands:**
/start - Welcome message
/price <coin> - Get current price
/top10 - Show top 10 coins
/top20 - Show top 20 coins
/help - Show this help

**Popular Coins:**
Bitcoin (BTC), Ethereum (ETH), Tether (USDT), BNB, Solana (SOL)
USDC, XRP, Staked ETH, Dogecoin (DOGE), Memecore (M)
Cardano (ADA), Tron (TRX), Avalanche (AVAX), Chainlink (LINK), Polkadot (DOT)
Bitcoin Cash (BCH), Near (NEAR), Polygon (MATIC), Litecoin (LTC)

**Meme Coins:**
Memecore (M) - BNB Chain Contract: 0x22b1458e780f8fa71e2f84502cee8b5a3cc731fa

**Examples:**
/price bitcoin
/price ethereum
/price dogecoin
/price memecore
/price m
/top10
/top20

**Group Usage:**
Just use the commands normally in groups!
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
            "Use /top10 or /top20 for market overview"
        )

def main():
    """Main function to run the bot"""
    BOT_TOKEN = "8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA"
    
    # Create bot instance
    bot = Top100CryptoBot()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("price", bot.price_command))
    application.add_handler(CommandHandler("top10", bot.top10_command))
    application.add_handler(CommandHandler("top20", bot.top20_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    logger.info("🚀 Top 100 Crypto Bot started!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
