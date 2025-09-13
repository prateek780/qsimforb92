#!/usr/bin/env python3
"""
Test B92 simulation flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_student_bridge_b92 import EnhancedStudentImplementationBridgeB92

def test_b92_simulation_flow():
    """Test B92 simulation flow"""
    print("Testing B92 simulation flow...")
    
    # Create a mock host
    class MockHost:
        def __init__(self):
            self.name = "TestHost"
            self._send_update_calls = []
            self._qubit_count = 0
            
        def _send_update(self, event_type, message, **kwargs):
            print(f"MockHost._send_update called:")
            print(f"  Event Type: {event_type}")
            print(f"  Message: {message}")
            print(f"  Kwargs: {kwargs}")
            self._send_update_calls.append((event_type, message, kwargs))
            
        def get_channel(self):
            return "mock_channel"
            
        def send_qubit(self, qubit, channel):
            print(f"MockHost.send_qubit called with: {qubit}")
            self._qubit_count += 1
            return True
            
        def send_bases_for_sifting(self):
            print("MockHost.send_bases_for_sifting called")
    
    # Create bridge and mock host
    bridge = EnhancedStudentImplementationBridgeB92()
    mock_host = MockHost()
    bridge.host = mock_host
    
    print("\n=== Testing complete B92 flow ===")
    
    # Step 1: Send qubits (Alice)
    print("\n--- Step 1: Alice sends qubits ---")
    try:
        result = bridge.b92_send_qubits(5)
        print(f"b92_send_qubits result: {result}")
        print(f"Expected bits: {bridge.expected_bits}")
        print(f"QKD phase: {bridge.qkd_phase}")
        print(f"Alice sent_bits: {bridge.student_alice.sent_bits}")
    except Exception as e:
        print(f"Error in b92_send_qubits: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 2: Simulate Bob receiving qubits
    print("\n--- Step 2: Bob receives qubits ---")
    try:
        # Simulate receiving qubits one by one
        for i in range(5):
            result = bridge.process_received_qbit(f"qubit_{i}", "mock_channel")
            print(f"process_received_qbit result {i+1}: {result}")
            print(f"Bits received: {bridge.bits_received}/{bridge.expected_bits}")
            print(f"Bob received_measurements: {bridge.student_bob.received_measurements}")
    except Exception as e:
        print(f"Error in process_received_qbit: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 3: Sifting
    print("\n--- Step 3: Sifting ---")
    try:
        result = bridge.b92_sifting([])
        print(f"b92_sifting result: {result}")
    except Exception as e:
        print(f"Error in b92_sifting: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 4: Error estimation
    print("\n--- Step 4: Error estimation ---")
    try:
        result = bridge.b92_estimate_error_rate([])
        print(f"b92_estimate_error_rate result: {result}")
    except Exception as e:
        print(f"Error in b92_estimate_error_rate: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\nTotal logging calls made: {len(mock_host._send_update_calls)}")
    print(f"Total qubits sent: {mock_host._qubit_count}")

if __name__ == "__main__":
    test_b92_simulation_flow()
