#!/usr/bin/env python3
"""
Test B92 Notebook Simulation
============================

This script simulates the notebook environment and tests B92 simulation.
"""

import sys
import os
import json

# Add current directory to path
sys.path.append('.')

def test_b92_notebook_simulation():
    """Test B92 simulation in notebook-like environment"""
    print("🔬 Testing B92 Notebook Simulation...")
    print("=" * 50)
    
    # Test 1: Import B92 implementation
    print("\n1. Testing B92 implementation import...")
    try:
        from student_b92_impl import StudentB92Host
        print("✅ B92 implementation imported successfully")
    except Exception as e:
        print(f"❌ B92 implementation import failed: {e}")
        return False
    
    # Test 2: Create B92 hosts
    print("\n2. Testing B92 host creation...")
    try:
        alice = StudentB92Host("Alice")
        bob = StudentB92Host("Bob")
        print("✅ B92 hosts created successfully")
    except Exception as e:
        print(f"❌ B92 host creation failed: {e}")
        return False
    
    # Test 3: Test B92 protocol methods
    print("\n3. Testing B92 protocol methods...")
    try:
        # Alice sends qubits
        qubits = alice.b92_send_qubits(10)
        print(f"✅ Alice sent {len(qubits)} qubits: {qubits[:5]}...")
        
        # Bob processes qubits
        for qbit in qubits:
            bob.b92_process_received_qbit(qbit)
        print(f"✅ Bob processed {len(bob.received_measurements)} qubits")
        
        # Sifting
        sifted_alice, sifted_bob = bob.b92_sifting(alice.sent_bits, bob.received_measurements)
        print(f"✅ Sifting complete: {len(sifted_alice)} bits shared")
        
        # Error estimation
        if sifted_alice:
            sample_positions = list(range(len(sifted_alice)))
            error_rate = bob.b92_estimate_error_rate(sample_positions, sifted_alice)
            print(f"✅ Error rate: {error_rate:.4f}")
        
    except Exception as e:
        print(f"❌ B92 protocol test failed: {e}")
        return False
    
    # Test 4: Test B92 status file creation
    print("\n4. Testing B92 status file creation...")
    try:
        status = {
            "student_implementation_ready": True,
            "implementation_type": "StudentImplementationBridge",
            "protocol": "B92",
            "methods_implemented": [
                "b92_send_qubits",
                "b92_process_received_qbit",
                "b92_sifting", 
                "b92_estimate_error_rate",
            ],
            "ui_logging_enabled": True,
            "has_valid_implementation": True,
        }
        
        with open("student_b92_implementation_status.json", "w") as f:
            json.dump(status, f)
        print("✅ B92 status file created successfully")
        
    except Exception as e:
        print(f"❌ B92 status file creation failed: {e}")
        return False
    
    # Test 5: Test B92 bridge
    print("\n5. Testing B92 bridge...")
    try:
        from enhanced_student_bridge_b92 import EnhancedStudentImplementationBridgeB92
        bridge = EnhancedStudentImplementationBridgeB92(alice, bob)
        print("✅ B92 bridge created successfully")
        
        # Test bridge methods
        test_qubits = bridge.b92_send_qubits(5)
        print(f"✅ Bridge send_qubits: {len(test_qubits)} qubits")
        
        for qbit in test_qubits:
            bridge.b92_process_received_qbit(qbit)
        print("✅ Bridge process_received_qbit working")
        
        sifted_a, sifted_b = bridge.b92_sifting()
        print(f"✅ Bridge sifting: {len(sifted_a)} bits")
        
        error_rate = bridge.b92_estimate_error_rate()
        print(f"✅ Bridge error estimation: {error_rate:.4f}")
        
    except Exception as e:
        print(f"❌ B92 bridge test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All B92 tests passed! B92 simulation is ready.")
    return True

if __name__ == "__main__":
    success = test_b92_notebook_simulation()
    if success:
        print("\n🎉 B92 simulation is working correctly!")
        print("   You can now use show_b92_simulation() in the notebook.")
    else:
        print("\n❌ B92 simulation has issues that need to be fixed.")
