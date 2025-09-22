# 🚀 Google Cloud Platform Deployment Guide

## Step-by-Step Google Cloud Deployment

### Prerequisites
- Google Cloud account (free tier available)
- $300 free credits for new users
- Credit card for verification (no charges for free tier)

---

## Method 1: Compute Engine VM (Recommended)

### Step 1: Create VM Instance

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Create new project or select existing one

2. **Navigate to Compute Engine**
   - Go to "Compute Engine" → "VM instances"
   - Click "Create Instance"

3. **Configure VM Settings**
   ```
   Name: crypto-bot-vm
   Region: us-central1 (Iowa) - cheapest
   Zone: us-central1-a
   
   Machine Type: e2-micro (Free tier eligible)
   - 1 vCPU, 1 GB RAM
   - $0/month (free tier)
   
   Boot Disk: Ubuntu 22.04 LTS
   - 30 GB standard persistent disk
   - $1.50/month
   
   Firewall: Allow HTTP and HTTPS traffic
   ```

4. **Click "Create"** (takes 2-3 minutes)

### Step 2: Connect to VM

```bash
# Option A: SSH from browser (easiest)
# Click "SSH" button next to your VM instance

# Option B: SSH from terminal
gcloud compute ssh crypto-bot-vm --zone=us-central1-a
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv git curl -y

# Install Docker (optional, for containerized deployment)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Step 4: Deploy Your Bot

```bash
# Create project directory
mkdir crypto-bot && cd crypto-bot

# Upload your bot files (choose one method):

# Method A: Git clone (if you have a repository)
git clone <your-repo-url> .

# Method B: Upload files manually
# Use the file upload feature in Google Cloud Console
# Or use gcloud scp command

# Method C: Create files directly
nano top100_crypto_bot.py
# Copy and paste your bot code
```

### Step 5: Setup Environment

```bash
# Create virtual environment
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate

# Install dependencies
pip install -r requirements_crypto_bot.txt

# Create environment file
nano crypto_bot.env
# Add: TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Step 6: Deploy with Systemd

```bash
# Copy service file
sudo cp crypto-bot.service /etc/systemd/system/

# Update service file for your user
sudo nano /etc/systemd/system/crypto-bot.service
# Change User=ubuntu to your actual username
# Change WorkingDirectory to your actual path

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable crypto-bot
sudo systemctl start crypto-bot

# Check status
sudo systemctl status crypto-bot
```

---

## Method 2: Cloud Run (Serverless)

### Step 1: Prepare Docker Image

```bash
# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/crypto-bot .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/crypto-bot
```

### Step 2: Deploy to Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy crypto-bot \
  --image gcr.io/YOUR_PROJECT_ID/crypto-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TELEGRAM_BOT_TOKEN=your_token
```

---

## Method 3: App Engine (Easiest)

### Step 1: Create app.yaml

```yaml
# app.yaml
runtime: python39
instance_class: F1  # Free tier
automatic_scaling:
  min_instances: 1
  max_instances: 1
env_variables:
  TELEGRAM_BOT_TOKEN: "your_bot_token_here"
```

### Step 2: Deploy to App Engine

```bash
# Deploy
gcloud app deploy

# View logs
gcloud app logs tail -s default
```

---

## Cost Breakdown

### Free Tier (12 months)
- **Compute Engine**: e2-micro instance (1 vCPU, 1GB RAM) - FREE
- **Storage**: 30GB persistent disk - FREE
- **Network**: 1GB egress per month - FREE
- **Total**: $0/month for first 12 months

### After Free Tier
- **Compute Engine**: $6.11/month
- **Storage**: $1.50/month  
- **Network**: $0.12/GB
- **Total**: ~$7.50/month

---

## Monitoring & Management

### Check Bot Status
```bash
# Check if running
ps aux | grep python

# Check systemd service
sudo systemctl status crypto-bot

# View logs
sudo journalctl -u crypto-bot -f
```

### Update Bot
```bash
# Pull latest changes
git pull origin main

# Restart service
sudo systemctl restart crypto-bot
```

### Backup Strategy
```bash
# Create snapshot of VM
gcloud compute disks snapshot crypto-bot-disk \
  --snapshot-names crypto-bot-backup-$(date +%Y%m%d) \
  --zone us-central1-a
```

---

## Security Setup

### 1. Firewall Rules
```bash
# Allow only SSH and HTTP/HTTPS
gcloud compute firewall-rules create allow-ssh-http \
  --allow tcp:22,tcp:80,tcp:443 \
  --source-ranges 0.0.0.0/0
```

### 2. Environment Variables
```bash
# Set environment variables securely
export TELEGRAM_BOT_TOKEN="your_token_here"

# Add to .bashrc for persistence
echo 'export TELEGRAM_BOT_TOKEN="your_token_here"' >> ~/.bashrc
```

### 3. Regular Updates
```bash
# Create update script
cat > update_bot.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/crypto-bot
git pull origin main
sudo systemctl restart crypto-bot
echo "Bot updated at $(date)"
EOF

chmod +x update_bot.sh

# Add to crontab (daily updates)
crontab -e
# Add: 0 2 * * * /home/ubuntu/crypto-bot/update_bot.sh
```

---

## Troubleshooting

### Bot Not Responding
```bash
# Check service status
sudo systemctl status crypto-bot

# Check logs
sudo journalctl -u crypto-bot -n 50

# Restart service
sudo systemctl restart crypto-bot
```

### High Resource Usage
```bash
# Monitor resources
htop

# Check memory usage
free -h

# Restart if needed
sudo systemctl restart crypto-bot
```

### Network Issues
```bash
# Test internet connectivity
ping google.com

# Test API access
curl https://api.coingecko.com/api/v3/ping

# Test Telegram API
curl https://api.telegram.org/bot<TOKEN>/getMe
```

---

## Quick Commands Reference

```bash
# Connect to VM
gcloud compute ssh crypto-bot-vm --zone=us-central1-a

# Check VM status
gcloud compute instances list

# Start/stop VM
gcloud compute instances start crypto-bot-vm --zone=us-central1-a
gcloud compute instances stop crypto-bot-vm --zone=us-central1-a

# View logs
gcloud logging read "resource.type=gce_instance" --limit=50

# Create snapshot
gcloud compute disks snapshot crypto-bot-disk --zone=us-central1-a
```

---

## Advanced Features

### 1. Auto-scaling
```bash
# Create instance template
gcloud compute instance-templates create crypto-bot-template \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud

# Create managed instance group
gcloud compute instance-groups managed create crypto-bot-group \
  --template=crypto-bot-template \
  --size=1 \
  --zone=us-central1-a
```

### 2. Load Balancing
```bash
# Create load balancer
gcloud compute backend-services create crypto-bot-backend \
  --global

# Add instances to backend
gcloud compute backend-services add-backend crypto-bot-backend \
  --instance-group=crypto-bot-group \
  --global
```

### 3. Monitoring
```bash
# Install monitoring agent
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install
```

---

## Quick Start Script

```bash
#!/bin/bash
# Quick deployment script for Google Cloud

echo "🚀 Deploying Crypto Bot to Google Cloud..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv git -y

# Setup bot
mkdir -p ~/crypto-bot && cd ~/crypto-bot
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate

# Install bot dependencies
pip install python-telegram-bot aiohttp schedule python-dotenv requests

# Setup systemd service
sudo cp crypto-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crypto-bot
sudo systemctl start crypto-bot

echo "✅ Bot deployed successfully!"
echo "📊 Check status: sudo systemctl status crypto-bot"
echo "📋 View logs: sudo journalctl -u crypto-bot -f"
```

---

## Support & Resources

- **Google Cloud Documentation**: https://cloud.google.com/docs
- **Compute Engine Pricing**: https://cloud.google.com/compute/pricing
- **Free Tier Limits**: https://cloud.google.com/free
- **Community Support**: https://cloud.google.com/community

Your crypto bot is now ready for Google Cloud deployment! 🚀📈
