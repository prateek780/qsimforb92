#!/usr/bin/env python3
"""
Start the server with Redis environment variables properly set
"""

import os
import sys

# Set Redis environment variables BEFORE importing any modules
os.environ['REDIS_HOST'] = 'redis-11509.c90.us-east-1-3.ec2.redns.redis-cloud.com'
os.environ['REDIS_PORT'] = '11509'
os.environ['REDIS_USERNAME'] = 'default'
os.environ['REDIS_PASSWORD'] = 'aDevCXKeLli9kldGJccV15D1yS93Oyvd'
os.environ['REDIS_DB'] = '0'
os.environ['REDIS_SSL'] = 'false'

print("🔧 Setting Redis environment variables...")
print(f"  REDIS_HOST: {os.environ['REDIS_HOST']}")
print(f"  REDIS_PORT: {os.environ['REDIS_PORT']}")
print(f"  REDIS_USERNAME: {os.environ['REDIS_USERNAME']}")
print(f"  REDIS_DB: {os.environ['REDIS_DB']}")
print(f"  REDIS_SSL: {os.environ['REDIS_SSL']}")

# Now import and start the server
if __name__ == "__main__":
    # Import start.py and run it
    import start
