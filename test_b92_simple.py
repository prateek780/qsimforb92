#!/usr/bin/env python3
"""
Simple B92 Test
===============

Test B92 endpoints with minimal dependencies
"""

import requests
import time

def test_b92_simple():
    """Test B92 endpoints with simple requests"""
    base_url = "http://localhost:5174"
    
    print("🔬 Simple B92 Test...")
    print("=" * 30)
    
    # Test 1: Basic server health
    print("\n1. Server health check...")
    try:
        response = requests.get(f"{base_url}/api/simulation/student-implementation-status-b92/", timeout=2)
        print(f"✅ B92 status endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Protocol: {data.get('protocol')}")
            print(f"   Ready: {data.get('student_implementation_ready')}")
    except Exception as e:
        print(f"❌ B92 status error: {e}")
    
    # Test 2: B92 status with short timeout
    print("\n2. B92 API status (short timeout)...")
    try:
        response = requests.get(f"{base_url}/api/b92/status", timeout=1)
        print(f"✅ B92 API status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except requests.exceptions.Timeout:
        print("⏰ B92 API status timed out (1s)")
    except Exception as e:
        print(f"❌ B92 API status error: {e}")
    
    # Test 3: B92 events with short timeout
    print("\n3. B92 events (short timeout)...")
    try:
        response = requests.get(f"{base_url}/api/b92/events", timeout=1)
        print(f"✅ B92 events: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except requests.exceptions.Timeout:
        print("⏰ B92 events timed out (1s)")
    except Exception as e:
        print(f"❌ B92 events error: {e}")

if __name__ == "__main__":
    test_b92_simple()


