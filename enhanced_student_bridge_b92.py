# enhanced_student_bridge_b92.py
# ===================================
# Bridge for using StudentB92Host implementation from student_b92_impl.py
# Preserves all features: qubit sending, receiving, sifting, error estimation
# Enhanced version - supports any host names

import random
import json

# Import student's actual B92 implementation
from student_b92_impl import StudentB92Host

# Helper functions for quantum operations (kept for compatibility)
def prepare_b92_quantum_state(bit):
    """Prepare a B92 quantum state (used internally by fallback or testing)"""
    if bit == 0:
        return '|0⟩'
    elif bit == 1:
        return '|+⟩'
    else:
        raise ValueError("Bit must be 0 or 1")

def measure_b92_quantum_state(quantum_state, measurement_basis):
    """Measure a B92 quantum state in a given basis (used internally)"""
    if measurement_basis == "Z":
        if quantum_state == '|0⟩':
            return 0
        elif quantum_state == '|+⟩':
            return random.randint(0, 1)  # Random outcome
        else:
            return random.randint(0, 1)
    elif measurement_basis == "X":
        if quantum_state == '|+⟩':
            return 0
        elif quantum_state == '|0⟩':
            return random.randint(0, 1)  # Random outcome
        else:
            return random.randint(0, 1)

# =================================================
# Enhanced bridge class using student's actual B92 code
# =================================================
class EnhancedStudentB92ImplementationBridge:
    """Directly uses StudentB92Host from student_b92_impl.py with flexible names"""
    
    def __init__(self, student_alice=None, student_bob=None, alice_name="Alice", bob_name="Bob"):
        # Store the actual names for flexible logging
        self.alice_name = alice_name
        self.bob_name = bob_name
        
        if student_alice is None:
            self.student_alice = StudentB92Host(self.alice_name)
        else:
            self.student_alice = student_alice
            self.alice_name = student_alice.name  # Get actual name from student host
            
        if student_bob is None:
            self.student_bob = StudentB92Host(self.bob_name)
        else:
            self.student_bob = student_bob
            self.bob_name = student_bob.name  # Get actual name from student host
            
        self.host = None
        self.b92_phase = "idle"
        self.bits_received = 0
        self.expected_bits = 0
    
    def b92_send_qubits(self, num_qubits):
        """Send qubits using student's B92 implementation directly"""
        if self.host is None:
            return False
            
        self.b92_phase = "sending"
        self.expected_bits = num_qubits
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO, 
                                   num_qubits=num_qubits, 
                                   protocol="B92",
                                   message=f"STUDENT B92: Starting with {num_qubits} qubits using student code",
                                   student_implementation="StudentB92Host")
        
        # Call student's B92 method
        encoded_qubits = self.student_alice.b92_send_qubits(num_qubits)
        
        # Store Alice's data on host
        self.host.sent_bits = list(self.student_alice.sent_bits)
        self.host.prepared_qubits = list(self.student_alice.qubits)
        self.host.basis_choices = list(self.student_alice.sent_bits)  # For B92, sent bits are the basis choices
        
        # Send through quantum channel
        channel = self.host.get_channel()
        if channel is None:
            return False
        
        for q in encoded_qubits:
            self.host.send_qubit(q, channel)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.DATA_SENT, 
                                   qubits_sent=len(encoded_qubits),
                                   message=f"STUDENT B92: Sent {len(encoded_qubits)} qubits")
        
        # Trigger sifting process
        if self.host and hasattr(self.host, 'send_bases_for_sifting'):
            self.host.send_bases_for_sifting()
        
        return True
    
    def process_received_qbit(self, qbit, from_channel):
        """Measure received qubit using student's B92 implementation"""
        if self.host is None:
            return False
            
        if self.b92_phase == "idle":
            self.b92_phase = "receiving"
            
        self.bits_received += 1
        result = self.student_bob.b92_process_received_qbit(qbit, from_channel)
        
        self.host.received_measurements = list(self.student_bob.received_measurements)
        self.host.measurement_outcomes = list(self.student_bob.measurement_outcomes)
        self.host.received_bases = list(self.student_bob.received_bases)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.DATA_RECEIVED,
                                   message=f"STUDENT {self.bob_name}: Received qubit {self.bits_received}/{self.expected_bits}",
                                   qubits_received=self.bits_received,
                                   total_expected=self.expected_bits)
        
        if self.bits_received >= self.expected_bits:
            self.b92_phase = "ready_for_sifting"
        
        return result
    
    def b92_process_received_qbit(self, qbit, from_channel):
        """Alias for process_received_qbit to match validation requirements"""
        return self.process_received_qbit(qbit, from_channel)
    
    def b92_sifting(self, sent_bits=None, received_measurements=None):
        """Perform B92 sifting using student's implementation"""
        if self.host is None:
            return False
        
        self.b92_phase = "sifting"
        
        # Use provided data or get from student implementations
        if sent_bits is None:
            sent_bits = self.student_alice.sent_bits
        if received_measurements is None:
            received_measurements = self.student_bob.received_measurements
        
        sifted_alice, sifted_bob = self.student_alice.b92_sifting(sent_bits, received_measurements)
        
        self.host.sifted_key = list(self.student_alice.sifted_key)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            efficiency = (len(sifted_bob) / len(received_measurements) * 100) if received_measurements else 0
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT {self.bob_name}: Found {len(sifted_bob)} sifted bits ({efficiency:.1f}% efficiency)",
                                   shared_bases=len(sifted_bob),
                                   efficiency=efficiency)
        
        self.host.send_classical_data({'type': 'sifted_key', 'data': self.host.sifted_key})
        return sifted_alice, sifted_bob
    
    def b92_estimate_error_rate(self, sample_positions=None, reference_bits=None):
        """Compute error rate using student's B92 implementation"""
        if self.host is None:
            return False
        
        self.b92_phase = "error_checking"
        
        # Use provided data or get from student implementations
        if sample_positions is None or reference_bits is None:
            # Use sifted key for error estimation
            sifted_key = self.student_alice.sifted_key
            if sifted_key:
                sample_positions = list(range(len(sifted_key)))
                reference_bits = sifted_key
            else:
                sample_positions, reference_bits = [], []
        
        error_rate = self.student_bob.b92_estimate_error_rate(sample_positions, reference_bits)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT {self.bob_name}: Error rate {error_rate:.1%}",
                                   error_rate=error_rate)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.SHARED_KEY_GENERATED,
                                   message="B92 QKD protocol completed successfully using student code",
                                   error_rate=error_rate,
                                   shared_bases=len(self.host.sifted_key))
        
        self.host.send_classical_data({'type': 'complete'})
        self.b92_phase = "complete"
        
        return error_rate
    
    def update_sifted_key(self, sifted_key):
        """Update sifted key - called by Alice"""
        if self.host is None:
            return False
        
        self.host.sifted_key = sifted_key
        
        if self.host and hasattr(self.host, 'update_sifted_key'):
            self.host.update_sifted_key(sifted_key)
        
        return True
    
    def b92_complete(self):
        """B92 protocol completion"""
        if self.host is None:
            return False
        
        self.b92_phase = "complete"
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.SHARED_KEY_GENERATED,
                                   message="B92 QKD protocol completed successfully using student code",
                                   protocol="B92")
        
        return True

# ==========================================
# Factory function for easy setup
# ==========================================
def create_b92_bridge(host1_name, host2_name):
    """Create a B92 bridge with custom host names"""
    student_host1 = StudentB92Host(host1_name)
    student_host2 = StudentB92Host(host2_name)
    
    bridge = EnhancedStudentB92ImplementationBridge(
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
    """Wrapper that uses EnhancedStudentB92ImplementationBridge with flexible names"""
    
    def __init__(self, host, host1_name="Alice", host2_name="Bob"):
        self.host = host
        self._bridge = create_b92_bridge(host1_name, host2_name)
        self._bridge.host = host
    
    def set_host(self, host):
        self.host = host
        self._bridge.host = host
    
    def b92_send_qubits(self, num_qubits):
        return self._bridge.b92_send_qubits(num_qubits)
    
    def process_received_qbit(self, qbit, from_channel):
        return self._bridge.process_received_qbit(qbit, from_channel)
    
    def b92_sifting(self, sent_bits=None, received_measurements=None):
        return self._bridge.b92_sifting(sent_bits, received_measurements)
    
    def b92_estimate_error_rate(self, sample_positions=None, reference_bits=None):
        return self._bridge.b92_estimate_error_rate(sample_positions, reference_bits)
