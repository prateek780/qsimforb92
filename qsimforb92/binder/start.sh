#!/bin/bash

# Binder startup script for Quantum Networking System
echo "🚀 Starting Quantum Networking System on Binder..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export REDIS_URL="redis://localhost:6379"
export REDIS_SSL="false"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_DB="0"
export REDIS_USERNAME="default"
export REDIS_PASSWORD=""

# Create necessary directories
mkdir -p saved_topologies
mkdir -p simulation_logs

# Disable problematic features for Binder
export DISABLE_EMBEDDING=1
export DISABLE_AI_FEATURES=1
export DISABLE_REDIS_LOGGING=1

# Start Redis if available (optional for Binder)
if command -v redis-server &> /dev/null; then
    echo "📦 Starting Redis server..."
    redis-server --daemonize yes --port 6379 --maxmemory 100mb --maxmemory-policy allkeys-lru
    sleep 2
else
    echo "⚠️ Redis not available, using file storage fallback"
    echo "💡 This is normal for Binder deployment"
fi

# Start the FastAPI application
echo "🌐 Starting FastAPI server on port ${PORT:-8080}..."
export HOST="0.0.0.0"
export PORT="${PORT:-8080}"
python start.py
