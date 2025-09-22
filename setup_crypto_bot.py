#!/usr/bin/env python3
"""
Setup script for Crypto Alarm Telegram Bot
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_crypto_bot.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def create_env_file():
    """Create .env file with configuration"""
    env_content = """# Crypto Alarm Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
ROMA_SERVER_URL=http://localhost:5000
DATABASE_PATH=crypto_alerts.db
CHECK_INTERVAL=60
LOG_LEVEL=INFO
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file - Please update with your bot token!")
    else:
        print("ℹ️ .env file already exists")

def setup_database():
    """Initialize the database"""
    print("🗄️ Setting up database...")
    try:
        conn = sqlite3.connect('crypto_alerts.db')
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                target_price REAL NOT NULL,
                alert_type TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                triggered_at TIMESTAMP NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                default_currency TEXT DEFAULT 'usd',
                timezone TEXT DEFAULT 'UTC',
                notification_frequency INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database setup complete!")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_config_file():
    """Create configuration file"""
    config_content = """# Crypto Alarm Bot Configuration
{
    "supported_coins": {
        "bitcoin": "bitcoin",
        "btc": "bitcoin",
        "ethereum": "ethereum", 
        "eth": "ethereum",
        "binancecoin": "binancecoin",
        "bnb": "binancecoin",
        "cardano": "cardano",
        "ada": "cardano",
        "solana": "solana",
        "sol": "solana",
        "polkadot": "polkadot",
        "dot": "polkadot",
        "chainlink": "chainlink",
        "link": "chainlink",
        "litecoin": "litecoin",
        "ltc": "litecoin",
        "bitcoin-cash": "bitcoin-cash",
        "bch": "bitcoin-cash",
        "stellar": "stellar",
        "xlm": "stellar"
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
"""
    
    with open('crypto_bot_config.json', 'w') as f:
        f.write(config_content)
    print("✅ Configuration file created!")

def create_docker_file():
    """Create Dockerfile for deployment"""
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    sqlite3 \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements_crypto_bot.txt .
RUN pip install --no-cache-dir -r requirements_crypto_bot.txt

# Copy application files
COPY crypto_alarm_bot.py .
COPY crypto_bot_config.json .

# Create directory for database
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/app/data/crypto_alerts.db

# Run the bot
CMD ["python", "crypto_alarm_bot.py"]
"""
    
    with open('Dockerfile.crypto-bot', 'w') as f:
        f.write(dockerfile_content)
    print("✅ Dockerfile created!")

def create_docker_compose():
    """Create docker-compose file"""
    compose_content = """version: '3.8'

services:
  crypto-bot:
    build:
      context: .
      dockerfile: Dockerfile.crypto-bot
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - ROMA_SERVER_URL=http://roma-server:5000
      - DATABASE_PATH=/app/data/crypto_alerts.db
    volumes:
      - ./data:/app/data
    depends_on:
      - roma-server
    restart: unless-stopped

  roma-server:
    image: sentient-agi/roma:latest
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./roma-data:/app/data
    restart: unless-stopped
"""
    
    with open('docker-compose.crypto-bot.yml', 'w') as f:
        f.write(compose_content)
    print("✅ Docker Compose file created!")

def main():
    """Main setup function"""
    print("🚀 Setting up Crypto Alarm Telegram Bot...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('crypto_alarm_bot.py'):
        print("❌ Please run this script from the ROMA directory")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create configuration files
    create_env_file()
    create_config_file()
    create_docker_file()
    create_docker_compose()
    
    # Setup database
    if not setup_database():
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Get a Telegram bot token from @BotFather")
    print("2. Update the .env file with your bot token")
    print("3. Make sure ROMA server is running on localhost:5000")
    print("4. Run: python crypto_alarm_bot.py")
    print("\n🐳 For Docker deployment:")
    print("1. Update docker-compose.crypto-bot.yml with your tokens")
    print("2. Run: docker-compose -f docker-compose.crypto-bot.yml up")
    
    return True

if __name__ == "__main__":
    main()
