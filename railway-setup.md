# 🚀 Railway Deployment Guide

## Quick Railway Setup for Crypto Bot

### Step 1: Install Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
# Login to Railway
railway login
```

### Step 3: Initialize Project
```bash
# Initialize Railway project
railway init
```

### Step 4: Set Environment Variables
```bash
# Set your Telegram bot token
railway variables set TELEGRAM_BOT_TOKEN=8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA
```

### Step 5: Deploy Your Bot
```bash
# Deploy to Railway
railway deploy
```

### Step 6: Check Status
```bash
# Check deployment status
railway status

# View logs
railway logs

# Open dashboard
railway dashboard
```

## 🎯 Why Railway is Perfect for Your Bot

### ✅ **Always Free Tier:**
- **No Time Limits** - Runs 24/7 forever
- **No Sleep Mode** - Always responsive
- **Persistent Storage** - Bot data saved
- **Auto-restart** - If bot crashes

### ✅ **Easy Management:**
- **Real-time Logs** - Monitor your bot
- **Environment Variables** - Secure token storage
- **One-click Deploy** - Update with one command
- **Global CDN** - Fast worldwide access

### ✅ **Perfect for Telegram Bots:**
- **Webhook Support** - Real-time updates
- **Background Tasks** - Continuous monitoring
- **Error Handling** - Automatic recovery
- **Scaling** - Handles traffic spikes

## 🔧 Railway Commands

### Basic Commands:
```bash
# Deploy your bot
railway deploy

# Check status
railway status

# View logs
railway logs

# Open dashboard
railway dashboard

# Set variables
railway variables set KEY=value

# List variables
railway variables
```

### Advanced Commands:
```bash
# Connect to service
railway connect

# Run locally
railway run python top100_crypto_bot.py

# Generate domain
railway domain

# Check metrics
railway metrics
```

## 🎉 Your Bot Features on Railway

### ✅ **Crypto Bot Features:**
- **Memecore Support** - `/price m` command
- **Top 100 Coins** - Comprehensive coverage
- **Real-time Prices** - Live market data
- **Group Chat Support** - Works in groups
- **24/7 Uptime** - Never sleeps
- **Global Access** - Worldwide availability

### ✅ **Railway Benefits:**
- **Free Forever** - No time limits
- **Auto-scaling** - Handles traffic
- **SSL Included** - Secure connections
- **Monitoring** - Built-in analytics
- **Backups** - Automatic data protection

## 🚀 Deployment Checklist

- [ ] Railway CLI installed
- [ ] Logged into Railway
- [ ] Project initialized
- [ ] Environment variables set
- [ ] Bot deployed successfully
- [ ] Bot responding to commands
- [ ] Logs monitoring active

## 🎯 Test Your Bot

After deployment, test these commands:
- `/start` - Welcome message
- `/price m` - Memecore price
- `/price bitcoin` - Bitcoin price
- `/top10` - Top 10 coins
- `/help` - Command list

## 🔧 Troubleshooting

### Bot Not Responding:
```bash
# Check logs
railway logs

# Restart service
railway restart

# Check variables
railway variables
```

### Deployment Issues:
```bash
# Check status
railway status

# View build logs
railway logs --build

# Redeploy
railway deploy --detach
```

## 🎉 Success!

Your crypto bot is now running on Railway with:
- ✅ **24/7 Uptime** - Never sleeps
- ✅ **Global Access** - Worldwide availability
- ✅ **Auto-restart** - If crashes
- ✅ **Real-time Logs** - Monitor activity
- ✅ **Free Forever** - No costs

Your bot is live on Railway! 🚀📈
