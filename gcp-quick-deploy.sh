#!/bin/bash

# Google Cloud Platform Quick Deployment Script
# This script automates the deployment of your crypto bot to Google Cloud

set -e

echo "🚀 Google Cloud Crypto Bot Deployment"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Google Cloud
check_gcp() {
    if ! curl -s -f http://metadata.google.internal/computeMetadata/v1/instance/name > /dev/null; then
        print_error "This script must be run on a Google Cloud VM instance"
        exit 1
    fi
    print_success "Running on Google Cloud VM"
}

# Install system dependencies
install_dependencies() {
    print_status "Installing system dependencies..."
    
    sudo apt update
    sudo apt install -y python3-pip python3-venv git curl wget htop
    
    print_success "Dependencies installed"
}

# Setup Python environment
setup_python() {
    print_status "Setting up Python environment..."
    
    # Create project directory
    mkdir -p ~/crypto-bot
    cd ~/crypto-bot
    
    # Create virtual environment
    python3 -m venv crypto_bot_env
    source crypto_bot_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    print_success "Python environment ready"
}

# Install bot dependencies
install_bot_deps() {
    print_status "Installing bot dependencies..."
    
    # Install required packages
    pip install python-telegram-bot aiohttp schedule python-dotenv requests
    
    print_success "Bot dependencies installed"
}

# Setup bot files
setup_bot_files() {
    print_status "Setting up bot files..."
    
    # Create bot files if they don't exist
    if [ ! -f "top100_crypto_bot.py" ]; then
        print_warning "Bot file not found. Please upload your bot files to ~/crypto-bot/"
        print_status "You can use: gcloud compute scp local_file crypto-bot-vm:~/crypto-bot/ --zone=us-central1-a"
        exit 1
    fi
    
    # Create environment file if it doesn't exist
    if [ ! -f "crypto_bot.env" ]; then
        print_status "Creating environment file..."
        cat > crypto_bot.env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
EOF
        print_warning "Please edit crypto_bot.env and add your Telegram bot token"
    fi
    
    print_success "Bot files ready"
}

# Setup systemd service
setup_systemd() {
    print_status "Setting up systemd service..."
    
    # Get current user
    USER=$(whoami)
    WORK_DIR=$(pwd)
    
    # Create systemd service file
    sudo tee /etc/systemd/system/crypto-bot.service > /dev/null << EOF
[Unit]
Description=Crypto Bot Telegram Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORK_DIR
Environment=PATH=$WORK_DIR/crypto_bot_env/bin
ExecStart=$WORK_DIR/crypto_bot_env/bin/python top100_crypto_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    print_success "Systemd service configured"
}

# Start the bot
start_bot() {
    print_status "Starting crypto bot..."
    
    # Enable and start service
    sudo systemctl enable crypto-bot
    sudo systemctl start crypto-bot
    
    # Wait a moment for startup
    sleep 3
    
    # Check status
    if sudo systemctl is-active --quiet crypto-bot; then
        print_success "Crypto bot is running!"
    else
        print_error "Failed to start crypto bot"
        print_status "Check logs with: sudo journalctl -u crypto-bot -f"
        exit 1
    fi
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Create monitoring script
    cat > monitor_bot.sh << 'EOF'
#!/bin/bash
# Monitor script for crypto bot

BOT_STATUS=$(systemctl is-active crypto-bot)
if [ "$BOT_STATUS" != "active" ]; then
    echo "$(date): Bot not running, restarting..."
    sudo systemctl restart crypto-bot
    echo "$(date): Bot restarted"
else
    echo "$(date): Bot running normally"
fi
EOF
    
    chmod +x monitor_bot.sh
    
    # Add to crontab (check every 5 minutes)
    (crontab -l 2>/dev/null; echo "*/5 * * * * $(pwd)/monitor_bot.sh >> $(pwd)/monitor.log 2>&1") | crontab -
    
    print_success "Monitoring setup complete"
}

# Display status and commands
show_status() {
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo ""
    echo "📊 Bot Status:"
    sudo systemctl status crypto-bot --no-pager
    echo ""
    echo "📋 Useful Commands:"
    echo "  Check status: sudo systemctl status crypto-bot"
    echo "  View logs:    sudo journalctl -u crypto-bot -f"
    echo "  Restart bot:  sudo systemctl restart crypto-bot"
    echo "  Stop bot:     sudo systemctl stop crypto-bot"
    echo "  Start bot:    sudo systemctl start crypto-bot"
    echo ""
    echo "📁 Bot Location: ~/crypto-bot/"
    echo "📝 Logs: sudo journalctl -u crypto-bot -f"
    echo ""
    echo "🔧 Configuration:"
    echo "  Edit bot: nano ~/crypto-bot/top100_crypto_bot.py"
    echo "  Edit env:  nano ~/crypto-bot/crypto_bot.env"
    echo ""
    echo "🚀 Your crypto bot is now running on Google Cloud!"
}

# Main deployment function
main() {
    print_status "Starting Google Cloud deployment..."
    
    # Check if running on GCP
    check_gcp
    
    # Install dependencies
    install_dependencies
    
    # Setup Python environment
    setup_python
    
    # Install bot dependencies
    install_bot_deps
    
    # Setup bot files
    setup_bot_files
    
    # Setup systemd service
    setup_systemd
    
    # Start the bot
    start_bot
    
    # Setup monitoring
    setup_monitoring
    
    # Show status
    show_status
}

# Run main function
main "$@"
