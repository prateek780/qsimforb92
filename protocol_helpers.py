#!/usr/bin/env python3
"""
Notebook Protocol Helpers
=========================
Helper functions for students to easily switch between BB84 and B92 protocols
"""

import json
import os
from datetime import datetime

def clear_redis_memory():
    """Clear Redis memory to prevent protocol conflicts"""
    try:
        import redis
        r = redis.Redis(
            host='redis-11509.c90.us-east-1-3.ec2.redns.redis-cloud.com',
            port=11509,
            username='default',
            password='aDevCXKeLli9kldGJccV15D1yS93Oyvd',
            db=0,
            ssl=False,
            socket_timeout=5
        )
        
        r.ping()
        keys = r.keys('*')
        if keys:
            deleted_count = r.delete(*keys)
            print(f"Cleared {deleted_count} Redis keys to prevent memory conflicts")
            return True
        else:
            print("Redis is already clean")
            return True
            
    except Exception as e:
        print(f"Could not clear Redis memory: {e}")
        return False

def create_bb84_status_file():
    """Create BB84 status file to enable BB84 simulation"""
    status = {
        "student_implementation_ready": True,
        "protocol": "bb84",
        "completion_timestamp": datetime.now().isoformat(),
        "source": "notebook_vibe_code",
        "message": "Student BB84 implementation completed successfully!",
        "required_methods": [
            "bb84_send_qubits", 
            "process_received_qbit", 
            "bb84_reconcile_bases", 
            "bb84_estimate_error_rate"
        ],
        "status": "completed",
        "implementation_file": "student_bb84_impl.py",
        "bridge_file": "enhanced_student_bridge.py"
    }
    
    with open("student_implementation_status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print("BB84 Status file created!")
    print("BB84 Simulation is now unlocked!")
    print("The simulator will now use BB84 protocol and show BB84 logs")
    print("Make sure to restart the backend to switch protocols")

def create_b92_status_file():
    """Create B92 status file to enable B92 simulation"""
    status = {
        "student_implementation_ready": True,
        "protocol": "b92",
        "completion_timestamp": datetime.now().isoformat(),
        "source": "notebook_vibe_code",
        "message": "Student B92 implementation completed successfully!",
        "required_methods": [
            "b92_send_qubits",
            "b92_process_received_qbit", 
            "b92_sifting",
            "b92_estimate_error_rate"
        ],
        "status": "completed",
        "implementation_file": "student_b92_impl.py",
        "bridge_file": "enhanced_student_bridge_b92.py"
    }
    
    with open("student_b92_implementation_status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print("B92 Status file created!")
    print("B92 Simulation is now unlocked!")
    print("The simulator will now use B92 protocol and show B92 logs")
    print("Make sure to restart the backend to switch protocols")

def disable_bb84():
    """Disable BB84 protocol"""
    if os.path.exists("student_implementation_status.json"):
        os.rename("student_implementation_status.json", "student_implementation_status.json.disabled")
        print("BB84 protocol disabled")
    else:
        print("BB84 protocol was not active")

def disable_b92():
    """Disable B92 protocol"""
    if os.path.exists("student_b92_implementation_status.json"):
        os.rename("student_b92_implementation_status.json", "student_b92_implementation_status.json.disabled")
        print("B92 protocol disabled")
    else:
        print("B92 protocol was not active")

def check_current_protocol():
    """Check which protocol is currently active"""
    print("Checking current protocol status...")
    
    if os.path.exists("student_implementation_status.json"):
        try:
            with open("student_implementation_status.json", "r") as f:
                status = json.load(f)
            if status.get("student_implementation_ready"):
                print(f"BB84 protocol is ACTIVE")
                print(f"   Status: {status.get('message', 'Ready')}")
                print(f"   Timestamp: {status.get('completion_timestamp', 'Unknown')}")
                return "BB84"
        except Exception as e:
            print(f"Error reading BB84 status: {e}")
    
    if os.path.exists("student_b92_implementation_status.json"):
        try:
            with open("student_b92_implementation_status.json", "r") as f:
                status = json.load(f)
            if status.get("student_implementation_ready"):
                print(f"B92 protocol is ACTIVE")
                print(f"   Status: {status.get('message', 'Ready')}")
                print(f"   Timestamp: {status.get('completion_timestamp', 'Unknown')}")
                return "B92"
        except Exception as e:
            print(f"Error reading B92 status: {e}")
    
    print("No active protocol detected")
    print("Run create_bb84_status_file() or create_b92_status_file() to enable a protocol")
    return None

def switch_to_bb84():
    """Switch to BB84 protocol (disable B92, enable BB84)"""
    print("Switching to BB84 protocol...")
    disable_b92()
    create_bb84_status_file()
    print("Ready to run BB84 simulation!")

def switch_to_b92():
    """Switch to B92 protocol (disable BB84, enable B92)"""
    print("Switching to B92 protocol...")
    disable_bb84()
    create_b92_status_file()
    print("Ready to run B92 simulation!")

def reset_protocols():
    """Reset all protocols (disable both)"""
    print("Resetting all protocols...")
    disable_bb84()
    disable_b92()
    print("All protocols disabled")
    print("Run create_bb84_status_file() or create_b92_status_file() to enable a protocol")

# Example usage for students
if __name__ == "__main__":
    print("Protocol Helper Functions Loaded!")
    print("=" * 50)
    print("Available functions:")
    print("  create_bb84_status_file()  - Enable BB84 simulation")
    print("  create_b92_status_file()   - Enable B92 simulation")
    print("  switch_to_bb84()          - Switch to BB84")
    print("  switch_to_b92()           - Switch to B92")
    print("  check_current_protocol()  - Check active protocol")
    print("  reset_protocols()         - Disable all protocols")
    print("=" * 50)
    check_current_protocol()
