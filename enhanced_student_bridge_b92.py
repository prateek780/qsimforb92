# enhanced_student_bridge_b92.py
# ===================================
# Bridge for using StudentB92Host implementation from student_b92_impl.py
# Preserves all features: qubit sending, receiving, sifting, error estimation

import random
import json

# Import student's actual B92 implementation
from student_b92_impl import StudentB92Host

# Helper functions for quantum operations (kept for compatibility)
def prepare_quantum_state(bit, basis):
    """Prepare a quantum state (used internally by fallback or testing)"""
    if bit == 0:
        return '|0⟩'
    else:  # bit == 1
        return '|+⟩'

def measure_quantum_state(quantum_state, measurement_basis):
    """Measure a quantum state in a given basis (used internally)"""
    if measurement_basis == "Z":
        if quantum_state in ['|0⟩', '|0>']:
            return 0
        elif quantum_state in ['|+⟩', '|+>']:
            return random.randint(0, 1)
        else:
            return random.randint(0, 1)
    else:  # X-basis
        if quantum_state in ['|+⟩', '|+>']:
            return 0
        elif quantum_state in ['|0⟩', '|0>']:
            return random.randint(0, 1)
        else:
            return random.randint(0, 1)

# =================================================
# Enhanced bridge class using student's actual code
# =================================================
class EnhancedStudentImplementationBridgeB92:
    """Directly uses StudentB92Host from student_b92_impl.py"""
    
    def __init__(self, student_alice=None, student_bob=None):
        if student_alice is None:
            print("Creating Alice using StudentB92Host...")
            self.student_alice = StudentB92Host("Alice")
        else:
            self.student_alice = student_alice
            
        if student_bob is None:
            print("Creating Bob using StudentB92Host...")
            self.student_bob = StudentB92Host("Bob")
        else:
            self.student_bob = student_bob
            
        self.host = None
        self.qkd_phase = "idle"
        self.bits_received = 0
        self.expected_bits = 0
        
        print("✅ Enhanced B92 Bridge created using StudentB92Host!")
        print(f"   Alice type: {type(self.student_alice).__name__}")
        print(f"   Bob type: {type(self.student_bob).__name__}")
    
    def set_expected_bits(self, num_qubits):
        """Set the expected number of qubits for Bob's bridge"""
        self.expected_bits = num_qubits
        print(f"DEBUG: Set expected_bits to {self.expected_bits} for {self.host.name if self.host else 'unknown host'}")
    
    def b92_send_qubits(self, num_qubits):
        """Send qubits using student's implementation directly"""
        if self.host is None:
            print("Bridge not attached to a simulation host")
            return False
            
        self.qkd_phase = "sending"
        self.expected_bits = num_qubits
        print(f"Starting B92 protocol with {num_qubits} qubits")
        print(f"DEBUG: Set expected_bits to {self.expected_bits}")
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO, 
                                   num_qubits=num_qubits, 
                                   protocol="B92",
                                   message=f"STUDENT B92: Starting with {num_qubits} qubits using your code!",
                                   student_implementation="StudentB92Host")
        
        # Call student's method
        encoded_qubits = self.student_alice.b92_send_qubits(num_qubits)
        
        # Debug: Print Alice's data
        print(f"DEBUG: Alice sent_bits after b92_send_qubits: {self.student_alice.sent_bits}")
        print(f"DEBUG: Alice qubits prepared: {len(encoded_qubits)}")
        
        # Log individual qubit preparation
        for i, (bit, qubit) in enumerate(zip(self.student_alice.sent_bits, encoded_qubits)):
            print(f"DEBUG: Alice prepared qubit {i+1}: bit={bit} -> {qubit}")
            if self.host and hasattr(self.host, '_send_update'):
                from core.enums import SimulationEventType
                self.host._send_update(SimulationEventType.INFO,
                                       message=f"STUDENT ALICE: Prepared qubit {i+1} - bit {bit} -> {qubit} [b92_prepare_qubit]")
        
        # Store Alice's data on host
        self.host.basis_choices = list(self.student_alice.sent_bits)
        self.host.measurement_outcomes = list(self.student_alice.sent_bits)
        
        # Log detailed qubit preparation
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT ALICE data: Generated {len(self.student_alice.sent_bits)} bits and {len(self.student_alice.sent_bits)} bases")
            
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT ALICE: Prepared {len(encoded_qubits)} qubits using b92_send_qubits() [b92_send_qubits] ({len(encoded_qubits)} qubits)")
        
        # Send through quantum channel
        channel = self.host.get_channel()
        if channel is None:
            print(f"ERROR: {self.host.name} has no quantum channel")
            return False
        
        print(f"Sending {len(encoded_qubits)} qubits through quantum channel...")
        for i, q in enumerate(encoded_qubits):
            print(f"DEBUG: Sending qubit {i+1}: {q}")
            self.host.send_qubit(q, channel)
            if i % 5 == 0 or i == len(encoded_qubits) - 1:
                print(f"   Sent {i+1}/{len(encoded_qubits)} qubits")
        
        print(f"All {len(encoded_qubits)} qubits sent successfully")
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.DATA_SENT, 
                                   qubits_sent=len(encoded_qubits),
                                   message=f"STUDENT B92: Sending {len(encoded_qubits)} encoded qubits from Alice's b92_send_qubits() through quantum channel ({len(encoded_qubits)} qubits) - Sample: [|0>, |+>, |0>...]")
        
        # Trigger sifting by sending Alice's bits to Bob
        if self.host and hasattr(self.host, 'send_classical_data'):
            print(f"DEBUG: Sending Alice's bits to Bob for sifting: {self.student_alice.sent_bits}")
            self.host.send_classical_data({
                "type": "sifting",
                "data": self.student_alice.sent_bits
            })
        
        return True
    
    def process_received_qbit(self, qbit, from_channel):
        """Measure received qubit using student's implementation"""
        if self.host is None:
            print("WARNING: Bridge not attached to host")
            return False
            
        if self.qkd_phase == "idle":
            self.qkd_phase = "receiving"
            print("Started receiving qubits...")
            
        self.bits_received += 1
        print(f"DEBUG: Processing qubit {self.bits_received}/{self.expected_bits} (qkd_phase: {self.qkd_phase})")
        result = self.student_bob.b92_process_received_qbit(qbit, from_channel)
        
        # Debug: Print Bob's data after processing
        print(f"DEBUG: Bob received_measurements after processing: {self.student_bob.received_measurements}")
        print(f"DEBUG: Bob measurement_outcomes: {self.student_bob.measurement_outcomes}")
        print(f"DEBUG: Bob received_bases: {self.student_bob.received_bases}")
        
        # Log individual qubit measurement
        if self.student_bob.received_measurements:
            last_measurement = self.student_bob.received_measurements[-1]
            outcome, basis = last_measurement
            print(f"DEBUG: Bob measured qubit {self.bits_received}: {qbit} -> outcome={outcome}, basis={basis}")
            if self.host and hasattr(self.host, '_send_update'):
                from core.enums import SimulationEventType
                self.host._send_update(SimulationEventType.INFO,
                                       message=f"STUDENT BOB: Measured qubit {self.bits_received} - {qbit} -> outcome={outcome}, basis={basis} [b92_measure_qubit]")
        
        self.host.basis_choices = list(self.student_bob.received_bases)
        self.host.measurement_outcomes = list(self.student_bob.measurement_outcomes)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.DATA_RECEIVED,
                                   message=f"STUDENT BOB: Received qubit {self.bits_received}/{self.expected_bits}!",
                                   qubits_received=self.bits_received,
                                   total_expected=self.expected_bits)
        
        if self.bits_received % 10 == 0:
            print(f"   Received {self.bits_received}/{self.expected_bits} qubits")
        
        if self.bits_received >= self.expected_bits:
            print(f"Received all {self.bits_received} qubits, ready for sifting...")
            self.qkd_phase = "ready_for_sifting"
            
            # Log completion of qubit receiving
            if self.host and hasattr(self.host, '_send_update'):
                from core.enums import SimulationEventType
                self.host._send_update(SimulationEventType.INFO,
                                       message=f"STUDENT BOB: Received all {self.bits_received} qubits, ready for b92_sifting() [b92_sifting]")
        
        return result
    
    def b92_sifting(self, their_bits):
        """Perform sifting using student's implementation"""
        if self.host is None:
            # Return empty results when no host is attached (for testing)
            return [], []
        
        self.qkd_phase = "sifting"
        print("Starting B92 sifting...")
        
        # Log detailed sifting process
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB: Starting sifting process with Alice's bits [b92_sifting]")
        
        # Debug: Print data before sifting
        print(f"DEBUG: Alice sent_bits: {getattr(self.student_alice, 'sent_bits', [])}")
        print(f"DEBUG: Bob received_measurements: {getattr(self.student_bob, 'received_measurements', [])}")
        print(f"DEBUG: Bob measurement_outcomes: {getattr(self.student_bob, 'measurement_outcomes', [])}")
        print(f"DEBUG: Bob received_bases: {getattr(self.student_bob, 'received_bases', [])}")
        
        # Try to get Alice's data from multiple sources
        alice_sent_bits = getattr(self.student_alice, 'sent_bits', [])
        
        # First priority: Use the sifting message data (their_bits parameter) - this is Alice's actual bits
        if their_bits:
            alice_sent_bits = their_bits
            print(f"DEBUG: Using Alice's data from sifting message: {alice_sent_bits}")
        
        # Second priority: Try to get it from Alice's student implementation
        elif not alice_sent_bits and hasattr(self.student_alice, 'sent_bits'):
            alice_sent_bits = self.student_alice.sent_bits
            print(f"DEBUG: Using Alice's data from student implementation: {alice_sent_bits}")
        
        # Third priority: Try to get it from the host's basis_choices (but only if it looks like bits, not bases)
        elif not alice_sent_bits and hasattr(self.host, 'basis_choices'):
            # Check if basis_choices contains bits (numbers) or bases (strings)
            if self.host.basis_choices and isinstance(self.host.basis_choices[0], (int, float)):
                alice_sent_bits = self.host.basis_choices
                print(f"DEBUG: Using Alice's data from host.basis_choices: {alice_sent_bits}")
            else:
                print(f"DEBUG: host.basis_choices contains bases, not bits: {self.host.basis_choices}")
        
        # Ensure we have data to work with
        if not alice_sent_bits:
            print("WARNING: Alice has no sent_bits data - using student implementation with empty data")
            if self.host and hasattr(self.host, '_send_update'):
                from core.enums import SimulationEventType
                self.host._send_update(SimulationEventType.INFO,
                                       message=f"STUDENT BOB: WARNING - Alice has no sent_bits data for sifting [b92_sifting]")
            # Use student implementation even with empty data
            return self.student_bob.b92_sifting([], self.student_bob.received_measurements)
        
        if not hasattr(self.student_bob, 'received_measurements') or not self.student_bob.received_measurements:
            print("WARNING: Bob has no received_measurements data - using student implementation with empty data")
            if self.host and hasattr(self.host, '_send_update'):
                from core.enums import SimulationEventType
                self.host._send_update(SimulationEventType.INFO,
                                       message=f"STUDENT BOB: WARNING - Bob has no received_measurements data for sifting [b92_sifting]")
            # Use student implementation even with empty data
            return self.student_bob.b92_sifting(alice_sent_bits, [])
        
        # Use Alice's sent bits and Bob's received measurements
        sifted_alice, sifted_bob = self.student_bob.b92_sifting(
            sent_bits=alice_sent_bits,  # Use Alice's actual sent bits
            received_measurements=self.student_bob.received_measurements
        )
        
        print(f"DEBUG: Sifting result - Alice: {sifted_alice}, Bob: {sifted_bob}")
        
        # Store sifted key on Bob's side
        self.student_bob.sifted_key = sifted_bob
        self.host.shared_bases_indices = list(range(len(sifted_bob)))
        
        # Calculate efficiency based on Alice's sent bits
        total_bits = len(alice_sent_bits) if alice_sent_bits else len(their_bits) if their_bits else 0
        efficiency = (len(sifted_bob) / total_bits * 100) if total_bits > 0 else 0
        
        # Log detailed sifting results
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB b92_sifting(): Found {len(sifted_bob)} sifted bits out of {total_bits} (Efficiency: {efficiency:.1f}%) [b92_sifting]",
                                   shared_bases=len(sifted_bob),
                                   efficiency=efficiency)
            
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB: Sifting completed - found {len(sifted_bob)} sifted bits [b92_sifting]",
                                   shared_bases=len(sifted_bob),
                                   efficiency=efficiency)
        
        self.host.send_classical_data({'type': 'sifted_bits', 'data': sifted_bob})
        return sifted_alice, sifted_bob
    
    def b92_estimate_error_rate(self, their_bits_sample):
        """Compute error rate using student's implementation"""
        if self.host is None:
            # Return 0.0 when no host is attached (for testing)
            return 0.0
        
        self.qkd_phase = "error_checking"
        print("Starting error rate estimation...")
        
        # Log detailed error estimation process
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB: Starting error rate estimation process [b92_estimate_error_rate]")
        
        # Debug: Print data before error estimation
        print(f"DEBUG: Bob sifted_key: {getattr(self.student_bob, 'sifted_key', [])}")
        print(f"DEBUG: their_bits_sample: {their_bits_sample}")
        
        # Use sifted key for error estimation if available
        if hasattr(self.student_bob, 'sifted_key') and self.student_bob.sifted_key:
            # Create sample positions and reference bits from sifted key
            sifted_key = self.student_bob.sifted_key
            sample_size = min(5, len(sifted_key))  # Sample first 5 bits
            sample_positions = list(range(sample_size))
            reference_bits = sifted_key[:sample_size]
            print(f"Using sifted key for error estimation: {len(sifted_key)} bits, sampling {sample_size}")
        else:
            # Fallback to provided sample
            if their_bits_sample:
                positions, reference_bits = zip(*their_bits_sample)
                sample_positions = list(positions)
            else:
                sample_positions = []
                reference_bits = []
            print(f"Using provided sample for error estimation: {len(sample_positions)} positions")
        
        # Ensure we have data for error estimation
        if not sample_positions or not reference_bits:
            print("WARNING: No data available for error estimation - using student implementation with empty data")
            if self.host and hasattr(self.host, '_send_update'):
                from core.enums import SimulationEventType
                self.host._send_update(SimulationEventType.INFO,
                                       message=f"STUDENT BOB: WARNING - No data available for error estimation [b92_estimate_error_rate]")
            # Use student implementation even with empty data
            return self.student_bob.b92_estimate_error_rate([], [])
        
        error_rate = self.student_bob.b92_estimate_error_rate(sample_positions, reference_bits)
        
        print(f"Student Bob error rate: {error_rate:.1%}")
        
        # Calculate error count for detailed logging
        total_comparisons = len(sample_positions) if sample_positions else 0
        error_count = int(error_rate * total_comparisons) if total_comparisons > 0 else 0
        
        # Log detailed error estimation results
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB b92_estimate_error_rate(): {error_rate:.1%} error rate ({error_count}/{total_comparisons} errors) using student implementation [b92_estimate_error_rate]",
                                   error_rate=error_rate)
            
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB: Error rate {error_rate:.1%} using b92_estimate_error_rate()!",
                                   error_rate=error_rate)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.SHARED_KEY_GENERATED,
                                   message="B92 QKD protocol completed successfully using student's code!",
                                   error_rate=error_rate,
                                   shared_bases=len(self.host.shared_bases_indices))
        
        self.host.send_classical_data({'type': 'complete'})
        self.qkd_phase = "complete"
        
        print("B92 PROTOCOL COMPLETE using student's implementation!")
        return error_rate
    
    def update_sifted_bits(self, sifted_bits):
        """Update sifted bits - called by Alice"""
        if self.host is None:
            return False
        
        print(f"Alice: Received {len(sifted_bits)} sifted bits from Bob")
        self.host.shared_bases_indices = list(range(len(sifted_bits)))
        
        if self.host and hasattr(self.host, 'update_sifted_bits'):
            self.host.update_sifted_bits(sifted_bits)
        
        return True

# ==========================================
# Simple wrapper to attach bridge to host
# ==========================================
class StudentImplementationBridgeB92:
    """Wrapper that uses EnhancedStudentImplementationBridgeB92"""
    
    def __init__(self, host):
        self.host = host
        self._bridge = EnhancedStudentImplementationBridgeB92()
        self._bridge.host = host
        print(f"✅ B92 Bridge created using StudentB92Host for host: {host.name if host else 'Unknown'}")
    
    def set_host(self, host):
        self.host = host
        self._bridge.host = host
        print(f"B92 Bridge host updated: {host.name if host else 'Unknown'}")
    
    def b92_send_qubits(self, num_qubits):
        return self._bridge.b92_send_qubits(num_qubits)
    
    def process_received_qbit(self, qbit, from_channel):
        return self._bridge.process_received_qbit(qbit, from_channel)
    
    def b92_sifting(self, their_bits):
        return self._bridge.b92_sifting(their_bits)
    
    def b92_estimate_error_rate(self, their_bits_sample):
        return self._bridge.b92_estimate_error_rate(their_bits_sample)