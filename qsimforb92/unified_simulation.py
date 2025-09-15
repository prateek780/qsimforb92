# unified_simulation.py
# =====================
# Unified Simulation Runner for QKD Protocols
# Handles both BB84 and B92 protocols dynamically

import sys
import os
import json
from typing import Optional, Dict, Any, Tuple

from protocol_detector import detect_qkd_protocol, get_protocol_manager
from bb84_impl import create_bb84_simulation
from b92_impl import create_b92_simulation

class UnifiedQKDSimulation:
    """
    Unified QKD Simulation Manager
    Automatically detects and runs the appropriate protocol
    """
    
    def __init__(self):
        self.current_protocol = None
        self.protocol_manager = None
        self.alice_host = None
        self.bob_host = None
        self.enhanced_bridge = None
        
    def detect_and_setup(self, cell_content: str = None, alice_name="Alice", bob_name="Bob"):
        """
        Detect protocol and setup simulation
        """
        print("🚀 Starting Unified QKD Simulation Setup")
        print("=" * 50)
        
        # Detect protocol
        self.current_protocol = detect_qkd_protocol(cell_content)
        print(f"📡 Detected Protocol: {self.current_protocol}")
        
        # Get protocol manager
        self.protocol_manager = get_protocol_manager(self.current_protocol)
        print(f"🔧 Using Protocol Manager: {type(self.protocol_manager).__name__}")
        
        return self.current_protocol
    
    def create_simulation(self, network, zone, alice_name="Alice", bob_name="Bob"):
        """
        Create the complete simulation for the detected protocol
        """
        if self.protocol_manager is None:
            raise RuntimeError("Protocol not detected. Call detect_and_setup() first.")
        
        print(f"🏗️ Creating {self.current_protocol} simulation...")
        
        # Use the protocol manager to create the simulation
        self.alice_host, self.bob_host, self.enhanced_bridge = \
            self.protocol_manager.setup_complete_simulation(network, zone, alice_name, bob_name)
        
        print(f"✅ {self.current_protocol} simulation created successfully!")
        return self.alice_host, self.bob_host, self.enhanced_bridge
    
    def run_simulation(self, num_qubits: int = None):
        """
        Run the QKD simulation
        """
        if self.alice_host is None or self.bob_host is None:
            raise RuntimeError("Simulation not created. Call create_simulation() first.")
        
        print(f"🎬 Running {self.current_protocol} QKD Simulation")
        print("=" * 50)
        
        # Set default number of qubits based on protocol
        if num_qubits is None:
            num_qubits = 50 if self.current_protocol == "BB84" else 20
        
        print(f"📊 Number of qubits: {num_qubits}")
        
        # Run the appropriate protocol
        if self.current_protocol == "BB84":
            return self._run_bb84_simulation(num_qubits)
        elif self.current_protocol == "B92":
            return self._run_b92_simulation(num_qubits)
        else:
            raise ValueError(f"Unknown protocol: {self.current_protocol}")
    
    def _run_bb84_simulation(self, num_qubits: int):
        """Run BB84 simulation"""
        print("🔹 Running BB84 Protocol...")
        
        # Alice sends qubits
        print("📤 Alice sending qubits...")
        self.alice_host.bb84_send_qubits(num_qubits)
        
        # Bob processes received qubits (handled by quantum channel)
        print("📥 Bob processing received qubits...")
        
        # The simulation will handle the rest through the enhanced bridge
        print("✅ BB84 simulation initiated!")
        return True
    
    def _run_b92_simulation(self, num_qubits: int):
        """Run B92 simulation"""
        print("🔹 Running B92 Protocol...")
        
        # Alice sends qubits
        print("📤 Alice sending qubits...")
        self.alice_host.b92_send_qubits(num_qubits)
        
        # Bob processes received qubits (handled by quantum channel)
        print("📥 Bob processing received qubits...")
        
        # The simulation will handle the rest through the enhanced bridge
        print("✅ B92 simulation initiated!")
        return True
    
    def get_simulation_info(self) -> Dict[str, Any]:
        """
        Get information about the current simulation
        """
        return {
            "protocol": self.current_protocol,
            "alice_host": self.alice_host.name if self.alice_host else None,
            "bob_host": self.bob_host.name if self.bob_host else None,
            "enhanced_bridge": type(self.enhanced_bridge).__name__ if self.enhanced_bridge else None,
            "protocol_manager": type(self.protocol_manager).__name__ if self.protocol_manager else None
        }

def create_unified_simulation(network, zone, cell_content: str = None, 
                            alice_name="Alice", bob_name="Bob"):
    """
    Factory function to create and setup unified QKD simulation
    """
    simulation = UnifiedQKDSimulation()
    simulation.detect_and_setup(cell_content, alice_name, bob_name)
    alice_host, bob_host, enhanced_bridge = simulation.create_simulation(network, zone, alice_name, bob_name)
    return simulation, alice_host, bob_host, enhanced_bridge

def run_qkd_simulation(network, zone, cell_content: str = None, 
                      alice_name="Alice", bob_name="Bob", num_qubits: int = None):
    """
    Complete QKD simulation runner - detects protocol and runs simulation
    """
    simulation = UnifiedQKDSimulation()
    
    # Detect and setup
    protocol = simulation.detect_and_setup(cell_content, alice_name, bob_name)
    
    # Create simulation
    alice_host, bob_host, enhanced_bridge = simulation.create_simulation(network, zone, alice_name, bob_name)
    
    # Run simulation
    success = simulation.run_simulation(num_qubits)
    
    return simulation, success

# Export main functions
__all__ = ['UnifiedQKDSimulation', 'create_unified_simulation', 'run_qkd_simulation']
