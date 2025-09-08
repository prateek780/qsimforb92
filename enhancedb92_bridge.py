# enhancedb92_bridge.py
# ===================================
# Bridge for using StudentB92Host implementation from student_b92_impl.py
# Connects B92 student implementation to the simulation system

import random
import json

# Import student's actual B92 implementation
from student_b92_impl import StudentB92Host

# =================================================
# B92 Bridge class using student's actual code
# =================================================
class EnhancedB92Bridge:
    """Directly uses StudentB92Host from student_b92_impl.py"""
    
    def __init__(self, student_alice=None, student_bob=None, alice_name="Alice", bob_name="Bob"):
        # Store the actual names for flexible logging
        self.alice_name = alice_name
        self.bob_name = bob_name
        
        if student_alice is None:
            self.student_alice = StudentB92Host(self.alice_name)
        else:
            self.student_alice = student_alice
            
        if student_bob is None:
            self.student_bob = StudentB92Host(self.bob_name)
        else:
            self.student_bob = student_bob
        
        # Store reference to the host for updates
        self.host = None
        
        print(f"🔹 B92 Bridge initialized: {self.alice_name} <-> {self.bob_name}")

    def b92_send_qubits(self, num_qubits):
        """Alice's B92 implementation: Prepare and send qubits"""
        print(f"🔹 {self.alice_name}: Starting B92 qubit preparation...")
        
        # Use student's B92 implementation
        result = self.student_alice.b92_send_qubits(num_qubits)
        
        # Send update event
        self._send_update("student_b92_send_start", {
            "message": f"Student {self.alice_name}: Starting B92 qubit preparation",
            "qubits": num_qubits,
            "protocol": "B92"
        })
        
        self._send_update("student_b92_send_complete", {
            "message": f"Student {self.alice_name}: B92 qubits prepared successfully",
            "qubits": num_qubits,
            "protocol": "B92"
        })
        
        return result

    def b92_process_received_qbit(self, qubit_data):
        """Bob's B92 implementation: Process received qubit"""
        print(f"🔹 {self.bob_name}: Processing received B92 qubit...")
        
        # Use student's B92 implementation
        result = self.student_bob.b92_process_received_qbit(qubit_data)
        
        # Send update event
        self._send_update("student_b92_measure_start", {
            "message": f"Student {self.bob_name}: Starting B92 qubit measurement",
            "protocol": "B92"
        })
        
        self._send_update("student_b92_measure_complete", {
            "message": f"Student {self.bob_name}: B92 qubit measurement completed",
            "protocol": "B92"
        })
        
        return result

    def b92_sifting(self):
        """B92 sifting process"""
        print(f"🔹 {self.alice_name} & {self.bob_name}: Starting B92 sifting...")
        
        # Use student's B92 implementation
        result = self.student_alice.b92_sifting()
        
        # Send update event
        self._send_update("student_b92_sift_start", {
            "message": f"Student {self.alice_name}: Starting B92 sifting process",
            "protocol": "B92"
        })
        
        self._send_update("student_b92_sift_complete", {
            "message": f"Student {self.alice_name}: B92 sifting completed",
            "protocol": "B92"
        })
        
        return result

    def b92_estimate_error_rate(self):
        """B92 error rate estimation"""
        print(f"🔹 {self.alice_name} & {self.bob_name}: Estimating B92 error rate...")
        
        # Use student's B92 implementation
        result = self.student_alice.b92_estimate_error_rate()
        
        # Send update event
        self._send_update("student_b92_error_start", {
            "message": f"Student {self.alice_name}: Starting B92 error rate estimation",
            "protocol": "B92"
        })
        
        self._send_update("student_b92_error_complete", {
            "message": f"Student {self.alice_name}: B92 error rate estimation completed",
            "error_rate": result,
            "protocol": "B92"
        })
        
        return result

    def _send_update(self, event_type, data):
        """Send update event to the B92 simulation system"""
        try:
            # Import B92 event system
            from core.world_b92 import b92_event_manager
            from core.event_b92 import B92EventType
            
            # Convert event type to B92 event type
            b92_event_type = None
            if event_type == "student_b92_send_start":
                b92_event_type = B92EventType.B92_STUDENT_SEND_START
            elif event_type == "student_b92_send_complete":
                b92_event_type = B92EventType.B92_STUDENT_SEND_COMPLETE
            elif event_type == "student_b92_measure_start":
                b92_event_type = B92EventType.B92_STUDENT_MEASURE_START
            elif event_type == "student_b92_measure_complete":
                b92_event_type = B92EventType.B92_STUDENT_MEASURE_COMPLETE
            elif event_type == "student_b92_reconcile_start":
                b92_event_type = B92EventType.B92_STUDENT_RECONCILE_START
            elif event_type == "student_b92_reconcile_complete":
                b92_event_type = B92EventType.B92_STUDENT_RECONCILE_COMPLETE
            elif event_type == "student_b92_error_start":
                b92_event_type = B92EventType.B92_STUDENT_ERROR_START
            elif event_type == "student_b92_error_complete":
                b92_event_type = B92EventType.B92_STUDENT_ERROR_COMPLETE
            elif event_type == "student_b92_ready":
                b92_event_type = B92EventType.B92_STUDENT_READY
            elif event_type == "student_b92_trigger":
                b92_event_type = B92EventType.B92_STUDENT_TRIGGER
            elif event_type == "student_b92_complete":
                b92_event_type = B92EventType.B92_STUDENT_COMPLETE
            
            if b92_event_type and self.host:
                # Emit B92 event
                b92_event_manager.emit_b92_student_event(
                    b92_event_type, 
                    self.host, 
                    data.get("message", f"B92 {event_type}"),
                    **data
                )
                print(f"🔹 B92 Event emitted: {event_type}")
            else:
                print(f"⚠️ Unknown B92 event type: {event_type}")
                
        except Exception as e:
            print(f"❌ Error emitting B92 event: {e}")
            # Fallback to original method if available
            if self.host and hasattr(self.host, 'emit_event'):
                self.host.emit_event(event_type, data)

    # BB84 compatibility methods (for simulation integration)
    def bb84_send_qubits(self, num_qubits):
        """BB84 compatibility: calls B92 send qubits"""
        return self.b92_send_qubits(num_qubits)

    def process_received_qbit(self, qubit_data):
        """BB84 compatibility: calls B92 process received qubit"""
        return self.b92_process_received_qbit(qubit_data)

    def bb84_reconcile_bases(self):
        """BB84 compatibility: calls B92 sifting"""
        return self.b92_sifting()

    def bb84_estimate_error_rate(self):
        """BB84 compatibility: calls B92 error estimation"""
        return self.b92_estimate_error_rate()

    def get_sifted_key(self):
        """Get the sifted key from Alice"""
        return getattr(self.student_alice, 'sifted_key', [])

    def get_prepared_bits(self):
        """Get the prepared bits from Alice"""
        return getattr(self.student_alice, 'sent_bits', [])

    def get_measurement_outcomes(self):
        """Get the measurement outcomes from Bob"""
        return getattr(self.student_bob, 'received_measurements', [])

# ==========================================
# Factory function for easy setup
# ==========================================
def create_b92_bridge(host1_name, host2_name):
    """Create a B92 bridge with custom host names"""
    student_host1 = StudentB92Host(host1_name)
    student_host2 = StudentB92Host(host2_name)
    
    bridge = EnhancedB92Bridge(
        student_alice=student_host1,
        student_bob=student_host2,
        alice_name=host1_name,
        bob_name=host2_name
    )
    return bridge

# ==========================================
# Wrapper to attach bridge to host
# ==========================================
class StudentB92ImplementationBridge:
    """Wrapper that uses EnhancedB92Bridge"""
    
    def __init__(self, host, host1_name="Alice", host2_name="Bob"):
        self.host = host
        self._bridge = create_b92_bridge(host1_name, host2_name)
        self._bridge.host = host
    
    def set_host(self, host):
        self.host = host
        self._bridge.host = host
    
    def __getattr__(self, name):
        """Delegate all other methods to the bridge"""
        return getattr(self._bridge, name)
