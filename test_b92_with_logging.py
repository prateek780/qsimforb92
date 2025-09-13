#!/usr/bin/env python3
"""
Test B92 Student Code with Logging
==================================

Test the B92 student implementation and create logs for the simulation UI
"""

import sys
import os
import json
import time
from datetime import datetime

# Add current directory to path
sys.path.append('.')

def test_b92_with_logging():
    """Test B92 implementation and create simulation logs"""
    print("🔬 Testing B92 Student Code with Logging...")
    print("=" * 50)
    
    try:
        # Import B92 implementation
        from student_b92_impl import StudentB92Host
        print("✅ B92 implementation imported successfully")
        
        # Create B92 hosts
        alice = StudentB92Host("Alice")
        bob = StudentB92Host("Bob")
        print("✅ B92 hosts created successfully")
        
        # Clear any existing simulation log
        try:
            with open("simulation.log", "w") as f:
                f.write("")
            print("🧹 Cleared existing simulation.log")
        except:
            pass
        
        # Test B92 protocol with logging
        print("\n📤 Testing B92 Protocol with Logging...")
        
        # Alice sends qubits
        num_qubits = 50
        print(f"🔹 Alice preparing {num_qubits} qubits...")
        qubits = alice.b92_send_qubits(num_qubits)
        
        # Log Alice's action
        log_event("B92_SEND_START", f"Alice prepared {len(qubits)} qubits", alice.name)
        
        # Bob processes qubits
        print(f"🔹 Bob measuring {len(qubits)} qubits...")
        for i, qbit in enumerate(qubits):
            bob.b92_process_received_qbit(qbit)
            if i % 10 == 0:  # Log every 10th qubit
                log_event("B92_MEASURE", f"Bob measured qubit {i+1}: {qbit}", bob.name)
        
        # Log Bob's completion
        log_event("B92_MEASURE_COMPLETE", f"Bob completed measuring {len(qubits)} qubits", bob.name)
        
        # Sifting
        print("🔹 Performing B92 sifting...")
        sifted_alice, sifted_bob = bob.b92_sifting(alice.sent_bits, bob.received_measurements)
        
        # Log sifting results
        log_event("B92_SIFTING", f"Sifting complete: {len(sifted_alice)} bits shared", "System")
        
        # Error estimation
        if sifted_alice:
            sample_positions = list(range(len(sifted_alice)))
            error_rate = bob.b92_estimate_error_rate(sample_positions, sifted_alice)
            print(f"🔹 Error rate: {error_rate:.4f}")
            
            # Log error analysis
            log_event("B92_ERROR_ANALYSIS", f"Error rate: {error_rate:.4f} ({error_rate*100:.2f}%)", "System")
        
        # Protocol statistics
        efficiency = len(sifted_alice) / num_qubits if num_qubits > 0 else 0
        print(f"🔹 Protocol efficiency: {efficiency:.4f} ({efficiency*100:.2f}%)")
        
        # Log final results
        log_event("B92_PROTOCOL_COMPLETE", f"B92 protocol completed successfully. Efficiency: {efficiency:.2f}%, Key length: {len(sifted_alice)}", "System")
        
        print("\n✅ B92 Protocol Test with Logging Complete!")
        print(f"📁 Logs written to simulation.log")
        print(f"📊 Final results:")
        print(f"   - Qubits sent: {num_qubits}")
        print(f"   - Key length: {len(sifted_alice)}")
        print(f"   - Efficiency: {efficiency:.2f}%")
        print(f"   - Error rate: {error_rate:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ B92 test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def log_event(event_type, message, node):
    """Log an event to simulation.log in the format expected by the UI"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "data": {
                "event_type": "simulation_event",
                "node": node,
                "timestamp": time.time(),
                "data": {
                    "type": "b92_student_event",
                    "stage": event_type,
                    "message": message,
                    "host": node,
                    "protocol": "B92"
                },
                "log_level": "info"
            }
        }
        
        with open("simulation.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
            
        print(f"📝 Logged: {event_type} - {message}")
        
    except Exception as e:
        print(f"⚠️ Could not log event: {e}")

if __name__ == "__main__":
    success = test_b92_with_logging()
    if success:
        print("\n🎉 B92 student code test successful!")
        print("   You can now view the logs in the simulation UI")
        print("   The logs are saved in simulation.log")
    else:
        print("\n❌ B92 student code test failed")


