#!/usr/bin/env python3
"""
Test config loading
"""

import os
import sys
import pathlib

# Set up environment variables BEFORE any imports
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_USERNAME"] = "default"
os.environ["REDIS_PASSWORD"] = ""
os.environ["REDIS_DB"] = "0"
os.environ["REDIS_SSL"] = "false"

# Fix Python path
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

print("Environment variables:")
print(f"REDIS_HOST: {os.environ.get('REDIS_HOST')}")
print(f"REDIS_PORT: {os.environ.get('REDIS_PORT')}")
print(f"REDIS_DB: {os.environ.get('REDIS_DB')}")

try:
    from config.config import get_config
    config = get_config()
    print(f"✅ Config loaded successfully")
    print(f"Redis host: {config.redis.host}")
    print(f"Redis port: {config.redis.port}")
    print(f"Redis db: {config.redis.db}")
except Exception as e:
    print(f"❌ Config loading failed: {e}")
    import traceback
    traceback.print_exc()
