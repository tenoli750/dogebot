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
        # Top 100+ cryptocurrencies by market cap + popular tokens
        self.supported_coins = {
            # Top 20 Major Coins
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
            
            # Popular Meme Coins
            'shiba-inu': 'shiba-inu', 'shib': 'shiba-inu',
            'pepe': 'pepe', 'pepe': 'pepe',
            'floki': 'floki', 'floki': 'floki',
            'bonk': 'bonk', 'bonk': 'bonk',
            'dogwifhat': 'dogwifhat', 'wif': 'dogwifhat',
            'myro': 'myro', 'myro': 'myro',
            'popcat': 'popcat', 'popcat': 'popcat',
            'bome': 'bome', 'bome': 'bome',
            'wif': 'dogwifhat', 'wif': 'dogwifhat',
            
            # DeFi Tokens
            'aave': 'aave', 'aave': 'aave',
            'compound': 'compound', 'comp': 'compound',
            'maker': 'maker', 'mkr': 'maker',
            'sushi': 'sushi', 'sushi': 'sushi',
            'yearn-finance': 'yearn-finance', 'yfi': 'yearn-finance',
            'synthetix': 'synthetix', 'snx': 'synthetix',
            'curve-dao-token': 'curve-dao-token', 'crv': 'curve-dao-token',
            '1inch': '1inch', '1inch': '1inch',
            'balancer': 'balancer', 'bal': 'balancer',
            'pancakeswap-token': 'pancakeswap-token', 'cake': 'pancakeswap-token',
            'jupiter-exchange-solana': 'jupiter-exchange-solana', 'jup': 'jupiter-exchange-solana',
            'raydium': 'raydium', 'ray': 'raydium',
            'orca': 'orca', 'orca': 'orca',
            
            # Layer 2 & Scaling
            'arbitrum': 'arbitrum', 'arb': 'arbitrum',
            'optimism': 'optimism', 'op': 'optimism',
            'base': 'base', 'base': 'base',
            'polygon': 'polygon', 'matic': 'polygon',
            'immutable-x': 'immutable-x', 'imx': 'immutable-x',
            'loopring': 'loopring', 'lrc': 'loopring',
            
            # AI & Big Data
            'fetch-ai': 'fetch-ai', 'fet': 'fetch-ai',
            'singularitynet': 'singularitynet', 'agix': 'singularitynet',
            'ocean-protocol': 'ocean-protocol', 'ocean': 'ocean-protocol',
            'render-token': 'render-token', 'rndr': 'render-token',
            'akash-network': 'akash-network', 'akt': 'akash-network',
            'bittensor': 'bittensor', 'tao': 'bittensor',
            'worldcoin-wld': 'worldcoin-wld', 'wld': 'worldcoin-wld',
            
            # Gaming & Metaverse
            'the-sandbox': 'the-sandbox', 'sand': 'the-sandbox',
            'decentraland': 'decentraland', 'mana': 'decentraland',
            'axie-infinity': 'axie-infinity', 'axs': 'axie-infinity',
            'gala': 'gala', 'gala': 'gala',
            'enjincoin': 'enjincoin', 'enj': 'enjincoin',
            'illuvium': 'illuvium', 'ilv': 'illuvium',
            'stepn': 'stepn', 'gmt': 'stepn',
            'magic': 'magic', 'magic': 'magic',
            
            # Privacy Coins
            'monero': 'monero', 'xmr': 'monero',
            'zcash': 'zcash', 'zec': 'zcash',
            'dash': 'dash', 'dash': 'dash',
            'horizen': 'horizen', 'zen': 'horizen',
            
            # Storage & Infrastructure
            'filecoin': 'filecoin', 'fil': 'filecoin',
            'arweave': 'arweave', 'ar': 'arweave',
            'sia': 'sia', 'sc': 'sia',
            'storj': 'storj', 'storj': 'storj',
            
            # Oracle & Data
            'chainlink': 'chainlink', 'link': 'chainlink',
            'band-protocol': 'band-protocol', 'band': 'band-protocol',
            'api3': 'api3', 'api3': 'api3',
            'tellor': 'tellor', 'trb': 'tellor',
            
            # Additional Major Coins
            'stellar': 'stellar', 'xlm': 'stellar',
            'cosmos': 'cosmos', 'atom': 'cosmos',
            'aptos': 'aptos', 'apt': 'aptos',
            'hedera-hashgraph': 'hedera-hashgraph', 'hbar': 'hedera-hashgraph',
            'vechain': 'vechain', 'vet': 'vechain',
            'cronos': 'cronos', 'cro': 'cronos',
            'algorand': 'algorand', 'algo': 'algorand',
            'the-graph': 'the-graph', 'grt': 'the-graph',
            'fantom': 'fantom', 'ftm': 'fantom',
            'apecoin': 'apecoin', 'ape': 'apecoin',
            'elrond-erd-2': 'elrond-erd-2', 'egld': 'elrond-erd-2',
            'chiliz': 'chiliz', 'chz': 'chiliz',
            'flow': 'flow', 'flow': 'flow',
            'tezos': 'tezos', 'xtz': 'tezos',
            'eos': 'eos', 'eos': 'eos',
            'quant-network': 'quant-network', 'qnt': 'quant-network',
            'theta-token': 'theta-token', 'theta': 'theta-token',
            'bitcoin-sv': 'bitcoin-sv', 'bsv': 'bitcoin-sv',
            'kyber-network-crystal': 'kyber-network-crystal', 'knc': 'kyber-network-crystal',
            'ren': 'ren', 'ren': 'ren',
            '0x': '0x', 'zrx': '0x',
            'bancor': 'bancor', 'bnt': 'bancor',
            'basic-attention-token': 'basic-attention-token', 'bat': 'basic-attention-token',
            'harmony': 'harmony', 'one': 'harmony',
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
            
            # More Popular Tokens
            'injective': 'injective', 'inj': 'injective',
            'sei': 'sei', 'sei': 'sei',
            'sui': 'sui', 'sui': 'sui',
            'toncoin': 'toncoin', 'ton': 'toncoin',
            'kaspa': 'kaspa', 'kas': 'kaspa',
            'thorchain': 'thorchain', 'rune': 'thorchain',
            'osmosis': 'osmosis', 'osmo': 'osmosis',
            'juno': 'juno', 'juno': 'juno',
            'secret': 'secret', 'scrt': 'secret',
            'kava': 'kava', 'kava': 'kava',
            'terra-luna': 'terra-luna', 'luna': 'terra-luna',
            'terra-luna-2': 'terra-luna-2', 'luna2': 'terra-luna-2',
            'celo': 'celo', 'celo': 'celo',
            'mina': 'mina', 'mina': 'mina',
            'celestia': 'celestia', 'tia': 'celestia',
            'dymension': 'dymension', 'dym': 'dymension',
            'altlayer': 'altlayer', 'alt': 'altlayer',
            'eigenlayer': 'eigenlayer', 'eigen': 'eigenlayer',
            'pendle': 'pendle', 'pendle': 'pendle',
            'ethena': 'ethena', 'ena': 'ethena',
            'wormhole': 'wormhole', 'w': 'wormhole',
            'jito': 'jito', 'jito': 'jito',
            'pyth': 'pyth', 'pyth': 'pyth',
            'tensor': 'tensor', 'tnsr': 'tensor',
            'metis': 'metis', 'metis': 'metis',
            'mantle': 'mantle', 'mnt': 'mantle',
            'blast': 'blast', 'blast': 'blast',
            'mode': 'mode', 'mode': 'mode',
            'zksync': 'zksync', 'zk': 'zksync',
            'linea': 'linea', 'linea': 'linea',
            'scroll': 'scroll', 'scroll': 'scroll',
            'taiko': 'taiko', 'taiko': 'taiko',
            'polygon-zkevm': 'polygon-zkevm', 'polygon': 'polygon-zkevm',
            'starknet': 'starknet', 'strk': 'starknet',
            'dydx': 'dydx', 'dydx': 'dydx',
            'perpetual-protocol': 'perpetual-protocol', 'perp': 'perpetual-protocol',
            'gains-network': 'gains-network', 'gains': 'gains-network',
            'uma': 'uma', 'uma': 'uma',
            'bob': 'bob', 'bob': 'bob',
            'manta': 'manta', 'manta': 'manta',
            'zksync-era': 'zksync-era', 'era': 'zksync-era',
            'layerzero': 'layerzero', 'zro': 'layerzero',
            'stargate-finance': 'stargate-finance', 'stg': 'stargate-finance',
            'axelar': 'axelar', 'axl': 'axelar',
            'chainflip': 'chainflip', 'flip': 'chainflip',
            'squid': 'squid', 'squid': 'squid',
            'router-protocol': 'router-protocol', 'route': 'router-protocol',
            'multichain': 'multichain', 'multi': 'multichain',
            'anyswap': 'anyswap', 'any': 'anyswap',
            'hop-protocol': 'hop-protocol', 'hop': 'hop-protocol',
            'synapse': 'synapse', 'syn': 'synapse',
            'across-protocol': 'across-protocol', 'acx': 'across-protocol',
            'bungee': 'bungee', 'bungee': 'bungee',
            'socket': 'socket', 'socket': 'socket',
            'li-fi': 'li-fi', 'lifi': 'li-fi',
            'jumper': 'jumper', 'jumper': 'jumper',
            'rango': 'rango', 'rango': 'rango',
            'xy-finance': 'xy-finance', 'xy': 'xy-finance',
            'debridge': 'debridge', 'debridge': 'debridge',
            'biconomy': 'biconomy', 'bico': 'biconomy',
            'gelato': 'gelato', 'gel': 'gelato',
            'openzeppelin': 'openzeppelin', 'oz': 'openzeppelin',
            'tenderly': 'tenderly', 'tenderly': 'tenderly',
            'alchemy': 'alchemy', 'alchemy': 'alchemy',
            'infura': 'infura', 'infura': 'infura',
            'quicknode': 'quicknode', 'quicknode': 'quicknode',
            'ankr': 'ankr', 'ankr': 'ankr',
            'pocket-network': 'pocket-network', 'pokt': 'pocket-network',
            'livepeer': 'livepeer', 'lpt': 'livepeer',
            'audius': 'audius', 'audio': 'audius',
            'ipfs': 'ipfs', 'ipfs': 'ipfs',
            'pinata': 'pinata', 'pinata': 'pinata',
            'nft-storage': 'nft-storage', 'nft': 'nft-storage',
            'web3-storage': 'web3-storage', 'web3': 'web3-storage',
            'fleek': 'fleek', 'fleek': 'fleek',
            'skynet': 'skynet', 'skynet': 'skynet',
            'swarm': 'swarm', 'swarm': 'swarm',
            'maidsafe': 'maidsafe', 'maid': 'maidsafe',
            'safe': 'safe', 'safe': 'safe',
            'gnosis-safe': 'gnosis-safe', 'safe': 'gnosis-safe',
            'argent': 'argent', 'argent': 'argent',
            'authereum': 'authereum', 'authereum': 'authereum',
            'portis': 'portis', 'portis': 'portis',
            'torus': 'torus', 'torus': 'torus',
            'fortmatic': 'fortmatic', 'fortmatic': 'fortmatic',
            'walletconnect': 'walletconnect', 'walletconnect': 'walletconnect',
            'rainbow': 'rainbow', 'rainbow': 'rainbow',
            'metamask': 'metamask', 'metamask': 'metamask',
            'coinbase-wallet': 'coinbase-wallet', 'coinbase': 'coinbase-wallet',
            'trust-wallet': 'trust-wallet', 'trust': 'trust-wallet',
            'imtoken': 'imtoken', 'imtoken': 'imtoken',
            'tokenpocket': 'tokenpocket', 'tokenpocket': 'tokenpocket',
            'math-wallet': 'math-wallet', 'math': 'math-wallet',
            'bitpie': 'bitpie', 'bitpie': 'bitpie',
            'coolwallet': 'coolwallet', 'coolwallet': 'coolwallet',
            'ledger': 'ledger', 'ledger': 'ledger',
            'trezor': 'trezor', 'trezor': 'trezor',
            'keepkey': 'keepkey', 'keepkey': 'keepkey',
            'bitbox': 'bitbox', 'bitbox': 'bitbox',
            'coldcard': 'coldcard', 'coldcard': 'coldcard',
            'cobo': 'cobo', 'cobo': 'cobo',
            'casa': 'casa', 'casa': 'casa',
            'unchained-capital': 'unchained-capital', 'unchained': 'unchained-capital',
            'coinkite': 'coinkite', 'coinkite': 'coinkite',
            'opendime': 'opendime', 'opendime': 'opendime',
            'jade': 'jade', 'jade': 'jade',
            'specter': 'specter', 'specter': 'specter',
            'electrum': 'electrum', 'electrum': 'electrum',
            'wasabi': 'wasabi', 'wasabi': 'wasabi',
            'samourai': 'samourai', 'samourai': 'samourai',
            'sparrow': 'sparrow', 'sparrow': 'sparrow',
            'bluewallet': 'bluewallet', 'bluewallet': 'bluewallet',
            'exodus': 'exodus', 'exodus': 'exodus',
            'atomic': 'atomic', 'atomic': 'atomic',
            'guarda': 'guarda', 'guarda': 'guarda',
            'freewallet': 'freewallet', 'freewallet': 'freewallet',
            'coinomi': 'coinomi', 'coinomi': 'coinomi',
            'jaxx': 'jaxx', 'jaxx': 'jaxx',
            'bread': 'bread', 'bread': 'bread',
            'edge': 'edge', 'edge': 'edge',
            'mycelium': 'mycelium', 'mycelium': 'mycelium',
            'bitpay': 'bitpay', 'bitpay': 'bitpay',
            'copay': 'copay', 'copay': 'copay',
            'bitcoin-gold': 'bitcoin-gold', 'btg': 'bitcoin-gold',
            'bitcoin-diamond': 'bitcoin-diamond', 'bcd': 'bitcoin-diamond',
            'bitcoin-private': 'bitcoin-private', 'btcp': 'bitcoin-private',
            'bitcoin-atom': 'bitcoin-atom', 'bca': 'bitcoin-atom',
            'bitcoin-post-quantum': 'bitcoin-post-quantum', 'bpq': 'bitcoin-post-quantum'
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
/price <coin> or /p <coin> - Get current price
/top10 - Show top 10 coins
/top20 - Show top 20 coins
/help - Show this help

**Popular Examples:**
/price bitcoin or /p bitcoin
/price ethereum or /p ethereum
/price solana or /p solana
/price dogecoin or /p dogecoin
/price memecore or /p memecore
/price m or /p m
/price cardano or /p cardano
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

💵 **Current:** ${current_price:,.3f}
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
                results.append(f"{coin_name}: ${current_price:,.3f} {change_emoji} {change_24h:+.2f}%")
        
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
                results.append(f"{coin_name}: ${current_price:,.3f} {change_emoji} {change_24h:+.2f}%")
        
        if results:
            message = "🏆 **Top 20 Cryptocurrencies**\n\n" + "\n".join(results)
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Could not fetch top 20 prices")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Top 100+ Crypto Bot Help**

**Commands:**
/start - Welcome message
/price <coin> or /p <coin> - Get current price
/top10 - Show top 10 coins
/top20 - Show top 20 coins
/help - Show this help

**Major Coins:**
Bitcoin (BTC), Ethereum (ETH), Tether (USDT), BNB, Solana (SOL)
USDC, XRP, Staked ETH, Dogecoin (DOGE), Memecore (M)
Cardano (ADA), Tron (TRX), Avalanche (AVAX), Chainlink (LINK), Polkadot (DOT)
Bitcoin Cash (BCH), Near (NEAR), Polygon (MATIC), Litecoin (LTC)

**Meme Coins:**
Dogecoin (DOGE), Shiba Inu (SHIB), Pepe (PEPE), Floki (FLOKI)
Bonk (BONK), Dogwifhat (WIF), Myro (MYRO), Popcat (POPCAT)
Memecore (M) - BNB Chain Contract: 0x22b1458e780f8fa71e2f84502cee8b5a3cc731fa

**DeFi Tokens:**
Uniswap (UNI), Aave (AAVE), Compound (COMP), Maker (MKR)
Sushi (SUSHI), Yearn Finance (YFI), Synthetix (SNX), Curve (CRV)
1inch (1INCH), Balancer (BAL), PancakeSwap (CAKE), Jupiter (JUP)

**Layer 2 & Scaling:**
Arbitrum (ARB), Optimism (OP), Base (BASE), Polygon (MATIC)
Immutable X (IMX), Loopring (LRC), Metis (METIS), Mantle (MNT)
Blast (BLAST), Mode (MODE), zkSync (ZK), Linea (LINEA)

**AI & Big Data:**
Fetch.ai (FET), SingularityNET (AGIX), Ocean Protocol (OCEAN)
Render (RNDR), Akash Network (AKT), Bittensor (TAO), Worldcoin (WLD)

**Gaming & Metaverse:**
The Sandbox (SAND), Decentraland (MANA), Axie Infinity (AXS)
Gala (GALA), Enjin Coin (ENJ), Illuvium (ILV), STEPN (GMT)

**Popular Examples:**
/price bitcoin
/price ethereum
/price dogecoin
/price memecore
/price m
/price shib
/price pepe
/price bonk
/price arbitrum
/price optimism
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
    application.add_handler(CommandHandler("p", bot.price_command))  # Shortcut for /price
    application.add_handler(CommandHandler("top10", bot.top10_command))
    application.add_handler(CommandHandler("top20", bot.top20_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    logger.info("🚀 Top 100 Crypto Bot started!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
