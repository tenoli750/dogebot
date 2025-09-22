# 🧠 Real ROMA AI Integration Setup Guide

## 🚀 **Connect Your Bot to Real ROMA AI Server**

Your current bot is using **simulated responses**. Let's connect it to the **real ROMA AI server** for genuine AI capabilities!

---

## 🔧 **Step 1: Start ROMA Server**

### **Option A: Automated Start**
```bash
# Run the automated script
./start_roma_server.sh
```

### **Option B: Manual Start**
```bash
# Navigate to ROMA directory
cd /Users/jaehongkweon/Downloads/ROMA-main

# Start ROMA server
python src/sentientresearchagent/server/main.py
```

### **Option C: Background Start**
```bash
# Start ROMA server in background
nohup python src/sentientresearchagent/server/main.py > roma_server.log 2>&1 &
```

---

## 🤖 **Step 2: Start Real ROMA Bot**

### **Terminal 1: ROMA Server**
```bash
cd /Users/jaehongkweon/Downloads/ROMA-main
python src/sentientresearchagent/server/main.py
```

### **Terminal 2: Real ROMA Bot**
```bash
cd /Users/jaehongkweon/Downloads/ROMA-main
python real_roma_bot.py
```

---

## 🔍 **Step 3: Test Real ROMA Integration**

### **Test Commands:**
```
/start - See all features
/think What is blockchain? - Real ROMA thinking
/analyze bitcoin market - Real ROMA analysis
/research DeFi protocols - Real ROMA research
Tell me about Ethereum - Natural chat with ROMA
```

### **Expected Behavior:**
- ✅ **Real ROMA responses** (not simulated)
- ✅ **Different answers** for each question
- ✅ **Intelligent analysis** from ROMA server
- ✅ **Context-aware responses**

---

## 🚨 **Troubleshooting**

### **If ROMA Server Won't Start:**
```bash
# Check if port 5000 is available
lsof -i :5000

# Kill any process using port 5000
kill -9 $(lsof -t -i:5000)

# Try starting ROMA server again
python src/sentientresearchagent/server/main.py
```

### **If Bot Can't Connect to ROMA:**
```bash
# Check if ROMA server is running
curl http://localhost:5000/health

# Check ROMA server logs
tail -f roma_server.log
```

### **If Getting Same Responses:**
- ✅ **ROMA server is running** (check with `curl http://localhost:5000`)
- ✅ **Bot is using real_roma_bot.py** (not top100_crypto_bot.py)
- ✅ **ROMA server is responding** (check logs)

---

## 🔄 **Deploy Real ROMA Bot**

### **Option 1: Replace Current Bot**
```bash
# Backup current bot
cp top100_crypto_bot.py top100_crypto_bot_backup.py

# Replace with real ROMA bot
cp real_roma_bot.py top100_crypto_bot.py

# Commit and push
git add .
git commit -m "Replace with real ROMA integration"
git push origin main
```

### **Option 2: Deploy as New Service**
```bash
# Deploy real ROMA bot to Render
# Update render.yaml to use real_roma_bot.py
```

---

## 🎯 **Real ROMA Features**

### **✅ What You'll Get:**
- 🧠 **Real AI thinking** from ROMA server
- 📊 **Genuine analysis** with different responses
- 🔍 **Actual research** capabilities
- 💬 **Intelligent conversations** that vary
- 🎯 **Context-aware responses** that remember

### **✅ Commands That Use Real ROMA:**
- `/think <question>` - Real ROMA thinking
- `/analyze <topic>` - Real ROMA analysis
- `/research <topic>` - Real ROMA research
- Natural chat - Real ROMA responses

### **✅ Commands That Don't Use ROMA:**
- `/p <coin>` - Crypto prices (CoinGecko API)
- `/top10` - Top 10 cryptocurrencies
- `/top20` - Top 20 cryptocurrencies

---

## 🚀 **Quick Start Commands**

### **Start Everything:**
```bash
# Terminal 1: Start ROMA server
cd /Users/jaehongkweon/Downloads/ROMA-main
python src/sentientresearchagent/server/main.py

# Terminal 2: Start real ROMA bot
cd /Users/jaehongkweon/Downloads/ROMA-main
python real_roma_bot.py
```

### **Test Real ROMA:**
```
/think What is DeFi?
/analyze ethereum market
Tell me about blockchain
```

---

## 🎉 **Success Indicators**

### **✅ Real ROMA is Working When:**
- Different responses for each question
- Intelligent analysis with insights
- Context-aware responses
- No "simulated" or "fallback" messages

### **❌ ROMA is Not Working When:**
- Same responses every time
- "Local AI fallback" messages
- Generic responses
- No connection to ROMA server

---

## 🔧 **Advanced Configuration**

### **Custom ROMA Server URL:**
```python
# In real_roma_bot.py, change:
self.roma_client = RealROMAClient("http://your-roma-server:5000")
```

### **Multiple ROMA Endpoints:**
The bot tries multiple endpoints automatically:
- `/api/thinking`
- `/api/simple/execute`
- `/thinking`
- `/api/agent/thinking`

---

## 📱 **Test Your Real ROMA Bot**

1. **Start ROMA server** using the guide above
2. **Start real ROMA bot** with `python real_roma_bot.py`
3. **Test commands** in Telegram:
   - `/think What is blockchain?`
   - `/analyze bitcoin market`
   - `Tell me about DeFi`
4. **Verify responses** are different and intelligent

**Your bot now has real ROMA AI capabilities!** 🧠🚀
