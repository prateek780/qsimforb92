#!/usr/bin/env python3
"""
Test B92 Logs
=============
Quick test to verify B92 events are being sent to the WebSocket.
"""

import asyncio
import json
from server.socket_server.socket_server_b92 import b92_connection_manager

async def test_b92_event():
    """Test sending a B92 event"""
    test_message = {
        "type": "b92_event",
        "event_type": "student_b92_test",
        "node": "TestNode",
        "timestamp": asyncio.get_event_loop().time(),
        "data": {
            "message": "🔬 Test B92 Event: This is a test message to verify B92 logging works!",
            "protocol": "B92",
            "student_method": "test"
        },
        "log_level": "PROTOCOL",
        "protocol": "B92"
    }
    
    print("📤 Sending test B92 event...")
    await b92_connection_manager.broadcast(test_message)
    print("✅ Test B92 event sent!")

def test_b92_sync():
    """Test B92 event synchronously"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(test_b92_event())
        loop.close()
        print("✅ B92 test completed successfully!")
    except Exception as e:
        print(f"❌ B92 test failed: {e}")

if __name__ == "__main__":
    test_b92_sync()
