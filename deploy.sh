#!/bin/bash

# Crypto Bot Server Deployment Script
# This script helps deploy your crypto bot to a server

set -e

echo "🚀 Crypto Bot Server Deployment"
echo "================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root"
    exit 1
fi

# Function to install systemd service
install_systemd() {
    echo "📦 Installing systemd service..."
    
    # Stop existing service if running
    sudo systemctl stop crypto-bot 2>/dev/null || true
    
    # Copy service file
    sudo cp crypto-bot.service /etc/systemd/system/
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable and start service
    sudo systemctl enable crypto-bot
    sudo systemctl start crypto-bot
    
    echo "✅ Systemd service installed and started"
    echo "📊 Check status: sudo systemctl status crypto-bot"
    echo "📋 View logs: sudo journalctl -u crypto-bot -f"
}

# Function to install with Docker
install_docker() {
    echo "🐳 Installing with Docker..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "📦 Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        echo "✅ Docker installed. Please log out and back in to use Docker without sudo"
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo "📦 Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Build and start container
    docker-compose up -d --build
    
    echo "✅ Docker container started"
    echo "📊 Check status: docker-compose ps"
    echo "📋 View logs: docker-compose logs -f"
}

# Function to setup monitoring
setup_monitoring() {
    echo "📊 Setting up monitoring..."
    
    # Create monitoring script
    cat > monitor_bot.sh << 'EOF'
#!/bin/bash
# Simple monitoring script for crypto bot

BOT_PID=$(pgrep -f "python.*top100_crypto_bot.py" || echo "")
if [ -z "$BOT_PID" ]; then
    echo "$(date): Bot not running, restarting..."
    cd /home/ubuntu/crypto-bot
    source crypto_bot_env/bin/activate
    nohup python top100_crypto_bot.py > bot.log 2>&1 &
    echo "$(date): Bot restarted"
else
    echo "$(date): Bot running (PID: $BOT_PID)"
fi
EOF
    
    chmod +x monitor_bot.sh
    
    # Add to crontab (check every 5 minutes)
    (crontab -l 2>/dev/null; echo "*/5 * * * * $(pwd)/monitor_bot.sh >> $(pwd)/monitor.log 2>&1") | crontab -
    
    echo "✅ Monitoring setup complete"
}

# Main menu
echo "Choose deployment method:"
echo "1) Systemd service (recommended for Linux servers)"
echo "2) Docker container (recommended for cloud platforms)"
echo "3) Simple background process with monitoring"
echo "4) Exit"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        install_systemd
        setup_monitoring
        ;;
    2)
        install_docker
        ;;
    3)
        echo "🔄 Starting bot in background..."
        nohup python top100_crypto_bot.py > bot.log 2>&1 &
        echo "✅ Bot started in background"
        setup_monitoring
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo "📱 Your bot should now be running on your server"
echo "🔗 Test it by messaging your bot on Telegram"
