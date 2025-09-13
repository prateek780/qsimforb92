#!/usr/bin/env python3
"""
Test topology storage and retrieval
"""

import os
import json
import sys

# Add current directory to path
sys.path.insert(0, '.')

def test_redis_connection():
    """Test Redis connection"""
    try:
        from data.models.connection.redis import get_redis_conn
        conn = get_redis_conn()
        if conn:
            print("✅ Redis connection successful")
            keys = conn.keys('*')
            print(f"Redis keys found: {len(keys)}")
            for key in keys[:10]:  # Show first 10 keys
                print(f"  - {key}")
            return True
        else:
            print("❌ Redis connection failed")
            return False
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

def test_file_storage():
    """Test if there are any topology files"""
    print("\n🔍 Checking for topology files...")
    
    # Check for JSON files that might contain topologies
    json_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.json') and 'topology' in file.lower():
                json_files.append(os.path.join(root, file))
    
    print(f"Found {len(json_files)} potential topology files:")
    for file in json_files:
        print(f"  - {file}")
    
    # Check for network.json
    if os.path.exists('network.json'):
        print("✅ Found network.json")
        try:
            with open('network.json', 'r') as f:
                data = json.load(f)
            print(f"  - Contains {len(data.get('zones', []))} zones")
        except Exception as e:
            print(f"  - Error reading: {e}")
    else:
        print("❌ No network.json found")
    
    # Check lab files
    if os.path.exists('lab/lab5_world.json'):
        print("✅ Found lab5_world.json")
        try:
            with open('lab/lab5_world.json', 'r') as f:
                data = json.load(f)
            print(f"  - Contains {len(data.get('zones', []))} zones")
        except Exception as e:
            print(f"  - Error reading: {e}")

def create_sample_topology():
    """Create a sample topology for testing"""
    print("\n🔧 Creating sample topology...")
    
    sample_topology = {
        "name": "test1",
        "size": [1000, 1000],
        "zones": [
            {
                "name": "Zone1",
                "position": [0, 0],
                "size": [500, 500],
                "networks": [
                    {
                        "name": "QuantumNetwork1",
                        "hosts": [
                            {
                                "name": "Alice",
                                "position": [100, 100],
                                "type": "InteractiveQuantumHost"
                            },
                            {
                                "name": "Bob", 
                                "position": [200, 200],
                                "type": "InteractiveQuantumHost"
                            }
                        ],
                        "channels": [
                            {
                                "name": "Alice-Bob",
                                "from_host": "Alice",
                                "to_host": "Bob",
                                "length": 100.0,
                                "loss_per_km": 0.1
                            }
                        ]
                    }
                ]
            }
        ],
        "temporary_world": False,
        "lab_world": False,
        "owner": "Default"
    }
    
    # Save to file
    with open('test1_topology.json', 'w') as f:
        json.dump(sample_topology, f, indent=2)
    
    print("✅ Created test1_topology.json")

def test_topology_api():
    """Test the topology API endpoints"""
    print("\n🔍 Testing topology API...")
    
    try:
        # Test if we can import the topology functions
        from data.models.topology.world_model import get_all_topologies_from_redis
        topologies = get_all_topologies_from_redis()
        print(f"✅ Found {len(topologies)} topologies from Redis")
        
        for topo in topologies:
            print(f"  - {topo.name} (owner: {topo.owner})")
            
    except Exception as e:
        print(f"❌ Topology API error: {e}")

if __name__ == "__main__":
    print("🔍 Testing Topology Storage...")
    print("=" * 50)
    
    # Test Redis connection
    redis_ok = test_redis_connection()
    
    # Test file storage
    test_file_storage()
    
    # Test topology API
    test_topology_api()
    
    # Create sample topology if needed
    if not os.path.exists('test1_topology.json'):
        create_sample_topology()
    
    print("\n" + "=" * 50)
    if redis_ok:
        print("✅ Redis is working - topologies should be saved there")
    else:
        print("❌ Redis is not working - topologies need to be saved to files")
        print("💡 The simulation UI might not be able to load saved topologies")
