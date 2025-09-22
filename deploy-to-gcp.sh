#!/bin/bash

# Google Cloud Platform Deployment Script
# This script will help you deploy your crypto bot to Google Cloud

echo "🚀 Google Cloud Crypto Bot Deployment"
echo "====================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Please login to Google Cloud first:"
    echo "   gcloud auth login"
    exit 1
fi

echo "✅ Google Cloud CLI is ready"

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project selected. Please set a project:"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Project: $PROJECT_ID"

# Create VM instance
echo "🖥️  Creating VM instance..."
gcloud compute instances create crypto-bot-vm \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --zone=us-central1-a \
    --tags=crypto-bot \
    --metadata=startup-script='#!/bin/bash
apt-get update
apt-get install -y python3-pip python3-venv git curl
'

echo "⏳ Waiting for VM to be ready..."
sleep 30

# Upload bot files
echo "📤 Uploading bot files..."
gcloud compute scp top100_crypto_bot.py crypto-bot-vm:~/ --zone=us-central1-a
gcloud compute scp requirements_crypto_bot.txt crypto-bot-vm:~/ --zone=us-central1-a
gcloud compute scp crypto_bot.env crypto-bot-vm:~/ --zone=us-central1-a
gcloud compute scp gcp-quick-deploy.sh crypto-bot-vm:~/ --zone=us-central1-a

# Deploy on VM
echo "🚀 Deploying bot on VM..."
gcloud compute ssh crypto-bot-vm --zone=us-central1-a --command="
    chmod +x gcp-quick-deploy.sh
    ./gcp-quick-deploy.sh
"

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "📊 Your crypto bot is now running on Google Cloud!"
echo "🖥️  VM Instance: crypto-bot-vm"
echo "🌍 Zone: us-central1-a"
echo ""
echo "📋 Management Commands:"
echo "  Connect to VM: gcloud compute ssh crypto-bot-vm --zone=us-central1-a"
echo "  Check status:  gcloud compute ssh crypto-bot-vm --zone=us-central1-a --command='sudo systemctl status crypto-bot'"
echo "  View logs:     gcloud compute ssh crypto-bot-vm --zone=us-central1-a --command='sudo journalctl -u crypto-bot -f'"
echo "  Stop VM:       gcloud compute instances stop crypto-bot-vm --zone=us-central1-a"
echo "  Start VM:      gcloud compute instances start crypto-bot-vm --zone=us-central1-a"
echo ""
echo "💰 Cost: ~$6/month (free tier eligible for 12 months)"
echo "🔗 Your bot should be responding on Telegram now!"
