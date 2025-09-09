# bb84_impl.py
# =============
# BB84 Protocol Implementation Module
# Integrates student BB84 implementation with simulation system

import sys
import os
import json
from typing import Optional, Dict, Any

# Import BB84-specific components
from quantum_network.interactive_host import InteractiveQuantumHost
from enhanced_student_bridge import EnhancedStudentImplementationBridge
from student_bb84_impl import StudentQuantumHost

class BB84ProtocolManager:
    """
    BB84 Protocol Manager
    Handles BB84-specific simulation setup and execution
    """
    
    def __init__(self):
        self.protocol_name = "BB84"
        self.student_alice = None
        self.student_bob = None
        self.enhanced_bridge = None
        self.status_file = "student_implementation_status.json"
        
    def create_student_hosts(self, alice_name="Alice", bob_name="Bob"):
        """Create student BB84 host instances"""
        print(f"🔹 Creating BB84 student hosts: {alice_name} and {bob_name}")
        
        self.student_alice = StudentQuantumHost(alice_name)
        self.student_bob = StudentQuantumHost(bob_name)
        
        print(f"✅ BB84 student hosts created successfully")
        return self.student_alice, self.student_bob
    
    def create_enhanced_bridge(self, alice_name="Alice", bob_name="Bob"):
        """Create enhanced bridge for BB84 protocol"""
        print(f"🔹 Creating BB84 enhanced bridge")
        
        self.enhanced_bridge = EnhancedStudentImplementationBridge(
            student_alice=self.student_alice,
            student_bob=self.student_bob,
            alice_name=alice_name,
            bob_name=bob_name
        )
        
        print(f"✅ BB84 enhanced bridge created successfully")
        return self.enhanced_bridge
    
    def create_quantum_hosts(self, network, zone, alice_name="Alice", bob_name="Bob"):
        """Create quantum hosts for BB84 simulation"""
        print(f"🔹 Creating BB84 quantum hosts")
        
        # Create Alice (sender)
        alice_host = InteractiveQuantumHost(
            address="alice_bb84",
            location=(100, 100),
            network=network,
            zone=zone,
            name=alice_name,
            description="BB84 Alice - Quantum Key Sender",
            protocol="bb84",
            student_implementation=self.enhanced_bridge
        )
        
        # Create Bob (receiver)
        bob_host = InteractiveQuantumHost(
            address="bob_bb84", 
            location=(200, 100),
            network=network,
            zone=zone,
            name=bob_name,
            description="BB84 Bob - Quantum Key Receiver",
            protocol="bb84",
            student_implementation=self.enhanced_bridge
        )
        
        print(f"✅ BB84 quantum hosts created successfully")
        return alice_host, bob_host
    
    def write_status_file(self):
        """Write BB84 implementation status to file"""
        status = {
            "student_implementation_ready": True,
            "implementation_type": "BB84",
            "protocol": "bb84",
            "methods_implemented": [
                "bb84_send_qubits",
                "process_received_qbit", 
                "bb84_reconcile_bases",
                "bb84_estimate_error_rate"
            ],
            "student_plugin_module": "enhanced_student_bridge",
            "student_plugin_class": "EnhancedStudentImplementationBridge"
        }
        
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
        
        print(f"✅ BB84 status file written: {self.status_file}")
    
    def setup_complete_simulation(self, network, zone, alice_name="Alice", bob_name="Bob"):
        """Complete BB84 simulation setup"""
        print(f"🚀 Setting up complete BB84 simulation")
        
        # Step 1: Create student hosts
        self.create_student_hosts(alice_name, bob_name)
        
        # Step 2: Create enhanced bridge
        self.create_enhanced_bridge(alice_name, bob_name)
        
        # Step 3: Create quantum hosts
        alice_host, bob_host = self.create_quantum_hosts(network, zone, alice_name, bob_name)
        
        # Step 4: Write status file
        self.write_status_file()
        
        print(f"✅ BB84 simulation setup complete!")
        return alice_host, bob_host, self.enhanced_bridge

def create_bb84_simulation(network, zone, alice_name="Alice", bob_name="Bob"):
    """
    Factory function to create complete BB84 simulation
    """
    manager = BB84ProtocolManager()
    return manager.setup_complete_simulation(network, zone, alice_name, bob_name)

# Export the main function for notebook use
__all__ = ['BB84ProtocolManager', 'create_bb84_simulation']
