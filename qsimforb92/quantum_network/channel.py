from __future__ import annotations
import random
import time
import os
import json
try:
    import qutip as qt
except Exception:
    qt = None
import numpy as np
from typing import TYPE_CHECKING, Union

# from core.base_classes import Node
from core.enums import SimulationEventType
from core.exceptions import QubitLossError
from core.s_object import Sobject

if TYPE_CHECKING:
    from quantum_network.node import QuantumNode

class QuantumChannel(Sobject):
    def __init__(
        self,
        node_1: QuantumNode,
        node_2: QuantumNode,
        length: float,
        loss_per_km: float,
        noise_model: str,
        noise_strength: float = 0.01,
        name: str = "",
        description: str = "",
        error_rate_threshold: float = 10.0,
        num_bits: int = 16
    ) -> None:
        super().__init__(name, description)
        self.node_1 = node_1
        self.node_2 = node_2
        self.length = length
        self.loss_per_km = loss_per_km
        self.noise_model = noise_model
        self.noise_strength = noise_strength
        self.error_rate_threshold = error_rate_threshold
        self.num_bits = num_bits

    def __name__(self) -> str:
        return f"{self.node_1.name} <~~~> {self.node_2.name}"

    def __repr__(self) -> str:
        return self.__name__()

    def transmit_qubit(self, qubit, from_node: QuantumNode, noise_strength: float = None) -> None:
        # Use provided noise strength or default to channel's setting
        if noise_strength is None:
            noise_strength = self.noise_strength
            
        if self.noise_model != 'none' and qt is not None:
            # Simulate the loss based on length and loss_per_km
            length_km = self.length
            loss_prob = 1 - (1 - self.loss_per_km) ** length_km
            loss_prod_rand = random.random()
            if loss_prod_rand < loss_prob:
                protocol = self.detect_active_protocol()
                reason = f"Qubit lost during transmission in connection {self.name} over {length_km} km. (Loss probability: {loss_prob:.2f})"
                if protocol == "B92":
                    print(f"⚠️ 🔬 B92 {reason} Loss probability: {loss_prob:.2f}. Random value: {loss_prod_rand:.2f}")
                elif protocol == "BB84":
                    print(f"⚠️ 🔐 BB84 {reason} Loss probability: {loss_prob:.2f}. Random value: {loss_prod_rand:.2f}")
                else:
                    print(f"⚠️ {reason} Loss probability: {loss_prob:.2f}. Random value: {loss_prod_rand:.2f}")
                # Skip server update to avoid Redis configuration issues
                # self._send_update(SimulationEventType.QUBIT_LOST, reason=reason)
                raise QubitLossError(self, qubit)

            # Apply noise to the qubit (using QuTiP)
            noisy_qubit = self.apply_noise(qubit, noise_strength)
        else:
            noisy_qubit = qubit

        # Send the qubit to the destination node
        to_node = self.node_2 if self.node_1 == from_node else self.node_1
        
        to_node.receive_qubit(noisy_qubit, self)

    def log(self, message: str) -> None:
        """Protocol-aware logging function"""
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            print(f"🔬 [B92-Channel] {message}")
        elif protocol == "BB84":
            print(f"🔐 [BB84-Channel] {message}")
        else:
            print(f"[QuantumChannel] {message}")
    
    def detect_active_protocol(self) -> str:
        """Detect which protocol is currently active based on status files"""
        # Use centralized protocol detection utility
        try:
            from protocol_detection_utils import detect_active_protocol
            return detect_active_protocol()
        except ImportError:
            # Fallback to local implementation if utility not available
            # Check for BB84 status file first (priority)
            if os.path.exists("student_implementation_status.json"):
                try:
                    with open("student_implementation_status.json", "r") as f:
                        status = json.load(f)
                    if status.get("student_implementation_ready") and status.get("protocol") == "bb84":
                        return "BB84"
                except Exception:
                    pass
            
            # Check for B92 status file (only if not disabled)
            if os.path.exists("student_b92_implementation_status.json") and not os.path.exists("student_b92_implementation_status.json.disabled"):
                try:
                    with open("student_b92_implementation_status.json", "r") as f:
                        status = json.load(f)
                    if status.get("student_implementation_ready"):
                        return "B92"
                except Exception:
                    pass
            
            # Default to BB84 if no clear detection
            return "BB84"

    def get_other_node(self, node):
        return self.node_2 if self.node_1 == node else self.node_1
    
    def apply_noise(self, qubit, noise_strength: float = None):
        """Apply noise based on the channel's noise model"""
        if noise_strength is None:
            noise_strength = self.noise_strength
        # If QuTiP is unavailable or qubit is not a Qobj, skip noise
        if qt is None or not isinstance(qubit, qt.Qobj):
            return qubit
            
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log(f"🔬 Applying {self.noise_model} noise to B92 qubit (strength: {noise_strength})")
        elif protocol == "BB84":
            self.log(f"🔐 Applying {self.noise_model} noise to BB84 qubit (strength: {noise_strength})")
        else:
            self.log(f"Applying {self.noise_model} noise to qubit (strength: {noise_strength})")
        
        if self.noise_model == "transmutation":
            return self._apply_transmutation_noise(qubit, noise_strength)
        elif self.noise_model == "depolarizing":
            return self._apply_depolarizing_noise(qubit, noise_strength)
        elif self.noise_model == "amplitude_damping":
            return self._apply_amplitude_damping(qubit, noise_strength)
        elif self.noise_model == "phase_damping":
            return self._apply_phase_damping(qubit, noise_strength)
        else:
            self.log("No noise model specified - returning original qubit")
            return qubit

    def _apply_transmutation_noise(self, qubit: 'qt.Qobj', p_flip: float):
        """Apply bit-flip (transmutation) noise"""
        # Ensure input is a qt.Qobj
        if qt is None or not isinstance(qubit, qt.Qobj):
            return qubit
            
        protocol = self.detect_active_protocol()
        if random.random() < p_flip:
            if protocol == "B92":
                self.log(f"🔬 B92 Bit-flip occurred with probability {p_flip}")
            elif protocol == "BB84":
                self.log(f"🔐 BB84 Bit-flip occurred with probability {p_flip}")
            else:
                self.log(f"Bit-flip occurred with probability {p_flip}")
            # Apply Pauli-X (bit flip)
            return qt.sigmax() * qubit
        else:
            if protocol == "B92":
                self.log(f"🔬 B92 No bit-flip (probability was {p_flip})")
            elif protocol == "BB84":
                self.log(f"🔐 BB84 No bit-flip (probability was {p_flip})")
            else:
                self.log(f"No bit-flip (probability was {p_flip})")
            return qubit

    def _apply_depolarizing_noise(self, qubit: 'qt.Qobj', p: float):
        """Apply depolarizing noise using Kraus operators"""
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log(f"🔬 B92 Applying depolarizing noise with strength {p}")
        elif protocol == "BB84":
            self.log(f"🔐 BB84 Applying depolarizing noise with strength {p}")
        else:
            self.log(f"Applying depolarizing noise with strength {p}")
        if qt is None or not isinstance(qubit, qt.Qobj):
            return qubit
        
        if qubit.isket:
            # Convert to density matrix
            rho = qubit * qubit.dag()
        else:
            rho = qubit
        
        # Depolarizing channel Kraus operators
        E0 = np.sqrt(1 - 3*p/4) * qt.qeye(2)
        E1 = np.sqrt(p/4) * qt.sigmax()
        E2 = np.sqrt(p/4) * qt.sigmay()
        E3 = np.sqrt(p/4) * qt.sigmaz()
        
        kraus_ops = [E0, E1, E2, E3]
        noisy_rho = sum(E * rho * E.dag() for E in kraus_ops)
        
        # Ensure we return a qt.Qobj even if sum resulted in scalar
        if not isinstance(noisy_rho, qt.Qobj):
            noisy_rho = qt.Qobj(noisy_rho)
        
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log("🔬 B92 Depolarizing noise applied successfully")
        elif protocol == "BB84":
            self.log("🔐 BB84 Depolarizing noise applied successfully")
        else:
            self.log("Depolarizing noise applied successfully")
        return noisy_rho

    def _apply_amplitude_damping(self, qubit: 'qt.Qobj', gamma: float):
        """Apply amplitude damping noise"""
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log(f"🔬 B92 Applying amplitude damping with gamma={gamma}")
        elif protocol == "BB84":
            self.log(f"🔐 BB84 Applying amplitude damping with gamma={gamma}")
        else:
            self.log(f"Applying amplitude damping with gamma={gamma}")
        if qt is None or not isinstance(qubit, qt.Qobj):
            return qubit
        
        if qubit.isket:
            rho = qubit * qubit.dag()
        else:
            rho = qubit
        
        # Amplitude damping Kraus operators
        E0 = qt.Qobj([[1, 0], [0, np.sqrt(1-gamma)]])
        E1 = qt.Qobj([[0, np.sqrt(gamma)], [0, 0]])
        
        kraus_ops = [E0, E1]
        noisy_rho = sum(E * rho * E.dag() for E in kraus_ops)
        
        # Ensure we return a qt.Qobj even if sum resulted in scalar
        if not isinstance(noisy_rho, qt.Qobj):
            noisy_rho = qt.Qobj(noisy_rho)
        
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log("🔬 B92 Amplitude damping applied successfully")
        elif protocol == "BB84":
            self.log("🔐 BB84 Amplitude damping applied successfully")
        else:
            self.log("Amplitude damping applied successfully")
        return noisy_rho

    def _apply_phase_damping(self, qubit: 'qt.Qobj', gamma: float):
        """Apply phase damping noise"""
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log(f"🔬 B92 Applying phase damping with gamma={gamma}")
        elif protocol == "BB84":
            self.log(f"🔐 BB84 Applying phase damping with gamma={gamma}")
        else:
            self.log(f"Applying phase damping with gamma={gamma}")
        if qt is None or not isinstance(qubit, qt.Qobj):
            return qubit
        
        if qubit.isket:
            rho = qubit * qubit.dag()
        else:
            rho = qubit
        
        # Phase damping Kraus operators
        E0 = qt.Qobj([[1, 0], [0, np.sqrt(1-gamma)]])
        E1 = qt.Qobj([[0, 0], [0, np.sqrt(gamma)]])
        
        kraus_ops = [E0, E1]
        noisy_rho = sum(E * rho * E.dag() for E in kraus_ops)
        
        # Ensure we return a qt.Qobj even if sum resulted in scalar
        if not isinstance(noisy_rho, qt.Qobj):
            noisy_rho = qt.Qobj(noisy_rho)
        
        protocol = self.detect_active_protocol()
        if protocol == "B92":
            self.log(f"🔬 B92 Phase damping applied successfully. Before: {rho}, After: {noisy_rho}")
        elif protocol == "BB84":
            self.log(f"🔐 BB84 Phase damping applied successfully. Before: {rho}, After: {noisy_rho}")
        else:
            self.log(f"Phase damping applied successfully. Before: {rho}, After: {noisy_rho}")
        return noisy_rho