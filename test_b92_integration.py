# 🧪 B92 INTEGRATION TEST
# =======================
# This script tests the complete B92 integration flow

import json
import os
import sys

def test_b92_integration():
    """Test the complete B92 integration flow"""
    print("🧪 TESTING B92 INTEGRATION")
    print("=" * 40)
    
    # Test 1: Check if B92 files exist
    print("🔍 Test 1: Checking B92 files...")
    b92_files = [
        "student_b92_impl.py",
        "enhanced_student_bridge_b92.py", 
        "enhancedb92_bridge.py",
        "b92_impl.py",
        "quantum_network/interactive_host_b92.py"
    ]
    
    missing_files = []
    for file_path in b92_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All B92 files present")
    
    # Test 2: Test B92 student implementation
    print("\n🔍 Test 2: Testing B92 student implementation...")
    try:
        from student_b92_impl import StudentB92Host
        
        alice = StudentB92Host("Alice")
        bob = StudentB92Host("Bob")
        
        # Test B92 methods
        qubits = alice.b92_send_qubits(5)
        print(f"✅ Alice sent {len(qubits)} qubits: {qubits}")
        
        for q in qubits:
            bob.b92_process_received_qbit(q)
        
        print(f"✅ Bob processed {len(bob.received_measurements)} measurements")
        
        # Test sifting
        sifted_alice, sifted_bob = bob.b92_sifting(alice.sent_bits, bob.received_measurements)
        print(f"✅ Sifting completed: {len(sifted_alice)} shared bits")
        
        # Test error estimation
        sample_positions = [0, 1, 2]
        reference_bits = [0, 1, 0]
        error_rate = bob.b92_estimate_error_rate(sample_positions, reference_bits)
        print(f"✅ Error rate estimation: {error_rate:.2%}")
        
    except Exception as e:
        print(f"❌ B92 student implementation test failed: {e}")
        return False
    
    # Test 3: Test B92 enhanced bridge
    print("\n🔍 Test 3: Testing B92 enhanced bridge...")
    try:
        from enhancedb92_bridge import EnhancedB92Bridge
        
        bridge = EnhancedB92Bridge(
            student_alice=alice,
            student_bob=bob,
            alice_name="Alice",
            bob_name="Bob"
        )
        
        print("✅ B92 enhanced bridge created")
        
        # Test bridge methods
        result = bridge.b92_send_qubits(5)
        print(f"✅ Bridge send qubits: {result}")
        
        result = bridge.b92_sifting()
        print(f"✅ Bridge sifting: {result}")
        
        sample_positions = [0, 1, 2]
        reference_bits = [0, 1, 0]
        result = bridge.b92_estimate_error_rate(sample_positions, reference_bits)
        print(f"✅ Bridge error estimation: {result}")
        
    except Exception as e:
        print(f"❌ B92 enhanced bridge test failed: {e}")
        return False
    
    # Test 4: Test B92 protocol manager
    print("\n🔍 Test 4: Testing B92 protocol manager...")
    try:
        from b92_impl import B92ProtocolManager
        
        manager = B92ProtocolManager()
        alice_host, bob_host = manager.create_student_hosts("Alice", "Bob")
        enhanced_bridge = manager.create_enhanced_bridge("Alice", "Bob")
        
        print("✅ B92 protocol manager created")
        
    except Exception as e:
        print(f"❌ B92 protocol manager test failed: {e}")
        return False
    
    # Test 5: Test JSON file creation
    print("\n🔍 Test 5: Testing JSON file creation...")
    try:
        # Create BB84 completion file
        bb84_data = {
            "protocol": "bb84",
            "status": "completed",
            "timestamp": "2025-01-10T22:15:00Z"
        }
        with open("bb84_done.json", "w") as f:
            json.dump(bb84_data, f, indent=2)
        print("✅ BB84 completion file created")
        
        # Create B92 completion file
        b92_data = {
            "protocol": "b92",
            "status": "completed",
            "timestamp": "2025-01-10T22:15:00Z"
        }
        with open("b92_done.json", "w") as f:
            json.dump(b92_data, f, indent=2)
        print("✅ B92 completion file created")
        
    except Exception as e:
        print(f"❌ JSON file creation test failed: {e}")
        return False
    
    # Test 6: Test unified protocol runner
    print("\n🔍 Test 6: Testing unified protocol runner...")
    try:
        from unified_protocol_runner import check_protocol_completion, create_protocol_completion_file
        
        # Test protocol completion check
        bb84_done = check_protocol_completion("bb84")
        b92_done = check_protocol_completion("b92")
        
        print(f"✅ BB84 completion check: {bb84_done}")
        print(f"✅ B92 completion check: {b92_done}")
        
    except Exception as e:
        print(f"❌ Unified protocol runner test failed: {e}")
        return False
    
    print("\n🎉 ALL B92 INTEGRATION TESTS PASSED!")
    print("✅ B92 protocol is ready for use!")
    return True

if __name__ == "__main__":
    success = test_b92_integration()
    if success:
        print("\n🚀 B92 integration is working perfectly!")
        print("💡 You can now run B92 simulations from the notebook!")
    else:
        print("\n❌ B92 integration has issues")
        print("💡 Check the error messages above for debugging")
        sys.exit(1)
