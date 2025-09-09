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
        
        # Send update event
        self._send_update("student_b92_send_start", {
            "message": f"Student {self.alice_name}: Starting B92 qubit preparation",
            "qubits": num_qubits,
            "protocol": "B92"
        })
        
        # Use student's B92 implementation
        result = self.student_alice.b92_send_qubits(num_qubits)
        
        # Capture actual data from student implementation
        sent_bits = getattr(self.student_alice, 'sent_bits', [])
        qubits_prepared = getattr(self.student_alice, 'qubits', [])
        
        # Send through quantum channel (like BB84 bridge does)
        if self.host and hasattr(self.host, 'get_channel'):
            channel = self.host.get_channel()
            if channel and qubits_prepared:
                for q in qubits_prepared:
                    self.host.send_qubit(q, channel)
                print(f"📤 {self.alice_name}: Sent {len(qubits_prepared)} B92 qubits through quantum channel")
        
        # Send complete event with actual numerical data
        self._send_update("student_b92_send_complete", {
            "message": f"Student {self.alice_name}: B92 qubits prepared and sent successfully",
            "qubits": num_qubits,
            "actual_qubits_sent": len(qubits_prepared),
            "sent_bits": sent_bits[:10] if len(sent_bits) > 10 else sent_bits,  # Show first 10 bits
            "qubit_states": qubits_prepared[:5] if len(qubits_prepared) > 5 else qubits_prepared,  # Show first 5 qubit states
            "protocol": "B92"
        })
        
        # Trigger sifting process (like BB84 triggers reconciliation)
        if self.host and hasattr(self.host, 'send_bases_for_sifting'):
            print(f"🔹 {self.alice_name}: Triggering sifting process...")
            self.host.send_bases_for_sifting()
        else:
            print(f"⚠️ {self.alice_name}: Cannot trigger sifting - host={self.host}, has_method={hasattr(self.host, 'send_bases_for_sifting') if self.host else False}")
        
        return result

    def b92_process_received_qbit(self, qubit_data, from_channel=None):
        """Bob's B92 implementation: Process received qubit"""
        print(f"🔹 {self.bob_name}: Processing received B92 qubit from {from_channel}...")
        
        # Get current measurement count before processing
        measurements_before = len(getattr(self.student_bob, 'received_measurements', []))
        print(f"🔍 {self.bob_name}: Measurements before: {measurements_before}")
        
        # Send update event
        self._send_update("student_b92_measure_start", {
            "message": f"Student {self.bob_name}: Starting B92 qubit measurement [b92_process_received_qbit]",
            "protocol": "B92"
        })
        
        # Use student's B92 implementation
        result = self.student_bob.b92_process_received_qbit(qubit_data)
        
        # Capture actual measurement data after processing
        measurements_after = len(getattr(self.student_bob, 'received_measurements', []))
        measurement_outcomes = getattr(self.student_bob, 'measurement_outcomes', [])
        received_bases = getattr(self.student_bob, 'received_bases', [])
        
        print(f"🔍 {self.bob_name}: Measurements after: {measurements_after}")
        print(f"🔍 {self.bob_name}: Measurement outcomes: {measurement_outcomes}")
        print(f"🔍 {self.bob_name}: Received bases: {received_bases}")
        
        # Get the latest measurement if available
        latest_measurement = None
        if measurements_after > measurements_before and self.student_bob.received_measurements:
            latest_measurement = self.student_bob.received_measurements[-1]
            print(f"🔍 {self.bob_name}: Latest measurement: {latest_measurement}")
        
        # Send update event with actual measurement data
        self._send_update("student_b92_measure_complete", {
            "message": f"Student {self.bob_name}: B92 qubit measurement completed [b92_process_received_qbit]",
            "total_measurements": measurements_after,
            "latest_measurement": latest_measurement,
            "measurement_outcomes": measurement_outcomes[-5:] if len(measurement_outcomes) > 5 else measurement_outcomes,  # Show last 5 outcomes
            "received_bases": received_bases[-5:] if len(received_bases) > 5 else received_bases,  # Show last 5 bases
            "protocol": "B92"
        })
        
        return result

    def b92_sifting(self, sent_bits=None, received_measurements=None):
        """B92 sifting process"""
        print(f"🔹 {self.alice_name} & {self.bob_name}: Starting B92 sifting...")
        
        # Send update event
        self._send_update("student_b92_reconcile_start", {
            "message": f"Student {self.alice_name}: Starting B92 reconciliation process [b92_sifting]",
            "protocol": "B92"
        })
        
        # Use student's B92 implementation
        if sent_bits is not None and received_measurements is not None:
            result = self.student_alice.b92_sifting(sent_bits, received_measurements)
        else:
            # Use data from student implementations
            alice_sent_bits = getattr(self.student_alice, 'sent_bits', [])
            bob_measurements = getattr(self.student_bob, 'received_measurements', [])
            result = self.student_alice.b92_sifting(alice_sent_bits, bob_measurements)
        
        # Capture actual sifting results
        sifted_key = getattr(self.student_alice, 'sifted_key', [])
        alice_sent_bits = getattr(self.student_alice, 'sent_bits', [])
        bob_measurements = getattr(self.student_bob, 'received_measurements', [])
        
        print(f"🔍 {self.alice_name}: Sifted key: {sifted_key}")
        print(f"🔍 {self.alice_name}: Alice sent bits: {alice_sent_bits}")
        print(f"🔍 {self.bob_name}: Bob measurements: {bob_measurements}")
        
        # Calculate sifting efficiency
        total_measurements = len(bob_measurements)
        sifted_length = len(sifted_key)
        efficiency = (sifted_length / total_measurements * 100) if total_measurements > 0 else 0
        
        print(f"🔍 Sifting stats: {sifted_length} sifted bits from {total_measurements} measurements ({efficiency:.1f}% efficiency)")
        
        # Send update event with actual sifting data
        self._send_update("student_b92_reconcile_complete", {
            "message": f"Student {self.alice_name}: B92 reconciliation completed [b92_sifting]",
            "total_measurements": total_measurements,
            "sifted_key_length": sifted_length,
            "sifting_efficiency": round(efficiency, 2),
            "sifted_key_sample": sifted_key[:10] if len(sifted_key) > 10 else sifted_key,  # Show first 10 bits of sifted key
            "protocol": "B92"
        })
        
        return result
    
    def b92_estimate_error_rate(self, sample_positions=None, reference_bits=None):
        """B92 error rate estimation"""
        print(f"🔹 {self.alice_name} & {self.bob_name}: Estimating B92 error rate...")
        
        # Send update event
        self._send_update("student_b92_error_start", {
            "message": f"Student {self.alice_name}: Starting B92 error rate estimation [b92_estimate_error_rate]",
            "protocol": "B92"
        })
        
        # Use student's B92 implementation
        if sample_positions is not None and reference_bits is not None:
            result = self.student_alice.b92_estimate_error_rate(sample_positions, reference_bits)
        else:
            result = self.student_alice.b92_estimate_error_rate()
        
        # Store the error rate for completion method
        self._last_error_rate = result
        
        # Capture actual error estimation data
        sifted_key = getattr(self.student_alice, 'sifted_key', [])
        measurement_outcomes = getattr(self.student_bob, 'measurement_outcomes', [])
        
        print(f"🔍 {self.alice_name}: Error rate result: {result}")
        print(f"🔍 {self.alice_name}: Sample positions: {sample_positions}")
        print(f"🔍 {self.alice_name}: Reference bits: {reference_bits}")
        print(f"🔍 {self.alice_name}: Sifted key: {sifted_key}")
        
        # Calculate additional statistics
        error_rate_percentage = result * 100
        total_bits_compared = len(sample_positions) if sample_positions else len(sifted_key)
        errors_found = int(result * total_bits_compared) if total_bits_compared > 0 else 0
        
        print(f"🔍 Error estimation stats: {error_rate_percentage:.1f}% error rate, {errors_found}/{total_bits_compared} errors")
        
        # Send update event with actual error estimation data
        self._send_update("student_b92_error_complete", {
            "message": f"Student {self.alice_name}: B92 error rate estimation completed [b92_estimate_error_rate]",
            "error_rate": result,
            "error_rate_percentage": round(error_rate_percentage, 2),
            "total_bits_compared": total_bits_compared,
            "errors_found": errors_found,
            "sample_positions": sample_positions[:10] if sample_positions and len(sample_positions) > 10 else sample_positions,
            "reference_bits": reference_bits[:10] if reference_bits and len(reference_bits) > 10 else reference_bits,
            "protocol": "B92"
        })
        
        return result

    def b92_complete(self):
        """B92 protocol completion"""
        print(f"🔹 {self.alice_name} & {self.bob_name}: B92 protocol completed!")
        
        # Capture final statistics from student implementations
        alice_sent_bits = getattr(self.student_alice, 'sent_bits', [])
        bob_measurements = getattr(self.student_bob, 'received_measurements', [])
        sifted_key = getattr(self.student_alice, 'sifted_key', [])
        measurement_outcomes = getattr(self.student_bob, 'measurement_outcomes', [])
        
        # Calculate final statistics
        total_qubits_sent = len(alice_sent_bits)
        total_measurements = len(bob_measurements)
        final_key_length = len(sifted_key)
        sifting_efficiency = (final_key_length / total_measurements * 100) if total_measurements > 0 else 0
        
        # Get final error rate (if available from last estimation)
        final_error_rate = 0.0  # Default value
        if hasattr(self, '_last_error_rate'):
            final_error_rate = self._last_error_rate
        
        # Send completion event with actual final statistics
        self._send_update("student_b92_complete", {
            "message": f"Student B92 Implementation Complete! All methods executed successfully: b92_send_qubits(), b92_process_received_qbit(), b92_sifting(), b92_estimate_error_rate()",
            "protocol": "B92",
            "total_qubits_sent": total_qubits_sent,
            "total_measurements": total_measurements,
            "final_key_length": final_key_length,
            "sifting_efficiency": round(sifting_efficiency, 2),
            "final_error_rate": final_error_rate,
            "final_error_rate_percentage": round(final_error_rate * 100, 2),
            "sifted_key_sample": sifted_key[:10] if len(sifted_key) > 10 else sifted_key
        })
        
        return True

    def _send_update(self, event_type, data):
        """Send update event using the same pattern as working BB84 bridge"""
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            
            # Use the same event pattern as working BB84 bridge
            if event_type == "student_b92_send_start":
                self.host._send_update(SimulationEventType.INFO, 
                                     num_qubits=data.get("qubits", 0), 
                                     protocol="B92",
                                     message=data.get("message", "B92 Starting"),
                                     student_implementation="StudentB92Host")
            elif event_type == "student_b92_send_complete":
                self.host._send_update(SimulationEventType.DATA_SENT, 
                                     qubits_sent=data.get("actual_qubits_sent", 0),
                                     message=data.get("message", "B92 Sent"))
            elif event_type == "student_b92_measure_complete":
                self.host._send_update(SimulationEventType.DATA_RECEIVED,
                                     message=data.get("message", "B92 Received"),
                                     qubits_received=data.get("total_measurements", 0))
            elif event_type == "student_b92_reconcile_complete":
                self.host._send_update(SimulationEventType.INFO,
                                     message=data.get("message", "B92 Reconciled"),
                                     shared_bases=data.get("sifted_key_length", 0),
                                     efficiency=data.get("sifting_efficiency", 0))
            elif event_type == "student_b92_error_complete":
                self.host._send_update(SimulationEventType.INFO,
                                     message=data.get("message", "B92 Error Rate"),
                                     error_rate=data.get("error_rate", 0))
            elif event_type == "student_b92_complete":
                self.host._send_update(SimulationEventType.SHARED_KEY_GENERATED,
                                     message=data.get("message", "B92 Complete"),
                                     error_rate=data.get("final_error_rate", 0),
                                     shared_bases=data.get("final_key_length", 0))
        else:
            print(f"⚠️ B92 Bridge: No host or _send_update method available")

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
