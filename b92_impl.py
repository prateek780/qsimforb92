# b92_impl.py
# ============
# B92 Protocol Implementation Module
# Integrates student B92 implementation with simulation system

import sys
import os
import json
from typing import Optional, Dict, Any

# Import B92-specific components
from quantum_network.interactive_host_b92 import InteractiveQuantumHostB92
from enhanced_student_bridge_b92 import EnhancedStudentB92ImplementationBridge
from student_b92_impl import StudentB92Host

class B92ProtocolManager:
    """
    B92 Protocol Manager
    Handles B92-specific simulation setup and execution
    """
    
    def __init__(self):
        self.protocol_name = "B92"
        self.student_alice = None
        self.student_bob = None
        self.enhanced_bridge = None
        self.status_file = "student_b92_implementation_status.json"
        
    def create_student_hosts(self, alice_name="Alice", bob_name="Bob"):
        """Create student B92 host instances"""
        print(f"🔹 Creating B92 student hosts: {alice_name} and {bob_name}")
        
        self.student_alice = StudentB92Host(alice_name)
        self.student_bob = StudentB92Host(bob_name)
        
        print(f"✅ B92 student hosts created successfully")
        return self.student_alice, self.student_bob
    
    def create_enhanced_bridge(self, alice_name="Alice", bob_name="Bob"):
        """Create enhanced bridge for B92 protocol"""
        print(f"🔹 Creating B92 enhanced bridge")
        
        self.enhanced_bridge = EnhancedStudentB92ImplementationBridge(
            student_alice=self.student_alice,
            student_bob=self.student_bob,
            alice_name=alice_name,
            bob_name=bob_name
        )
        
        print(f"✅ B92 enhanced bridge created successfully")
        return self.enhanced_bridge
    
    def create_quantum_hosts(self, network, zone, alice_name="Alice", bob_name="Bob"):
        """Create quantum hosts for B92 simulation"""
        print(f"🔹 Creating B92 quantum hosts")
        
        # Create Alice (sender)
        alice_host = InteractiveQuantumHostB92(
            address="alice_b92",
            location=(100, 100),
            network=network,
            zone=zone,
            name=alice_name,
            description="B92 Alice - Quantum Key Sender",
            protocol="b92",
            student_implementation=self.enhanced_bridge
        )
        
        # Create Bob (receiver)
        bob_host = InteractiveQuantumHostB92(
            address="bob_b92",
            location=(200, 100),
            network=network,
            zone=zone,
            name=bob_name,
            description="B92 Bob - Quantum Key Receiver",
            protocol="b92",
            student_implementation=self.enhanced_bridge
        )
        
        print(f"✅ B92 quantum hosts created successfully")
        return alice_host, bob_host
    
    def write_status_file(self):
        """Write B92 implementation status to file"""
        status = {
            "student_implementation_ready": True,
            "implementation_type": "B92",
            "protocol": "b92",
            "methods_implemented": [
                "b92_send_qubits",
                "b92_process_received_qbit",
                "b92_sifting",
                "b92_estimate_error_rate"
            ],
            "student_plugin_module": "enhancedb92_bridge",
            "student_plugin_class": "EnhancedStudentB92ImplementationBridge"
        }
        
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
        
        print(f"✅ B92 status file written: {self.status_file}")
    
    def setup_complete_simulation(self, network, zone, alice_name="Alice", bob_name="Bob"):
        """Complete B92 simulation setup"""
        print(f"🚀 Setting up complete B92 simulation")
        
        # Step 1: Create student hosts
        self.create_student_hosts(alice_name, bob_name)
        
        # Step 2: Create enhanced bridge
        self.create_enhanced_bridge(alice_name, bob_name)
        
        # Step 3: Create quantum hosts
        alice_host, bob_host = self.create_quantum_hosts(network, zone, alice_name, bob_name)
        
        # Step 4: Write status file
        self.write_status_file()
        
        print(f"✅ B92 simulation setup complete!")
        return alice_host, bob_host, self.enhanced_bridge

def create_b92_simulation(network, zone, alice_name="Alice", bob_name="Bob"):
    """
    Factory function to create complete B92 simulation
    """
    manager = B92ProtocolManager()
    return manager.setup_complete_simulation(network, zone, alice_name, bob_name)

# Export the main function for notebook use
__all__ = ['B92ProtocolManager', 'create_b92_simulation']
