#!/usr/bin/env python3
"""
Fix Redis environment variables and test connection
"""

import os
import sys

# Set Redis environment variables BEFORE importing any config
os.environ['REDIS_HOST'] = 'redis-11509.c90.us-east-1-3.ec2.redns.redis-cloud.com'
os.environ['REDIS_PORT'] = '11509'
os.environ['REDIS_USERNAME'] = 'default'
os.environ['REDIS_PASSWORD'] = 'aDevCXKeLli9kldGJccV15D1yS93Oyvd'
os.environ['REDIS_DB'] = '0'
os.environ['REDIS_SSL'] = 'false'

print("✅ Redis environment variables set:")
print(f"  REDIS_HOST: {os.environ['REDIS_HOST']}")
print(f"  REDIS_PORT: {os.environ['REDIS_PORT']}")
print(f"  REDIS_USERNAME: {os.environ['REDIS_USERNAME']}")
print(f"  REDIS_DB: {os.environ['REDIS_DB']}")
print(f"  REDIS_SSL: {os.environ['REDIS_SSL']}")

# Now test the Redis connection
try:
    from data.models.connection.redis import get_redis_conn
    conn = get_redis_conn()
    
    if conn:
        print("✅ Redis connection successful!")
        keys = conn.keys('*')
        print(f"Found {len(keys)} keys in Redis")
        
        # Test saving a sample topology
        from data.models.topology.world_model import WorldModal, save_world_to_redis
        
        # Create a test topology
        test_topology = {
            "name": "test_redis",
            "size": [1000, 1000],
            "zones": [
                {
                    "name": "TestZone",
                    "position": [0, 0],
                    "size": [500, 500],
                    "networks": [
                        {
                            "name": "TestNetwork",
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
        
        # Save to Redis
        world = save_world_to_redis(test_topology)
        print(f"✅ Test topology saved with ID: {world.pk}")
        
        # Test retrieving it
        from data.models.topology.world_model import get_topology_from_redis
        retrieved = get_topology_from_redis(world.pk)
        if retrieved:
            print(f"✅ Test topology retrieved: {retrieved.name}")
        else:
            print("❌ Failed to retrieve test topology")
            
    else:
        print("❌ Redis connection failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
