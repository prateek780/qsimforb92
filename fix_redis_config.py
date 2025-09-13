#!/usr/bin/env python3
"""
Fix Redis configuration by setting environment variables
"""

import os

# Set Redis environment variables
os.environ['REDIS_HOST'] = 'redis-11509.c90.us-east-1-3.ec2.redns.redis-cloud.com'
os.environ['REDIS_PORT'] = '11509'
os.environ['REDIS_USERNAME'] = 'default'
os.environ['REDIS_PASSWORD'] = 'aDevCXKeLli9kldGJccV15D1yS93Oyvd'
os.environ['REDIS_DB'] = '0'
os.environ['REDIS_SSL'] = 'false'

print("✅ Redis environment variables set")
print(f"REDIS_HOST: {os.environ['REDIS_HOST']}")
print(f"REDIS_PORT: {os.environ['REDIS_PORT']}")
print(f"REDIS_USERNAME: {os.environ['REDIS_USERNAME']}")
print(f"REDIS_DB: {os.environ['REDIS_DB']}")
print(f"REDIS_SSL: {os.environ['REDIS_SSL']}")

# Test Redis connection
try:
    from data.models.connection.redis import get_redis_conn
    conn = get_redis_conn()
    if conn:
        print("✅ Redis connection successful!")
        keys = conn.keys('*')
        print(f"Found {len(keys)} keys in Redis")
    else:
        print("❌ Redis connection failed")
except Exception as e:
    print(f"❌ Redis error: {e}")
