"""
Interactive Quantum Host for B92 Student Learning
===============================================

This module provides an interactive quantum host implementation specifically for B92
quantum key distribution protocol. It uses the student's B92 implementation from
student_b92_impl.py through the enhancedb92_bridge.py.

This host REQUIRES students to implement B92 quantum protocols before simulation can run.
The simulation will only work after students have "vibe coded" their B92 algorithms.

Students must implement:
- B92 quantum key distribution
- Quantum state preparation and measurement
- Custom quantum networking protocols
"""

from __future__ import annotations

import random
import time
import traceback
from typing import Any, Callable, List, Tuple, Optional
import importlib
try:
    import qutip as qt
except Exception:
    qt = None
from core.base_classes import World, Zone
from core.enums import InfoEventType, NodeType, SimulationEventType
from core.exceptions import QuantumChannelDoesNotExists
from core.network import Network
from quantum_network.channel import QuantumChannel
from quantum_network.node import QuantumNode
from quantum_network.repeater import QuantumRepeater


class InteractiveQuantumHostB92(QuantumNode):
    """
    Interactive Quantum Host for B92 Protocol
    
    This host REQUIRES students to implement quantum protocols before simulation can run.
    The simulation will only work after students have "vibe coded" their B92 algorithms.
    
    Students must implement:
    - B92 quantum key distribution
    - Quantum state preparation and measurement
    - Custom quantum networking protocols
    """
    
    def __init__(
        self,
        address: str,
        location: Tuple[int, int],
        network: Network,
        zone: Zone | World = None,
        send_classical_fn: Callable[[Any], None] = None,
        qkd_completed_fn: Callable[[List[int]], None] = None,
        name="",
        description="",
        protocol: str = "b92",
        student_implementation: Optional[object] = None,
        require_student_code: bool = True
    ):
        super().__init__(
            NodeType.QUANTUM_HOST, location, network, address, zone, name, description
        )
        
        # Protocol configuration
        self.protocol = protocol
        self.require_student_code = require_student_code
        
        # B92 specific attributes
        self.sent_bits = []
        self.prepared_qubits = []
        self.received_measurements = []
        self.sifted_key = []
        self.random_bits = []
        
        # BB84 compatibility attributes (for simulation integration)
        self.basis_choices = []
        self.measurement_outcomes = []
        self.shared_bases_indices = []
        self._reconcile_sent = False
        
        # Educational validation
        self.student_code_validated = False
        self.required_methods = ['b92_send_qubits', 'b92_process_received_qbit', 'b92_sifting', 'b92_estimate_error_rate']
        
        # Entanglement attributes
        self.entangled_qubit: 'qt.Qobj' | None = None
        self.entanglement_partner_address: str | None = None
        self.entangled_channel: QuantumChannel | None = None
        self.entangled_pairs = []
        
        # Callback functions (initialize attributes to safe defaults)
        self.send_classical_data = send_classical_fn if send_classical_fn else (lambda message: None)
        self.qkd_completed_fn = qkd_completed_fn if qkd_completed_fn else None
        
        # Learning metrics
        self.learning_stats = {
            'qubits_sent': 0,
            'qubits_received': 0,
            'successful_protocols': 0,
            'error_rates': []
        }
        
        # Optional back-reference to the owning adapter
        self.adapter = None
        
        # Quantum channels
        self.quantum_channels: List[QuantumChannel] = []
        
        # Student implementation
        self.student_implementation = student_implementation
        self.enhanced_bridge = None
        
        # Initialize student implementation
        if self.student_implementation is None and self.require_student_code:
            if self._try_load_student_implementation():
                print("✅ Loaded student implementation using enhanced bridge")
                self.validate_student_implementation()
            else:
                print("❌ STUDENT IMPLEMENTATION REQUIRED!")
                print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
                print("This simulation will NOT work without student B92 code!")
                print("Export your student implementation plugin from the notebook to enable the simulation.")
                print("Open quantum_networking_complete.ipynb for the export helper cell.")
                print("No hardcoded fallbacks available!")
                self.student_code_validated = False
        else:
            print(f"✅ Using student implementation: {type(student_implementation).__name__}")
            self.validate_student_implementation()
            # Ensure bridges/plugins that expect a back-reference get it
            try:
                if hasattr(self.student_implementation, 'host') and getattr(self.student_implementation, 'host', None) is None:
                    self.student_implementation.host = self
            except Exception:
                pass

    def _try_load_student_implementation(self):
        """Try to load student implementation using enhanced bridge"""
        try:
            from enhancedb92_bridge import EnhancedB92Bridge
            print("🔧 Attempting to load B92 student implementation using enhanced bridge...")
            
            self.enhanced_bridge = EnhancedB92Bridge()
            
            if self.enhanced_bridge.student_alice and self.enhanced_bridge.student_bob:
                print("✅ Enhanced bridge loaded B92 student implementation successfully!")
                # Set the host reference on the enhanced bridge
                self.enhanced_bridge.host = self
                self.student_implementation = self.enhanced_bridge
                return True
            else:
                print("❌ Enhanced bridge could not load student implementation")
                return False
                
        except Exception as e:
            print(f"❌ Error loading student implementation with enhanced bridge: {e}")
            return False

    def validate_student_implementation(self) -> bool:
        """
        Validate that the student implementation has all required methods.
        
        The implementation object should have methods like:
        - b92_send_qubits(num_qubits)
        - b92_process_received_qbit(qubit_data)
        - b92_reconcile_bases()
        - b92_estimate_error_rate()
        """
        if not self.student_implementation:
            print("❌ No student implementation provided")
            return False
            
        missing_methods = []
        for method in self.required_methods:
            if not hasattr(self.student_implementation, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Student implementation missing methods: {missing_methods}")
            print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
            print("Students must implement all required B92 methods in quantum_networking_complete.ipynb")
            self.student_code_validated = False
            return False
        
        print("✅ Student implementation validated - all required methods present!")
        self.student_code_validated = True
        return True

    def check_student_implementation_required(self, operation: str) -> bool:
        """Check if student implementation is required and available"""
        if not self.require_student_code:
            return True
            
        if not self.student_code_validated:
            print(f"❌ {operation} BLOCKED - Student implementation not validated!")
            print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
            return False
            
        return True

    def attach_student(self, student) -> bool:
        """Attach a student B92 implementation and validate it."""
        self.student_implementation = student
        ok = self.validate_student_implementation()
        if ok:
            # Set back-reference if the student implementation expects it
            try:
                if hasattr(self.student_implementation, 'host'):
                    self.student_implementation.host = self
            except Exception:
                pass
        return ok

    def add_quantum_channel(self, channel):
        """Add a quantum channel to this host"""
        self.quantum_channels.append(channel)

    def channel_exists(self, to_host: QuantumNode):
        """Check if channel exists to target host"""
        for chan in self.quantum_channels:
            if (chan.node_1 == self and chan.node_2 == to_host) or \
               (chan.node_2 == self and chan.node_1 == to_host):
                return chan
        return self.proxy_channel_exists(to_host)

    def proxy_channel_exists(self, to_host: QuantumNode):
        """Check for proxy channels through repeaters"""
        for chan in self.quantum_channels:
            if hasattr(chan, 'node_1') and hasattr(chan, 'node_2'):
                if chan.node_1 == self and hasattr(chan.node_2, 'quantum_channels'):
                    return chan.node_2.channel_exists(to_host)
                elif chan.node_2 == self and hasattr(chan.node_1, 'quantum_channels'):
                    return chan.node_1.channel_exists(to_host)
        return None

    def get_channel(self, to_host: QuantumNode = None):
        """Get a quantum channel to target host"""
        if to_host:
            return self.channel_exists(to_host)
        elif self.quantum_channels:
            return self.quantum_channels[0]
        return None

    def send_qubit(self, qubit, channel: QuantumChannel):
        """Send a qubit through a quantum channel"""
        if channel:
            channel.transmit_qubit(qubit, self)

    def receive_qubit(self, qbit, from_channel):
        """Receive a qubit from a quantum channel"""
        print(f"🔬 {self.name}: Received qubit from {from_channel}")
        # Process the received qubit using B92 protocol
        if hasattr(self, 'b92_process_received_qbit'):
            self.b92_process_received_qbit(qbit, from_channel)

    def b92_send_qubits(self, num_qubits: int = None):
        """
        Send qubits using B92 protocol.
        ABSOLUTELY REQUIRES student implementation - NO FALLBACKS!
        """
        if not self.check_student_implementation_required("B92 Send Qubits"):
            return False
            
        default_bits = 16
        if num_qubits is None:
            num_qubits = default_bits
            
        print(f"🔬 {self.name}: B92 Send Qubits called with {num_qubits} qubits")
        
        # Use enhanced bridge if available
        if self.enhanced_bridge and hasattr(self.enhanced_bridge, 'b92_send_qubits'):
            print(f"🎓 {self.name}: Using enhanced bridge for b92_send_qubits")
            return self.enhanced_bridge.b92_send_qubits(num_qubits)
            
        if self.student_implementation and hasattr(self.student_implementation, 'b92_send_qubits'):
            print(f"🎓 {self.name}: Calling student B92 implementation...")
            result = self.student_implementation.b92_send_qubits(num_qubits)
            print(f"🎓 {self.name}: Student implementation result: {result}")
            return result
        
        # NO FALLBACKS! Students must implement this themselves
        print("❌ B92 Send Qubits BLOCKED - Student implementation required!")
        print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
        print("Students must implement b92_send_qubits() method in quantum_networking_complete.ipynb")
        return False

    def b92_process_received_qbit(self, qubit_data):
        """
        Process received qubit using B92 protocol.
        ABSOLUTELY REQUIRES student implementation - NO FALLBACKS!
        """
        if not self.check_student_implementation_required("B92 Process Received Qubit"):
            return False
            
        print(f"🔬 {self.name}: B92 Process Received Qubit called")
        
        # Use enhanced bridge if available
        if self.enhanced_bridge and hasattr(self.enhanced_bridge, 'b92_process_received_qbit'):
            print(f"🎓 {self.name}: Using enhanced bridge for b92_process_received_qbit")
            return self.enhanced_bridge.b92_process_received_qbit(qubit_data)
            
        if self.student_implementation and hasattr(self.student_implementation, 'b92_process_received_qbit'):
            print(f"🎓 {self.name}: Calling student b92_process_received_qbit implementation")
            return self.student_implementation.b92_process_received_qbit(qubit_data)
        
        # NO FALLBACKS! Students must implement this themselves
        print("❌ B92 Process Received Qubit BLOCKED - Student implementation required!")
        print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
        print("Students must implement b92_process_received_qbit() method in quantum_networking_complete.ipynb")
        return False

    def b92_sifting(self):
        """
        Perform sifting using B92 protocol.
        ABSOLUTELY REQUIRES student implementation - NO FALLBACKS!
        """
        print(f"🔍 {self.name}: b92_sifting called")
        if not self.check_student_implementation_required("B92 Sifting"):
            return False
            
        # Use enhanced bridge if available
        if self.enhanced_bridge and hasattr(self.enhanced_bridge, 'b92_sifting'):
            print(f"🎓 {self.name}: Using enhanced bridge for b92_sifting")
            return self.enhanced_bridge.b92_sifting()
            
        if self.student_implementation and hasattr(self.student_implementation, 'b92_sifting'):
            print(f"🎓 {self.name}: Calling student b92_sifting implementation")
            return self.student_implementation.b92_sifting()
        
        # NO FALLBACKS! Students must implement this themselves
        print("❌ B92 Sifting BLOCKED - Student implementation required!")
        print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
        print("Students must implement b92_sifting() method in quantum_networking_complete.ipynb")
        return False

    def b92_estimate_error_rate(self):
        """
        Estimate error rate using B92 protocol.
        ABSOLUTELY REQUIRES student implementation - NO FALLBACKS!
        """
        print(f"🔍 {self.name}: b92_estimate_error_rate called")
        if not self.check_student_implementation_required("B92 Error Rate Estimation"):
            return False
            
        # Use enhanced bridge if available
        if self.enhanced_bridge and hasattr(self.enhanced_bridge, 'b92_estimate_error_rate'):
            print(f"🎓 {self.name}: Using enhanced bridge for b92_estimate_error_rate")
            return self.enhanced_bridge.b92_estimate_error_rate()
            
        if self.student_implementation and hasattr(self.student_implementation, 'b92_estimate_error_rate'):
            print(f"🎓 {self.name}: Calling student b92_estimate_error_rate implementation")
            return self.student_implementation.b92_estimate_error_rate()
        
        # NO FALLBACKS! Students must implement this themselves
        print("❌ B92 Error Rate Estimation BLOCKED - Student implementation required!")
        print("🔬 VIBE CODE B92 ALGORITHM USING THE HINTS PROVIDED TO RUN THE SIMULATION")
        print("Students must implement b92_estimate_error_rate() method in quantum_networking_complete.ipynb")
        return False

    def b92_extract_key(self):
        """Extract the final shared key from B92 protocol"""
        if hasattr(self, 'sifted_key') and self.sifted_key:
            return self.sifted_key
        return []

    def perform_qkd(self):
        """Perform quantum key distribution using B92 protocol"""
        if self.protocol == 'entanglement_swapping':
            # Entanglement-based protocols
            channel = self.get_channel()
            if channel:
                repeater = channel.get_other_node(self)
                if not isinstance(repeater, QuantumRepeater):
                    print(f"ERROR: Host {self.name} is in 'entanglement_swapping' mode but no repeater found.")
                    return
                target = repeater.get_other_node(self)
                self.request_entanglement(target)
                target.request_entanglement(self)
        else:
            # B92 protocol
            self.b92_send_qubits()

    def start_quantum_protocol(self, target_host: 'InteractiveQuantumHostB92'):
        """Start B92 quantum protocol with target host"""
        print(f"🔬 {self.name}: Starting B92 quantum protocol with {target_host.name}")
        
        if self.entangled_channel:
            # Entanglement-based protocol
            self.request_entanglement(target_host)
        else:
            # B92 protocol
            self.b92_send_qubits()

    def request_entanglement(self, target_host: 'InteractiveQuantumHostB92'):
        """Request entanglement with target host"""
        if self.protocol != "entanglement_swapping":
            print(f"ERROR: Host {self.name} is not in 'entanglement_swapping' mode.")
            return

        print(f"🔗 {self.name}: Requesting entanglement with {target_host.name}")
        
        channel = self.channel_exists(target_host)
        if not channel:
            print(f"ERROR: No channel found to {target_host.name}")
            return
            
        # Create Bell state
        if qt:
            bell_state = qt.bell_state("00")
            qubit_to_keep = qt.ptrace(bell_state, 0)
            qubit_to_send = qt.ptrace(bell_state, 1)

            self.entangled_qubit = qubit_to_keep
            self.entanglement_partner_address = target_host.name
            
            channel.transmit_qubit(qubit_to_send, self)
        else:
            print("⚠️ Qutip not available for entanglement")

    def process_message(self, message: dict, from_host: 'InteractiveQuantumHostB92' = None):
        """Process incoming messages for B92 protocol"""
        print(f"📨 {self.name}: Processing message: {message.get('type', 'unknown')}")
        
        message_type = message.get("type")
        
        if self.protocol == "b92" or self.entangled_channel:
            if message_type == "reconcile_bases" or message_type == "sifting":
                print(f"🔍 {self.name}: Received sifting message")
                try:
                    if hasattr(self, 'b92_sifting'):
                        self.b92_sifting()
                except Exception:
                    pass
            elif message_type == "estimate_error_rate":
                print(f"🔍 {self.name}: Received estimate_error_rate message")
                try:
                    if hasattr(self, 'b92_estimate_error_rate'):
                        self.b92_estimate_error_rate()
                except Exception:
                    pass
            elif message_type == "complete":
                raw_key = self.b92_extract_key()
                callback = getattr(self, 'qkd_completed_fn', None)
                if callback:
                    callback(raw_key)
                print(f"🔐 {self.name}: B92 QKD completed with key length: {len(raw_key)}")

    def emit_event(self, event_type: str, data: dict = None):
        """Emit simulation event"""
        if data is None:
            data = {}
        
        event_data = {
            "type": event_type,
            "source": self.name,
            "timestamp": time.time(),
            "data": data
        }
        
        # Emit to simulation system
        if hasattr(self, 'world') and self.world:
            self.world.emit_event(event_data)

    def __str__(self):
        return f"InteractiveQuantumHostB92(name='{self.name}', protocol='{self.protocol}', validated={self.student_code_validated})"

    def __repr__(self):
        return self.__str__()
