#!/usr/bin/env python3
"""
Test B92 Simulation Connection
=============================

This script tests the B92 simulation connection and endpoints.
"""

import requests
import json
import time

def test_b92_endpoints():
    """Test B92-specific endpoints"""
    base_url = "http://localhost:5174"
    
    print("🔬 Testing B92 Simulation Endpoints...")
    print("=" * 50)
    
    # Test 1: B92 student implementation status
    print("\n1. Testing B92 student implementation status...")
    try:
        response = requests.get(f"{base_url}/api/simulation/student-implementation-status-b92/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ B92 Status: {data}")
        else:
            print(f"❌ B92 Status failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ B92 Status error: {e}")
    
    # Test 2: B92 API status
    print("\n2. Testing B92 API status...")
    try:
        response = requests.get(f"{base_url}/api/b92/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ B92 API Status: {data}")
        else:
            print(f"❌ B92 API Status failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ B92 API Status error: {e}")
    
    # Test 3: B92 events
    print("\n3. Testing B92 events...")
    try:
        response = requests.get(f"{base_url}/api/b92/events", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ B92 Events: {data}")
        else:
            print(f"❌ B92 Events failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ B92 Events error: {e}")
    
    # Test 4: Start B92 simulation
    print("\n4. Testing B92 simulation start...")
    try:
        response = requests.post(f"{base_url}/api/b92/simulation/start", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ B92 Simulation Start: {data}")
        else:
            print(f"❌ B92 Simulation Start failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ B92 Simulation Start error: {e}")
    
    print("\n" + "=" * 50)
    print("🔬 B92 Testing Complete!")

if __name__ == "__main__":
    test_b92_endpoints()
