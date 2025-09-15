#!/usr/bin/env python3
"""
Redis Cleanup Utility
Clears Redis memory to prevent conflicts between BB84 and B92 protocols
"""

import redis
import os
import sys

def clear_redis_memory():
    """Clear Redis memory to prevent protocol conflicts"""
    try:
        # Connect to Redis
        r = redis.Redis(
            host='redis-11509.c90.us-east-1-3.ec2.redns.redis-cloud.com',
            port=11509,
            username='default',
            password='aDevCXKeLli9kldGJccV15D1yS93Oyvd',
            db=0,
            ssl=False,
            socket_timeout=5
        )
        
        # Test connection
        r.ping()
        print("✅ Connected to Redis successfully")
        
        # Get memory info
        info = r.info('memory')
        used_memory = info.get('used_memory', 0)
        used_memory_human = info.get('used_memory_human', 'unknown')
        maxmemory = info.get('maxmemory', 0)
        maxmemory_human = info.get('maxmemory_human', 'unknown')
        
        print(f"📊 Redis Memory Status:")
        print(f"   Used: {used_memory_human} ({used_memory} bytes)")
        print(f"   Max:  {maxmemory_human} ({maxmemory} bytes)")
        
        if maxmemory > 0 and used_memory > maxmemory * 0.8:
            print("⚠️  Redis memory usage is high (>80%)")
        
        # Clear all keys
        keys = r.keys('*')
        if keys:
            deleted_count = r.delete(*keys)
            print(f"🧹 Cleared {deleted_count} keys from Redis")
            
            # Get new memory info
            new_info = r.info('memory')
            new_used_memory = new_info.get('used_memory', 0)
            new_used_memory_human = new_info.get('used_memory_human', 'unknown')
            
            print(f"📊 Redis Memory After Cleanup:")
            print(f"   Used: {new_used_memory_human} ({new_used_memory} bytes)")
            print(f"   Freed: {used_memory - new_used_memory} bytes")
        else:
            print("✅ Redis is already clean - no keys to clear")
            
        return True
        
    except redis.exceptions.ConnectionError as e:
        print(f"❌ Could not connect to Redis: {e}")
        return False
    except redis.exceptions.OutOfMemoryError as e:
        print(f"❌ Redis out of memory: {e}")
        return False
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

def ensure_single_protocol():
    """Ensure only one protocol is active at a time"""
    print("\n🔍 Checking protocol status files...")
    
    bb84_file = "student_implementation_status.json"
    b92_file = "student_b92_implementation_status.json"
    b92_disabled_file = "student_b92_implementation_status.json.disabled"
    
    bb84_exists = os.path.exists(bb84_file)
    b92_exists = os.path.exists(b92_file)
    b92_disabled = os.path.exists(b92_disabled_file)
    
    print(f"   BB84 status file: {'✅ exists' if bb84_exists else '❌ missing'}")
    print(f"   B92 status file: {'✅ exists' if b92_exists else '❌ missing'}")
    print(f"   B92 disabled: {'✅ yes' if b92_disabled else '❌ no'}")
    
    if bb84_exists and b92_exists and not b92_disabled:
        print("⚠️  WARNING: Both BB84 and B92 protocols are active!")
        print("   This can cause Redis memory conflicts.")
        print("   Consider disabling one protocol before running simulations.")
        return False
    elif bb84_exists and not b92_disabled:
        print("✅ BB84 protocol is active")
    elif b92_exists and not b92_disabled:
        print("✅ B92 protocol is active")
    else:
        print("ℹ️  No protocols are currently active")
    
    return True

if __name__ == "__main__":
    print("🧹 Redis Cleanup Utility")
    print("=" * 50)
    
    # Clear Redis memory
    success = clear_redis_memory()
    
    # Check protocol status
    protocol_ok = ensure_single_protocol()
    
    if success and protocol_ok:
        print("\n✅ Redis cleanup completed successfully!")
        print("💡 You can now run your quantum protocol simulation")
    else:
        print("\n❌ Redis cleanup had issues")
        if not success:
            print("   - Redis memory cleanup failed")
        if not protocol_ok:
            print("   - Multiple protocols are active (may cause conflicts)")
        
    sys.exit(0 if success and protocol_ok else 1)
