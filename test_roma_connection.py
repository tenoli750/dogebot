#!/usr/bin/env python3
"""
Test ROMA Server Connection
"""

import asyncio
import aiohttp
import sys

async def test_roma_connection():
    """Test connection to ROMA server"""
    
    # Try different ROMA server URLs
    roma_urls = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    async with aiohttp.ClientSession() as session:
        for url in roma_urls:
            try:
                print(f"🔍 Testing {url}...")
                
                # Test health endpoint
                async with session.get(f"{url}/health", timeout=5) as response:
                    if response.status == 200:
                        print(f"✅ ROMA server is running at {url}")
                        return url
                
                # Test root endpoint
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        print(f"✅ ROMA server is running at {url}")
                        return url
                        
            except Exception as e:
                print(f"❌ {url} failed: {e}")
                continue
    
    print("❌ No ROMA server found")
    return None

async def test_roma_endpoints(roma_url):
    """Test ROMA endpoints"""
    endpoints = [
        "/api/thinking",
        "/api/simple/execute", 
        "/thinking",
        "/api/agent/thinking",
        "/api/analysis",
        "/api/simple/analysis",
        "/analysis",
        "/api/agent/analysis"
    ]
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            try:
                url = f"{roma_url}{endpoint}"
                print(f"🔍 Testing {url}...")
                
                payload = {
                    "goal": "Test connection",
                    "question": "What is blockchain?",
                    "task_type": "thinking"
                }
                
                async with session.post(url, json=payload, timeout=10) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ {endpoint} working: {result}")
                        return endpoint
                    else:
                        print(f"❌ {endpoint} returned {response.status}")
                        
            except Exception as e:
                print(f"❌ {endpoint} failed: {e}")
                continue
    
    print("❌ No working ROMA endpoints found")
    return None

async def main():
    """Main test function"""
    print("🧠 Testing ROMA Server Connection...")
    print("=" * 50)
    
    # Test connection
    roma_url = await test_roma_connection()
    
    if roma_url:
        print(f"\n🔍 Testing ROMA endpoints at {roma_url}...")
        working_endpoint = await test_roma_endpoints(roma_url)
        
        if working_endpoint:
            print(f"\n✅ ROMA server is working!")
            print(f"🔗 URL: {roma_url}")
            print(f"📡 Working endpoint: {working_endpoint}")
        else:
            print(f"\n❌ ROMA server found but no working endpoints")
    else:
        print("\n❌ No ROMA server found")
        print("\n🔧 To start ROMA server:")
        print("   cd /Users/jaehongkweon/Downloads/ROMA-main")
        print("   python3 src/sentientresearchagent/server/main.py")

if __name__ == "__main__":
    asyncio.run(main())
