#!/usr/bin/env python3
"""
Test B92 Protocol Detection
==========================
This script tests if B92 protocol is properly detected and configured.
"""

import os
import json
from protocol_detection_utils import print_protocol_status

print("🔬 Testing B92 Protocol Detection")
print("=" * 40)

# Check current protocol
print_protocol_status()

# Check if B92 status file exists and is valid
if os.path.exists('student_b92_implementation_status.json'):
    with open('student_b92_implementation_status.json', 'r') as f:
        b92_status = json.load(f)
    
    print(f"\n📄 B92 Status File Contents:")
    print(f"   Ready: {b92_status.get('student_implementation_ready')}")
    print(f"   Protocol: {b92_status.get('protocol')}")
    print(f"   Status: {b92_status.get('status')}")
    
    if b92_status.get('student_implementation_ready'):
        print("✅ B92 is properly configured!")
    else:
        print("❌ B92 is not ready!")
else:
    print("❌ B92 status file not found!")

# Check if BB84 is disabled
if os.path.exists('student_implementation_status.json'):
    print("❌ BB84 is still active!")
else:
    print("✅ BB84 is properly disabled!")

print("\n💡 Next steps:")
print("   1. Stop the current simulation in the UI")
print("   2. Start a new simulation")
print("   3. The new simulation should use B92 nodes and show B92 logs")
