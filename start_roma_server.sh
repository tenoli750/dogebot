#!/bin/bash

# Start ROMA Server for Real AI Integration
echo "🚀 Starting ROMA Server for Real AI Integration..."

# Navigate to ROMA directory
cd /Users/jaehongkweon/Downloads/ROMA-main

# Check if ROMA server is already running
if pgrep -f "roma.*server" > /dev/null; then
    echo "✅ ROMA server is already running!"
    echo "🔗 ROMA Server URL: http://localhost:5000"
    echo "🧠 Ready for real AI integration!"
    exit 0
fi

# Start ROMA server
echo "🔄 Starting ROMA server..."
python src/sentientresearchagent/server/main.py &

# Wait a moment for server to start
sleep 3

# Check if server started successfully
if pgrep -f "roma.*server" > /dev/null; then
    echo "✅ ROMA server started successfully!"
    echo "🔗 ROMA Server URL: http://localhost:5000"
    echo "🧠 Ready for real AI integration!"
    echo ""
    echo "📱 Now you can start your bot with:"
    echo "   python real_roma_bot.py"
else
    echo "❌ Failed to start ROMA server"
    echo "🔧 Try running manually:"
    echo "   cd /Users/jaehongkweon/Downloads/ROMA-main"
    echo "   python src/sentientresearchagent/server/main.py"
fi
