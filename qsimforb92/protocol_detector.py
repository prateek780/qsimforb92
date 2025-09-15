# protocol_detector.py
# ====================
# Protocol Detection System for QKD Notebook
# Detects which protocol (BB84 or B92) to use based on notebook cell selection

import os
import json
import inspect
from typing import Optional, Dict, Any, Tuple

class ProtocolDetector:
    """
    Detects which QKD protocol to use based on notebook context
    """
    
    def __init__(self):
        self.bb84_indicators = [
            "bb84", "BB84", "bb84_send_qubits", "bb84_reconcile_bases", 
            "bb84_estimate_error_rate", "StudentQuantumHost", "Z-basis", "X-basis"
        ]
        self.b92_indicators = [
            "b92", "B92", "b92_send_qubits", "b92_sifting", "b92_estimate_error_rate",
            "StudentB92Host", "|0>", "|+>", "non-orthogonal"
        ]
        self.current_protocol = None
        self.detection_method = None
    
    def detect_from_globals(self) -> Optional[str]:
        """
        Detect protocol from global variables in notebook
        """
        try:
            # Get the calling frame (notebook context)
            frame = inspect.currentframe()
            while frame:
                frame = frame.f_back
                if frame and frame.f_globals:
                    globals_dict = frame.f_globals
                    
                    # Check for BB84 indicators
                    bb84_score = 0
                    b92_score = 0
                    
                    for key, value in globals_dict.items():
                        key_str = str(key).lower()
                        value_str = str(value).lower()
                        
                        # Check for BB84 indicators
                        for indicator in self.bb84_indicators:
                            if indicator.lower() in key_str or indicator.lower() in value_str:
                                bb84_score += 1
                        
                        # Check for B92 indicators  
                        for indicator in self.b92_indicators:
                            if indicator.lower() in key_str or indicator.lower() in value_str:
                                b92_score += 1
                    
                    # Determine protocol based on scores - require significant difference
                    if bb84_score > b92_score and bb84_score >= 2:
                        self.current_protocol = "BB84"
                        self.detection_method = "globals_bb84"
                        return "BB84"
                    elif b92_score > bb84_score and b92_score >= 2:
                        self.current_protocol = "B92"
                        self.detection_method = "globals_b92"
                        return "B92"
                        
        except Exception as e:
            print(f"⚠️ Error detecting from globals: {e}")
        
        return None
    
    def detect_from_status_files(self) -> Optional[str]:
        """
        Detect protocol from existing status files using centralized detection
        """
        try:
            # Use centralized protocol detection from QuantumChannel
            from quantum_network.channel import QuantumChannel
            from types import SimpleNamespace
            
            class MockNode:
                def __init__(self, name):
                    self.name = name
            
            # Create a temporary channel just to use its protocol detection
            temp_channel = QuantumChannel(
                MockNode('Alice'), MockNode('Bob'), 
                length=1.0, loss_per_km=0.1, noise_model='none'
            )
            
            detected_protocol = temp_channel.detect_active_protocol()
            if detected_protocol in ["BB84", "B92"]:
                self.current_protocol = detected_protocol
                self.detection_method = f"centralized_status_{detected_protocol.lower()}"
                return detected_protocol
                        
        except Exception as e:
            print(f"⚠️ Error using centralized protocol detection: {e}")
        
        return None
    
    def detect_from_cell_content(self, cell_content: str) -> Optional[str]:
        """
        Detect protocol from notebook cell content
        """
        try:
            content_lower = cell_content.lower()
            
            # Remove commented lines to avoid false positives
            lines = content_lower.split('\n')
            active_lines = []
            for line in lines:
                line = line.strip()
                # Skip commented lines and docstrings
                if not line.startswith('#') and not line.startswith('"""') and not line.startswith("'''"):
                    active_lines.append(line)
            active_content = '\n'.join(active_lines)
            
            bb84_score = sum(1 for indicator in self.bb84_indicators 
                           if indicator.lower() in active_content)
            b92_score = sum(1 for indicator in self.b92_indicators 
                          if indicator.lower() in active_content)
            
            # Only detect if there's a clear winner and significant score
            if bb84_score > b92_score and bb84_score >= 2:
                self.current_protocol = "BB84"
                self.detection_method = "cell_content_bb84"
                return "BB84"
            elif b92_score > bb84_score and b92_score >= 2:
                self.current_protocol = "B92"
                self.detection_method = "cell_content_b92"
                return "B92"
                
        except Exception as e:
            print(f"⚠️ Error detecting from cell content: {e}")
        
        return None
    
    def detect_protocol(self, cell_content: str = None) -> str:
        """
        Main detection method - tries multiple approaches
        """
        print("🔍 Detecting QKD protocol...")
        
        # Method 1: Check status files first (most reliable)
        protocol = self.detect_from_status_files()
        if protocol:
            print(f"✅ Protocol detected from status file: {protocol}")
            return protocol
        
        # Force BB84 if BB84 status file exists and is ready
        if os.path.exists("student_implementation_status.json"):
            try:
                with open("student_implementation_status.json", 'r') as f:
                    status = json.load(f)
                if status.get("student_implementation_ready") and status.get("protocol") == "bb84":
                    print("🔹 BB84 status file found and ready - forcing BB84 protocol")
                    self.current_protocol = "BB84"
                    self.detection_method = "forced_bb84"
                    return "BB84"
            except Exception as e:
                print(f"⚠️ Error checking BB84 status file: {e}")
        
        # Check if B92 status file is disabled
        if os.path.exists("student_b92_implementation_status.json.disabled"):
            print("🔹 B92 status file is disabled - forcing BB84 protocol")
            self.current_protocol = "BB84"
            self.detection_method = "b92_disabled_bb84"
            return "BB84"
        
        # Method 2: Check cell content if provided
        if cell_content:
            protocol = self.detect_from_cell_content(cell_content)
            if protocol:
                print(f"✅ Protocol detected from cell content: {protocol}")
                return protocol
        
        # Method 3: Check global variables
        protocol = self.detect_from_globals()
        if protocol:
            print(f"✅ Protocol detected from globals: {protocol}")
            return protocol
        
        # Default to BB84 if no clear detection
        print("⚠️ No clear protocol detected, defaulting to BB84")
        self.current_protocol = "BB84"
        self.detection_method = "default_bb84"
        return "BB84"
    
    def get_protocol_info(self) -> Dict[str, Any]:
        """
        Get information about the detected protocol
        """
        return {
            "protocol": self.current_protocol,
            "detection_method": self.detection_method,
            "bb84_indicators": self.bb84_indicators,
            "b92_indicators": self.b92_indicators
        }

def detect_qkd_protocol(cell_content: str = None) -> str:
    """
    Convenience function to detect QKD protocol
    """
    detector = ProtocolDetector()
    return detector.detect_protocol(cell_content)

def get_protocol_manager(protocol: str = None):
    """
    Get the appropriate protocol manager based on detected protocol
    """
    if protocol is None:
        protocol = detect_qkd_protocol()
    
    if protocol == "BB84":
        from bb84_impl import BB84ProtocolManager
        return BB84ProtocolManager()
    elif protocol == "B92":
        from b92_impl import B92ProtocolManager
        return B92ProtocolManager()
    else:
        raise ValueError(f"Unknown protocol: {protocol}")

# Export main functions
__all__ = ['ProtocolDetector', 'detect_qkd_protocol', 'get_protocol_manager']
