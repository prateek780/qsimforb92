#!/usr/bin/env python3
"""
Debug B92 Routes
================

Debug why B92 API routes are returning 404
"""

import requests
import json

def debug_b92_routes():
    """Debug B92 route issues"""
    base_url = "http://localhost:5174"
    
    print("🔍 Debugging B92 Routes...")
    print("=" * 40)
    
    # Test 1: Check if server is running
    print("\n1. Testing server health...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"✅ Server is running (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return
    
    # Test 2: Check B92 status endpoint
    print("\n2. Testing B92 status endpoint...")
    try:
        response = requests.get(f"{base_url}/api/b92/status", timeout=5)
        print(f"✅ B92 status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ B92 status error: {e}")
    
    # Test 3: Check B92 events endpoint
    print("\n3. Testing B92 events endpoint...")
    try:
        response = requests.get(f"{base_url}/api/b92/events", timeout=5)
        print(f"✅ B92 events: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ B92 events error: {e}")
    
    # Test 4: Check B92 simulation start
    print("\n4. Testing B92 simulation start...")
    try:
        response = requests.post(f"{base_url}/api/b92/simulation/start", timeout=5)
        print(f"✅ B92 simulation start: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ B92 simulation start error: {e}")
    
    # Test 5: Check available routes
    print("\n5. Checking available routes...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi = response.json()
            b92_routes = [path for path in openapi.get("paths", {}).keys() if "/api/b92/" in path]
            print(f"✅ Found B92 routes: {b92_routes}")
        else:
            print(f"❌ Could not get OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI error: {e}")

if __name__ == "__main__":
    debug_b92_routes()


