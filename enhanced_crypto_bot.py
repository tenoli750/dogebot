#!/usr/bin/env python3
"""
Enhanced Crypto Bot with ROMA AI Integration
Combines crypto price functionality with intelligent AI chat capabilities
"""

import asyncio
import aiohttp
import logging
import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class EnhancedCryptoBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.session = None
        self.roma_client = None
        
        # Initialize ROMA client
        self.setup_roma_client()
        
        # Supported coins with aliases
        self.supported_coins = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'solana': 'solana', 'sol': 'solana',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'cardano': 'cardano', 'ada': 'cardano',
            'avalanche-2': 'avalanche-2', 'avax': 'avalanche-2',
            'chainlink': 'chainlink', 'link': 'chainlink',
            'polkadot': 'polkadot', 'dot': 'polkadot',
            'bitcoin-cash': 'bitcoin-cash', 'bch': 'bitcoin-cash',
            'near': 'near', 'near': 'near',
            'polygon': 'matic-network', 'matic': 'matic-network',
            'litecoin': 'litecoin', 'ltc': 'litecoin',
            'internet-computer': 'internet-computer', 'icp': 'internet-computer',
            'uniswap': 'uniswap', 'uni': 'uniswap',
            'ethereum-classic': 'ethereum-classic', 'etc': 'ethereum-classic',
            'memecore': 'memecore', 'm': 'memecore',
            'shiba-inu': 'shiba-inu', 'shib': 'shiba-inu',
            'pepe': 'pepe', 'pepe': 'pepe',
            'floki': 'floki', 'floki': 'floki',
            'bonk': 'bonk', 'bonk': 'bonk',
            'dogwifhat': 'dogwifhat', 'wif': 'dogwifhat',
            'myro': 'myro', 'myro': 'myro',
            'popcat': 'popcat', 'popcat': 'popcat'
        }

    def setup_roma_client(self):
        """Setup ROMA client connection"""
        # This would connect to your ROMA server
        # For now, we'll simulate the connection
        self.roma_client = ROMAClient()

    async def start_session(self):
        """Start aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🚀 **Enhanced Crypto Bot with AI**

💰 **Crypto Commands:**
• `/p <coin>` - Quick price check
• `/price <coin>` - Full price info
• `/top10` - Top 10 cryptocurrencies
• `/top20` - Top 20 cryptocurrencies

🧠 **AI Commands:**
• `/think <question>` - AI thinking
• `/analyze <topic>` - AI analysis
• `/research <topic>` - AI research

💬 **Chat Features:**
• Just type naturally - I understand context!
• Ask about crypto, markets, or anything
• I remember our conversation

🔥 **Popular Coins:**
BTC, ETH, SOL, DOGE, ADA, AVAX, LINK, DOT, BCH, NEAR, MATIC, LTC, ICP, UNI, ETC

🎯 **Meme Coins:**
M (Memecore), SHIB, PEPE, FLOKI, BONK, WIF, MYRO, POPCAT

**Examples:**
• `/p btc` - Bitcoin price
• `/think What is DeFi?` - AI thinking
• `Tell me about Ethereum` - Natural chat
• `Analyze the crypto market` - AI analysis
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def think_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /think command using ROMA"""
        if not context.args:
            await update.message.reply_text("Please specify a question. Example: /think What is DeFi?")
            return
        
        question = " ".join(context.args)
        await update.message.reply_text(f"🤔 Thinking about '{question}' using ROMA AI...")
        
        try:
            # Use ROMA's thinking capabilities
            thinking_result = await self.roma_client.execute_thinking(question)
            
            message = f"""
🤔 **ROMA AI Thinking: {question}**

{thinking_result}

🧠 *Powered by ROMA AI*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Thinking error: {e}")
            await update.message.reply_text(f"❌ Thinking failed: {str(e)}")

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command using ROMA"""
        if not context.args:
            await update.message.reply_text("Please specify what to analyze. Example: /analyze bitcoin market")
            return
        
        analysis_target = " ".join(context.args)
        await update.message.reply_text(f"📊 Analyzing '{analysis_target}' using ROMA AI...")
        
        try:
            # Use ROMA's analysis capabilities
            analysis_result = await self.roma_client.execute_analysis(analysis_target)
            
            message = f"""
📊 **ROMA AI Analysis: {analysis_target}**

{analysis_result}

🧠 *Powered by ROMA AI*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            await update.message.reply_text(f"❌ Analysis failed: {str(e)}")

    async def research_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /research command using ROMA"""
        if not context.args:
            await update.message.reply_text("Please specify a research topic. Example: /research blockchain technology")
            return
        
        topic = " ".join(context.args)
        await update.message.reply_text(f"🔍 Researching '{topic}' using ROMA AI...")
        
        try:
            # Use ROMA's research capabilities
            research_result = await self.roma_client.execute_research(topic)
            
            message = f"""
🔍 **ROMA AI Research: {topic}**

{research_result}

🧠 *Powered by ROMA AI*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Research error: {e}")
            await update.message.reply_text(f"❌ Research failed: {str(e)}")

    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /price and /p commands"""
        if not context.args:
            await update.message.reply_text("Please specify a coin. Example: /p bitcoin")
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

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural language messages with AI"""
        message_text = update.message.text.lower()
        
        # Check if it's a crypto-related question
        crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'solana', 'sol', 'price', 'crypto', 'cryptocurrency', 'market', 'trading']
        is_crypto_related = any(keyword in message_text for keyword in crypto_keywords)
        
        if is_crypto_related:
            # Use ROMA AI for crypto-related questions
            await update.message.reply_text(f"🧠 Analyzing your crypto question using ROMA AI...")
            
            try:
                # Use ROMA's thinking capabilities for crypto questions
                ai_response = await self.roma_client.execute_thinking(f"Crypto question: {update.message.text}")
                
                response_message = f"""
🤖 **ROMA AI Response:**

{ai_response}

💡 *Tip: Use /p <coin> for quick prices or /think <question> for AI analysis*
                """
                await update.message.reply_text(response_message, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"AI response error: {e}")
                await update.message.reply_text(
                    "🤖 I understand you're asking about crypto! Try these commands:\n\n"
                    "• `/p btc` - Get Bitcoin price\n"
                    "• `/think What is DeFi?` - AI analysis\n"
                    "• `/analyze bitcoin market` - Market analysis"
                )
        else:
            # Use ROMA AI for general questions
            await update.message.reply_text(f"🧠 Thinking about your question using ROMA AI...")
            
            try:
                # Use ROMA's thinking capabilities for general questions
                ai_response = await self.roma_client.execute_thinking(update.message.text)
                
                response_message = f"""
🤖 **ROMA AI Response:**

{ai_response}

💡 *Tip: Use /think <question> for direct AI analysis*
                """
                await update.message.reply_text(response_message, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"AI response error: {e}")
                await update.message.reply_text(
                    "🤖 I'm here to help! Try these commands:\n\n"
                    "• `/think <question>` - AI thinking\n"
                    "• `/analyze <topic>` - AI analysis\n"
                    "• `/research <topic>` - AI research\n"
                    "• `/p <coin>` - Crypto prices"
                )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Enhanced Crypto Bot with AI**

💰 **Crypto Commands:**
• `/p <coin>` - Quick price check
• `/price <coin>` - Full price info
• `/top10` - Top 10 cryptocurrencies
• `/top20` - Top 20 cryptocurrencies

🧠 **AI Commands:**
• `/think <question>` - AI thinking
• `/analyze <topic>` - AI analysis
• `/research <topic>` - AI research

💬 **Natural Chat:**
• Just type naturally - I understand context!
• Ask about crypto, markets, or anything
• I remember our conversation

🔥 **Popular Coins:**
BTC, ETH, SOL, DOGE, ADA, AVAX, LINK, DOT, BCH, NEAR, MATIC, LTC, ICP, UNI, ETC

🎯 **Meme Coins:**
M (Memecore), SHIB, PEPE, FLOKI, BONK, WIF, MYRO, POPCAT

**Examples:**
• `/p btc` - Bitcoin price
• `/think What is DeFi?` - AI thinking
• `Tell me about Ethereum` - Natural chat
• `Analyze the crypto market` - AI analysis

🧠 *Powered by ROMA AI Framework*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors gracefully"""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again."
            )

class ROMAClient:
    """ROMA client for AI capabilities"""
    
    async def execute_thinking(self, question: str):
        """Execute thinking using ROMA"""
        # This would connect to your ROMA server
        # For now, return a simulated response
        return f"""
**ROMA AI Thinking: {question}**

Based on ROMA's hierarchical thinking capabilities:

**Initial Analysis:**
- Question complexity: Medium
- Required analysis: Multi-dimensional
- Context understanding: High

**Thinking Process:**
1. **Decomposition**: Breaking down the question into components
2. **Analysis**: Applying various analytical frameworks
3. **Synthesis**: Combining insights into coherent response

**Response:**
Based on ROMA's thinking capabilities, {question} requires careful consideration of multiple factors including market conditions, technical analysis, and fundamental research.

**Key Insights:**
- Market sentiment analysis shows positive trends
- Technical indicators suggest continued growth
- Fundamental analysis indicates strong potential

*This is a simulated response. Connect to your ROMA server for real AI thinking.*
        """
    
    async def execute_analysis(self, target: str):
        """Execute analysis using ROMA"""
        return f"""
**ROMA AI Analysis: {target}**

ROMA's analysis framework provides:

**Market Analysis:**
- Current trends: Bullish
- Risk assessment: Medium
- Opportunity score: 8/10

**Technical Analysis:**
- Support levels: Strong
- Resistance levels: Moderate
- Momentum: Positive

**Fundamental Analysis:**
- Market cap: Growing
- Adoption: Increasing
- Technology: Advancing

**Recommendation:**
Based on ROMA's analysis, {target} shows positive signals with strong potential for growth.

*This is a simulated response. Connect to your ROMA server for real analysis.*
        """
    
    async def execute_research(self, topic: str):
        """Execute research using ROMA"""
        return f"""
**ROMA AI Research: {topic}**

Based on ROMA's hierarchical research capabilities:

**Primary Research:**
- Market data analysis
- Technical indicators review
- Fundamental factors assessment

**Secondary Research:**
- News sentiment analysis
- Social media trends
- Expert opinions

**Key Findings:**
- Market sentiment is positive
- Technical indicators are strong
- Fundamental analysis shows promise
- Adoption is increasing

**Research Summary:**
{topic} shows significant potential in the current market with strong fundamentals and positive sentiment.

*This is a simulated response. Connect to your ROMA server for real research.*
        """

def main():
    """Main function"""
    bot = EnhancedCryptoBot()
    
    if not bot.token:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return
    
    # Create application
    application = Application.builder().token(bot.token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("price", bot.price_command))
    application.add_handler(CommandHandler("p", bot.price_command))  # Shortcut
    application.add_handler(CommandHandler("top10", bot.top10_command))
    application.add_handler(CommandHandler("top20", bot.top20_command))
    application.add_handler(CommandHandler("think", bot.think_command))
    application.add_handler(CommandHandler("analyze", bot.analyze_command))
    application.add_handler(CommandHandler("research", bot.research_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    logger.info("🚀 Enhanced Crypto Bot with AI started!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
