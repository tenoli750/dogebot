# 🖥️ Google Cloud VM Instance Setup Guide

## Step-by-Step VM Creation

### 1. 🌐 Access Google Cloud Console
- Go to: https://console.cloud.google.com/
- Sign in with your Google account

### 2. 📁 Create a New Project
- Click the project dropdown (top left)
- Click "New Project"
- **Project Name**: `crypto-bot-project`
- **Organization**: (leave default)
- Click "Create"

### 3. 💳 Enable Billing (Required)
- Go to "Billing" in the left menu
- Click "Link a billing account"
- Add a payment method (credit card)
- **Note**: Free tier gives you $300 credit for 12 months

### 4. 🖥️ Create VM Instance

#### Navigate to Compute Engine:
- Go to "Compute Engine" → "VM instances"
- Click "Create Instance"

#### Configure Your VM:
```
Name: crypto-bot-vm
Region: us-central1 (Iowa) - Cheapest option
Zone: us-central1-a

Machine Configuration:
- Machine family: General-purpose
- Series: E2
- Machine type: e2-micro (1 vCPU, 1 GB memory)
  - Cost: $0/month (free tier) or $6.11/month

Boot Disk:
- Operating System: Ubuntu
- Version: Ubuntu 22.04 LTS
- Boot disk type: Standard persistent disk
- Size: 30 GB (default)

Firewall:
- Allow HTTP traffic: ✅
- Allow HTTPS traffic: ✅
```

#### Advanced Options (Optional):
```
- Preemptible: No (for 24/7 operation)
- Access scopes: Allow default access
- Management: 
  - Enable OS Login: ✅
  - Enable serial port access: ✅
```

### 5. 🚀 Create and Connect
- Click "Create" (takes 1-2 minutes)
- Wait for green checkmark ✅
- Click "SSH" button next to your VM

### 6. 🔑 SSH Connection
- Browser-based SSH opens automatically
- You're now connected to your Ubuntu server!

## 📋 Next Steps After VM Creation

### Install Dependencies:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install python3-pip python3-venv git curl wget -y

# Install screen for background processes
sudo apt install screen -y
```

### Upload Your Bot Files:
```bash
# Create project directory
mkdir crypto-bot
cd crypto-bot

# Option 1: Clone from GitHub (if you have a repo)
git clone https://github.com/your-username/crypto-bot.git .

# Option 2: Upload files manually
# Use the file upload feature in the SSH terminal
```

### Set Up Python Environment:
```bash
# Create virtual environment
python3 -m venv crypto_bot_env

# Activate environment
source crypto_bot_env/bin/activate

# Install dependencies
pip install -r requirements_crypto_bot.txt
```

### Configure Your Bot:
```bash
# Create environment file
nano crypto_bot.env

# Add your Telegram bot token:
TELEGRAM_BOT_TOKEN=8013494369:AAEB-S-1e-6PUHSjagbFsUilda9pnuUH3xA
```

### Run Your Bot:
```bash
# Test run
python top100_crypto_bot.py

# Run in background with screen
screen -S crypto-bot
python top100_crypto_bot.py
# Press Ctrl+A, then D to detach

# Reattach later
screen -r crypto-bot
```

## 🔧 VM Management Commands

### Check VM Status:
```bash
# Check if bot is running
ps aux | grep python

# Check system resources
htop
```

### Restart Bot:
```bash
# Kill existing processes
pkill -f "python.*crypto.*bot"

# Start new instance
screen -S crypto-bot
python top100_crypto_bot.py
```

### View Logs:
```bash
# Check bot logs
tail -f /var/log/syslog | grep crypto
```

## 💰 Cost Optimization

### Free Tier (12 months):
- **e2-micro**: $0/month
- **30 GB storage**: $0/month
- **Total**: $0/month

### After Free Tier:
- **e2-micro**: $6.11/month
- **30 GB storage**: $1.20/month
- **Total**: ~$7.31/month

### Cost-Saving Tips:
1. Use **preemptible instances** (60-80% cheaper)
2. **Stop VM** when not needed
3. Use **smaller disk** if possible
4. **Monitor usage** in billing dashboard

## 🛡️ Security Best Practices

### Firewall Rules:
```bash
# Allow only necessary ports
gcloud compute firewall-rules create allow-ssh \
    --allow tcp:22 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow SSH"
```

### SSH Key Setup:
```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# Add to VM
gcloud compute instances add-metadata crypto-bot-vm \
    --metadata-from-file ssh-keys=~/.ssh/id_rsa.pub
```

## 🔄 Backup and Recovery

### Create Snapshot:
```bash
# Create disk snapshot
gcloud compute disks snapshot crypto-bot-vm \
    --snapshot-names crypto-bot-backup-$(date +%Y%m%d)
```

### Restore from Snapshot:
```bash
# Create new VM from snapshot
gcloud compute instances create crypto-bot-vm-restored \
    --source-snapshot=crypto-bot-backup-20241201
```

## 📊 Monitoring

### Set Up Monitoring:
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Check system status
htop          # CPU and memory
iotop         # Disk I/O
nethogs       # Network usage
```

### Google Cloud Monitoring:
- Go to "Monitoring" in Google Cloud Console
- Set up alerts for CPU, memory, disk usage
- Configure uptime checks

## 🚨 Troubleshooting

### Common Issues:

#### Bot Not Responding:
```bash
# Check if bot is running
ps aux | grep python

# Check logs
journalctl -u crypto-bot -f
```

#### High CPU Usage:
```bash
# Check processes
top
htop

# Kill problematic processes
sudo pkill -f "python.*crypto"
```

#### Out of Memory:
```bash
# Check memory usage
free -h

# Restart VM if needed
sudo reboot
```

## ✅ Success Checklist

- [ ] VM instance created
- [ ] SSH connection working
- [ ] Python environment set up
- [ ] Bot files uploaded
- [ ] Bot token configured
- [ ] Bot running in screen session
- [ ] Bot responding to Telegram commands
- [ ] Monitoring set up
- [ ] Backup strategy in place

## 🎉 Your Bot is Now Live!

Your crypto bot is now running 24/7 on Google Cloud with:
- ✅ **Memecore support** (`/price m`)
- ✅ **Top 100 cryptocurrencies**
- ✅ **Real-time price data**
- ✅ **Group chat support**
- ✅ **Global accessibility**

**Test your bot:**
- Send `/start` to your bot
- Try `/price m` for Memecore
- Try `/price bitcoin` for Bitcoin
- Try `/top10` for top 10 coins

Your bot is now running on Google Cloud! 🚀📈
