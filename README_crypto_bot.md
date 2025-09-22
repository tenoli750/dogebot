# 🚀 Crypto Price Alarm Telegram Bot with ROMA Integration

A powerful Telegram bot that provides real-time cryptocurrency price monitoring, alerts, and market analysis using the ROMA hierarchical AI framework.

## ✨ Features

- 🔔 **Price Alerts**: Set custom price alerts for any supported cryptocurrency
- 📊 **Real-time Prices**: Get current prices with 24h change and volume data
- 🤖 **AI Market Analysis**: Leverage ROMA framework for intelligent market analysis
- 📱 **User-friendly Interface**: Simple commands and intuitive navigation
- 💾 **Persistent Storage**: SQLite database for storing user alerts and preferences
- 🔄 **Background Monitoring**: Automatic price checking and alert notifications
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │────│   ROMA Server   │────│  Market APIs   │
│                 │    │                 │    │  (CoinGecko)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
    ┌─────────┐              ┌─────────┐
    │ SQLite  │              │   AI    │
    │Database │              │Analysis │
    └─────────┘              └─────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- ROMA framework running on localhost:5000
- Telegram Bot Token (from @BotFather)

### Installation

1. **Clone and setup ROMA**:
   ```bash
   git clone https://github.com/sentient-agi/ROMA.git
   cd ROMA
   ./setup.sh  # Choose Docker or Native setup
   ```

2. **Setup the crypto bot**:
   ```bash
   python setup_crypto_bot.py
   ```

3. **Configure your bot**:
   - Get a bot token from [@BotFather](https://t.me/botfather)
   - Update `.env` file with your token:
     ```bash
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     ```

4. **Start ROMA server**:
   ```bash
   python -m src.sentientresearchagent.server.main --port 5000
   ```

5. **Run the crypto bot**:
   ```bash
   python crypto_alarm_bot.py
   ```

## 🤖 Bot Commands

### Basic Commands
- `/start` - Welcome message and help
- `/help` - Show all available commands
- `/price <coin>` - Get current price for a cryptocurrency

### Alert Management
- `/setalert <coin> <price> <above/below>` - Set a price alert
- `/myalerts` - View all your active alerts
- `/removealert <coin> <price>` - Remove a specific alert

### Advanced Features
- `/analysis <coin>` - Get AI-powered market analysis using ROMA
- `/portfolio` - Track your cryptocurrency portfolio (coming soon)

### Examples
```
/price bitcoin
/setalert ethereum 3000 above
/setalert bitcoin 45000 below
/analysis solana
/myalerts
```

## 🪙 Supported Cryptocurrencies

- **Bitcoin** (BTC)
- **Ethereum** (ETH)
- **Binance Coin** (BNB)
- **Cardano** (ADA)
- **Solana** (SOL)
- **Polkadot** (DOT)
- **Chainlink** (LINK)
- **Litecoin** (LTC)
- **Bitcoin Cash** (BCH)
- **Stellar** (XLM)

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ROMA_SERVER_URL=http://localhost:5000

# Optional
DATABASE_PATH=crypto_alerts.db
CHECK_INTERVAL=60
LOG_LEVEL=INFO
```

### Bot Settings

The bot can be configured through `crypto_bot_config.json`:

```json
{
    "supported_coins": {
        "bitcoin": "bitcoin",
        "btc": "bitcoin"
    },
    "api_settings": {
        "coingecko_api": "https://api.coingecko.com/api/v3/simple/price",
        "request_timeout": 10,
        "rate_limit_delay": 1
    },
    "alert_settings": {
        "check_interval": 60,
        "max_alerts_per_user": 20,
        "price_precision": 2
    }
}
```

## 🐳 Docker Deployment

### Using Docker Compose

1. **Update environment variables** in `docker-compose.crypto-bot.yml`
2. **Run the stack**:
   ```bash
   docker-compose -f docker-compose.crypto-bot.yml up -d
   ```

### Manual Docker Build

```bash
# Build the bot image
docker build -f Dockerfile.crypto-bot -t crypto-alarm-bot .

# Run the bot
docker run -d \
  --name crypto-bot \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e ROMA_SERVER_URL=http://roma-server:5000 \
  -v $(pwd)/data:/app/data \
  crypto-alarm-bot
```

## 📊 Database Schema

### Price Alerts Table
```sql
CREATE TABLE price_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    target_price REAL NOT NULL,
    alert_type TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    triggered_at TIMESTAMP NULL
);
```

### User Preferences Table
```sql
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    default_currency TEXT DEFAULT 'usd',
    timezone TEXT DEFAULT 'UTC',
    notification_frequency INTEGER DEFAULT 1
);
```

## 🔄 How It Works

1. **Price Monitoring**: The bot checks cryptocurrency prices every minute using the CoinGecko API
2. **Alert Processing**: Compares current prices with user-set alerts
3. **AI Analysis**: Uses ROMA framework for intelligent market analysis
4. **Notification**: Sends alerts to users when price conditions are met
5. **Data Persistence**: Stores all alerts and user preferences in SQLite database

## 🛠️ Development

### Project Structure
```
ROMA/
├── crypto_alarm_bot.py          # Main bot implementation
├── setup_crypto_bot.py          # Setup script
├── requirements_crypto_bot.txt  # Python dependencies
├── crypto_bot_config.json       # Bot configuration
├── Dockerfile.crypto-bot        # Docker configuration
├── docker-compose.crypto-bot.yml # Docker Compose
└── crypto_alerts.db            # SQLite database (created at runtime)
```

### Adding New Features

1. **New Commands**: Add handlers in the main bot class
2. **New Cryptocurrencies**: Update the `supported_coins` dictionary
3. **New APIs**: Extend the `get_crypto_price` method
4. **New Analysis**: Integrate with ROMA's analysis endpoints

### Testing

```bash
# Run the bot in development mode
python crypto_alarm_bot.py

# Test specific functions
python -c "
from crypto_alarm_bot import CryptoAlarmBot
bot = CryptoAlarmBot('test_token')
print('Bot initialized successfully')
"
```

## 📈 ROMA Integration

The bot leverages ROMA's hierarchical AI framework for:

- **Market Analysis**: Intelligent analysis of market conditions
- **Trend Prediction**: AI-powered price trend analysis
- **Sentiment Analysis**: Market sentiment evaluation
- **Risk Assessment**: Portfolio risk analysis

### ROMA Endpoints Used

- `POST /api/simple/analysis` - Market analysis
- `POST /api/simple/execute` - Custom AI tasks
- WebSocket streaming for real-time updates

## 🚨 Troubleshooting

### Common Issues

1. **Bot not responding**:
   - Check if ROMA server is running on port 5000
   - Verify bot token is correct
   - Check internet connection

2. **Price data not updating**:
   - CoinGecko API rate limits
   - Check API endpoint availability
   - Verify coin symbols are correct

3. **Database errors**:
   - Check file permissions
   - Ensure SQLite is installed
   - Verify database path is writable

### Logs

Check the console output for detailed logs:
```bash
python crypto_alarm_bot.py 2>&1 | tee bot.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ROMA Framework](https://github.com/sentient-agi/ROMA) for AI capabilities
- [CoinGecko API](https://www.coingecko.com/en/api) for price data
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for Telegram integration

## 📞 Support

- Create an issue on GitHub
- Join the [ROMA Discord](https://discord.gg/sentientfoundation)
- Check the [documentation](docs/)

---

**Happy Trading! 🚀📈**
