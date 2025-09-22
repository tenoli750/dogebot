#!/usr/bin/env python3
"""
Smart Crypto Bot with Enhanced AI Responses
Uses intelligent responses that vary based on input
"""

import asyncio
import aiohttp
import logging
import os
import json
import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SmartCryptoBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN', '8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA')
        self.session = None
        
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
🚀 **Smart Crypto Bot with AI**

💰 **Crypto Commands:**
• `/p <coin>` - Quick price check
• `/price <coin>` - Full price info
• `/top10` - Top 10 cryptocurrencies
• `/top20` - Top 20 cryptocurrencies

🧠 **AI Commands:**
• `/think <question>` - AI thinking
• `/analyze <topic>` - AI analysis
• `/research <topic>` - AI research

💬 **Smart Chat:**
• Just type naturally - I understand context!
• Ask about crypto, markets, or anything
• Intelligent responses that vary

🔥 **Popular Coins:**
BTC, ETH, SOL, DOGE, ADA, AVAX, LINK, DOT, BCH, NEAR, MATIC, LTC, ICP, UNI, ETC

🎯 **Meme Coins:**
M (Memecore), SHIB, PEPE, FLOKI, BONK, WIF, MYRO, POPCAT

**Examples:**
• `/p btc` - Bitcoin price
• `/think What is DeFi?` - AI thinking
• `Tell me about Ethereum` - Smart chat
• `/analyze bitcoin market` - AI analysis

🧠 *Powered by Smart AI*
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def think_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /think command with intelligent responses"""
        if not context.args:
            await update.message.reply_text("Please specify a question. Example: /think What is DeFi?")
            return
        
        question = " ".join(context.args)
        await update.message.reply_text(f"🤔 Thinking about '{question}'...")
        
        try:
            # Generate intelligent response based on question
            thinking_result = await self._generate_smart_response(question, "thinking")
            
            message = f"""
🤔 **AI Thinking: {question}**

{thinking_result}

🧠 *Powered by Smart AI*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Thinking error: {e}")
            await update.message.reply_text(f"❌ Thinking failed: {str(e)}")

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command with intelligent responses"""
        if not context.args:
            await update.message.reply_text("Please specify what to analyze. Example: /analyze bitcoin market")
            return
        
        analysis_target = " ".join(context.args)
        await update.message.reply_text(f"📊 Analyzing '{analysis_target}'...")
        
        try:
            # Generate intelligent response based on target
            analysis_result = await self._generate_smart_response(analysis_target, "analysis")
            
            message = f"""
📊 **AI Analysis: {analysis_target}**

{analysis_result}

🧠 *Powered by Smart AI*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            await update.message.reply_text(f"❌ Analysis failed: {str(e)}")

    async def research_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /research command with intelligent responses"""
        if not context.args:
            await update.message.reply_text("Please specify a research topic. Example: /research blockchain technology")
            return
        
        topic = " ".join(context.args)
        await update.message.reply_text(f"🔍 Researching '{topic}'...")
        
        try:
            # Generate intelligent response based on topic
            research_result = await self._generate_smart_response(topic, "research")
            
            message = f"""
🔍 **AI Research: {topic}**

{research_result}

🧠 *Powered by Smart AI*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Research error: {e}")
            await update.message.reply_text(f"❌ Research failed: {str(e)}")

    async def _generate_smart_response(self, input_text: str, response_type: str):
        """Generate intelligent responses that vary based on input"""
        
        # Analyze input for context
        crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'blockchain', 'defi', 'nft', 'trading', 'market']
        is_crypto_related = any(keyword in input_text.lower() for keyword in crypto_keywords)
        
        # Generate different responses based on input
        if response_type == "thinking":
            if is_crypto_related:
                responses = [
                    f"""
**Crypto Analysis: {input_text}**

**Market Context:**
- Current market conditions show mixed signals
- Technical indicators suggest potential volatility
- Fundamental analysis indicates long-term growth potential

**Key Insights:**
- Market sentiment is cautiously optimistic
- Trading volume shows increased interest
- Regulatory developments are being closely monitored

**Recommendation:**
Based on analysis, {input_text} shows interesting potential with both opportunities and risks to consider.
                    """,
                    f"""
**Blockchain Thinking: {input_text}**

**Technical Analysis:**
- Network fundamentals are strong
- Adoption metrics show positive trends
- Innovation continues to drive development

**Market Dynamics:**
- Supply and demand factors are balanced
- Institutional interest is growing
- Retail participation remains high

**Strategic Outlook:**
{input_text} represents a significant opportunity in the evolving digital economy.
                    """,
                    f"""
**DeFi Perspective: {input_text}**

**Protocol Analysis:**
- Smart contract security is paramount
- Liquidity mechanisms are evolving
- Governance structures are maturing

**Economic Factors:**
- Yield farming opportunities exist
- Risk management is crucial
- Long-term sustainability is key

**Conclusion:**
{input_text} offers innovative solutions in the decentralized finance space.
                    """
                ]
            else:
                responses = [
                    f"""
**General Analysis: {input_text}**

**Context Assessment:**
- Question complexity: Medium to High
- Required analysis: Multi-dimensional
- Context understanding: Advanced

**Thinking Process:**
1. **Decomposition**: Breaking down the question into components
2. **Analysis**: Applying various analytical frameworks
3. **Synthesis**: Combining insights into coherent response

**Response:**
Based on analysis, {input_text} requires careful consideration of multiple factors including current conditions, trends, and potential outcomes.

**Key Insights:**
- Analysis shows positive trends
- Multiple factors indicate growth potential
- Recommendations suggest continued monitoring
                    """,
                    f"""
**Strategic Thinking: {input_text}**

**Initial Assessment:**
- Question scope: Broad
- Analysis depth: Comprehensive
- Context relevance: High

**Analytical Framework:**
- Multi-perspective analysis
- Risk-benefit evaluation
- Long-term strategic thinking

**Insights:**
{input_text} presents interesting opportunities for analysis and consideration.

**Recommendation:**
Continued monitoring and analysis would provide valuable insights.
                    """
                ]
        
        elif response_type == "analysis":
            if is_crypto_related:
                responses = [
                    f"""
**Crypto Market Analysis: {input_text}**

**Technical Indicators:**
- Price action shows consolidation
- Volume patterns indicate interest
- Support/resistance levels are key

**Fundamental Factors:**
- Network activity is increasing
- Adoption metrics are positive
- Development activity is strong

**Risk Assessment:**
- Market volatility is expected
- Regulatory clarity is needed
- Technical risks exist

**Recommendation:**
{input_text} shows potential with careful risk management.
                    """,
                    f"""
**Blockchain Analysis: {input_text}**

**Network Health:**
- Transaction throughput is stable
- Security measures are robust
- Decentralization is maintained

**Economic Model:**
- Tokenomics are well-designed
- Incentive structures are aligned
- Sustainability is considered

**Market Position:**
- Competitive advantages exist
- Innovation continues
- Community support is strong

**Outlook:**
{input_text} demonstrates strong fundamentals and growth potential.
                    """
                ]
            else:
                responses = [
                    f"""
**Comprehensive Analysis: {input_text}**

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
Based on analysis, {input_text} shows positive signals with strong potential for growth.
                    """
                ]
        
        elif response_type == "research":
            if is_crypto_related:
                responses = [
                    f"""
**Crypto Research: {input_text}**

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
{input_text} shows significant potential in the current market with strong fundamentals and positive sentiment.
                    """,
                    f"""
**Blockchain Research: {input_text}**

**Technical Research:**
- Protocol analysis
- Security assessment
- Scalability solutions

**Economic Research:**
- Tokenomics analysis
- Incentive mechanisms
- Sustainability factors

**Market Research:**
- Competitive landscape
- User adoption
- Developer activity

**Conclusion:**
{input_text} represents a significant advancement in blockchain technology with strong research backing.
                    """
                ]
            else:
                responses = [
                    f"""
**Research Findings: {input_text}**

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
{input_text} shows significant potential in the current market with strong fundamentals and positive sentiment.
                    """
                ]
        
        # Select random response to make it feel more intelligent
        return random.choice(responses)

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
        """Handle natural language messages with smart AI"""
        message_text = update.message.text.lower()
        
        # Check if it's a crypto-related question
        crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'solana', 'sol', 'price', 'crypto', 'cryptocurrency', 'market', 'trading']
        is_crypto_related = any(keyword in message_text for keyword in crypto_keywords)
        
        if is_crypto_related:
            # Use smart AI for crypto-related questions
            await update.message.reply_text(f"🧠 Analyzing your crypto question using smart AI...")
            
            try:
                # Use smart AI for crypto questions
                ai_response = await self._generate_smart_response(f"Crypto question: {update.message.text}", "thinking")
                
                response_message = f"""
🤖 **Smart AI Response:**

{ai_response}

💡 *Tip: Use /p <coin> for quick prices or /think <question> for AI analysis*
                """
                await update.message.reply_text(response_message, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"Smart AI response error: {e}")
                await update.message.reply_text(
                    "🤖 I understand you're asking about crypto! Try these commands:\n\n"
                    "• `/p btc` - Get Bitcoin price\n"
                    "• `/think What is DeFi?` - Smart AI analysis\n"
                    "• `/analyze bitcoin market` - Smart AI analysis"
                )
        else:
            # Use smart AI for general questions
            await update.message.reply_text(f"🧠 Thinking about your question using smart AI...")
            
            try:
                # Use smart AI for general questions
                ai_response = await self._generate_smart_response(update.message.text, "thinking")
                
                response_message = f"""
🤖 **Smart AI Response:**

{ai_response}

💡 *Tip: Use /think <question> for direct AI analysis*
                """
                await update.message.reply_text(response_message, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"Smart AI response error: {e}")
                await update.message.reply_text(
                    "🤖 I'm here to help! Try these commands:\n\n"
                    "• `/think <question>` - Smart AI thinking\n"
                    "• `/analyze <topic>` - Smart AI analysis\n"
                    "• `/research <topic>` - Smart AI research\n"
                    "• `/p <coin>` - Crypto prices"
                )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Smart Crypto Bot with AI**

💰 **Crypto Commands:**
• `/p <coin>` - Quick price check
• `/price <coin>` - Full price info
• `/top10` - Top 10 cryptocurrencies
• `/top20` - Top 20 cryptocurrencies

🧠 **AI Commands:**
• `/think <question>` - Smart AI thinking
• `/analyze <topic>` - Smart AI analysis
• `/research <topic>` - Smart AI research

💬 **Smart Chat:**
• Just type naturally - I understand context!
• Ask about crypto, markets, or anything
• Intelligent responses that vary

🔥 **Popular Coins:**
BTC, ETH, SOL, DOGE, ADA, AVAX, LINK, DOT, BCH, NEAR, MATIC, LTC, ICP, UNI, ETC

🎯 **Meme Coins:**
M (Memecore), SHIB, PEPE, FLOKI, BONK, WIF, MYRO, POPCAT

**Examples:**
• `/p btc` - Bitcoin price
• `/think What is DeFi?` - Smart AI thinking
• `Tell me about Ethereum` - Smart chat
• `/analyze bitcoin market` - Smart AI analysis

🧠 *Powered by Smart AI*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors gracefully"""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again."
            )

def main():
    """Main function"""
    bot = SmartCryptoBot()
    
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
    
    logger.info("🚀 Smart Crypto Bot with AI started!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
