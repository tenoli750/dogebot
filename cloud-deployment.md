# 🚀 Crypto Bot Cloud Deployment Guide

## Quick Start Options

### 1. DigitalOcean Droplet (Recommended)
```bash
# Create a $6/month droplet
# Ubuntu 22.04 LTS
# 1GB RAM, 1 CPU, 25GB SSD

# SSH into your server
ssh root@your-server-ip

# Create user
adduser ubuntu
usermod -aG sudo ubuntu
su - ubuntu

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv git

# Clone and setup
git clone <your-repo> crypto-bot
cd crypto-bot
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate
pip install -r requirements_crypto_bot.txt

# Run deployment script
./deploy.sh
```

### 2. AWS EC2 Instance
```bash
# Launch t2.micro (free tier eligible)
# Ubuntu 22.04 LTS
# Security group: Allow SSH (port 22)

# Same setup as DigitalOcean
```

### 3. Google Cloud Platform
```bash
# Create VM instance
# e2-micro (free tier eligible)
# Ubuntu 22.04 LTS

# Same setup as above
```

### 4. VPS Providers
- **Vultr**: $3.50/month
- **Linode**: $5/month  
- **Hetzner**: €3.29/month
- **Contabo**: $4.99/month

## Docker Deployment (Any Platform)

### Option A: Docker Compose
```bash
# On your server
git clone <your-repo> crypto-bot
cd crypto-bot

# Set environment variable
export TELEGRAM_BOT_TOKEN="your-bot-token"

# Start with Docker Compose
docker-compose up -d
```

### Option B: Docker Run
```bash
# Build image
docker build -t crypto-bot .

# Run container
docker run -d \
  --name crypto-bot \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="your-bot-token" \
  crypto-bot
```

## Systemd Service (Linux Servers)

### Install as Service
```bash
# Copy service file
sudo cp crypto-bot.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable crypto-bot
sudo systemctl start crypto-bot

# Check status
sudo systemctl status crypto-bot
```

### Service Management
```bash
# Start service
sudo systemctl start crypto-bot

# Stop service  
sudo systemctl stop crypto-bot

# Restart service
sudo systemctl restart crypto-bot

# View logs
sudo journalctl -u crypto-bot -f

# Check status
sudo systemctl status crypto-bot
```

## Monitoring & Maintenance

### Health Checks
```bash
# Check if bot is running
ps aux | grep "top100_crypto_bot.py"

# Check systemd service
sudo systemctl status crypto-bot

# Check Docker container
docker ps | grep crypto-bot
```

### Log Monitoring
```bash
# Systemd logs
sudo journalctl -u crypto-bot -f

# Docker logs
docker logs -f crypto-bot

# Application logs
tail -f bot.log
```

### Auto-restart Setup
```bash
# Add to crontab (check every 5 minutes)
crontab -e
# Add this line:
*/5 * * * * /path/to/monitor_bot.sh
```

## Cost Comparison

| Provider | Plan | Monthly Cost | RAM | Storage |
|----------|------|--------------|-----|---------|
| DigitalOcean | Basic | $6 | 1GB | 25GB |
| AWS EC2 | t2.micro | Free* | 1GB | 30GB |
| Google Cloud | e2-micro | Free* | 1GB | 30GB |
| Vultr | Regular | $3.50 | 1GB | 25GB |
| Linode | Nanode | $5 | 1GB | 25GB |

*Free tier eligible (12 months)

## Security Best Practices

### 1. Firewall Setup
```bash
# Ubuntu/Debian
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow out 443  # HTTPS for API calls
```

### 2. Environment Variables
```bash
# Don't hardcode tokens
export TELEGRAM_BOT_TOKEN="your-token"
```

### 3. Regular Updates
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Update bot
git pull origin main
sudo systemctl restart crypto-bot
```

## Troubleshooting

### Bot Not Responding
```bash
# Check if running
ps aux | grep python

# Check logs
sudo journalctl -u crypto-bot -n 50

# Restart service
sudo systemctl restart crypto-bot
```

### High Memory Usage
```bash
# Monitor resources
htop

# Restart if needed
sudo systemctl restart crypto-bot
```

### Network Issues
```bash
# Test API connectivity
curl https://api.coingecko.com/api/v3/ping

# Check Telegram API
curl https://api.telegram.org/bot<TOKEN>/getMe
```

## Backup Strategy

### 1. Code Backup
```bash
# Git repository
git add .
git commit -m "Backup $(date)"
git push origin main
```

### 2. Configuration Backup
```bash
# Backup environment file
cp crypto_bot.env crypto_bot.env.backup
```

### 3. Database Backup (if using SQLite)
```bash
# Backup database
cp crypto_bot.db crypto_bot.db.backup
```

## Scaling Options

### 1. Load Balancing
- Use multiple bot instances
- Distribute across regions
- Use message queues

### 2. Database Scaling
- Move from SQLite to PostgreSQL
- Add Redis for caching
- Implement connection pooling

### 3. Monitoring
- Add Prometheus metrics
- Use Grafana dashboards
- Set up alerting

## Quick Commands Reference

```bash
# Deploy bot
./deploy.sh

# Check status
sudo systemctl status crypto-bot

# View logs
sudo journalctl -u crypto-bot -f

# Restart bot
sudo systemctl restart crypto-bot

# Update bot
git pull && sudo systemctl restart crypto-bot
```

Your crypto bot is now ready for production deployment! 🚀📈
