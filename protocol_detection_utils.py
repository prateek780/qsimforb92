#!/usr/bin/env python3
"""
Protocol Detection Utilities
============================
Centralized protocol detection for the entire quantum networking system.
This eliminates duplicate protocol detection logic across multiple files.
"""

import os
import json
from typing import Optional

def detect_active_protocol() -> str:
    """
    Centralized protocol detection function.
    
    This is the SINGLE SOURCE OF TRUTH for protocol detection.
    All other files should use this function instead of implementing
    their own protocol detection logic.
    
    Returns:
        str: "BB84", "B92", or "BB84" (default)
    """
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

def get_protocol_info() -> dict:
    """
    Get detailed protocol information for debugging.
    
    Returns:
        dict: Protocol information including detection method and status
    """
    info = {
        "active_protocol": detect_active_protocol(),
        "bb84_status": {},
        "b92_status": {},
        "detection_method": "unknown"
    }
    
    # Check BB84 status
    if os.path.exists("student_implementation_status.json"):
        try:
            with open("student_implementation_status.json", "r") as f:
                info["bb84_status"] = json.load(f)
        except Exception:
            pass
    
    # Check B92 status
    if os.path.exists("student_b92_implementation_status.json"):
        try:
            with open("student_b92_implementation_status.json", "r") as f:
                info["b92_status"] = json.load(f)
        except Exception:
            pass
    elif os.path.exists("student_b92_implementation_status.json.disabled"):
        info["b92_status"] = {"status": "disabled"}
    
    # Determine detection method
    if info["bb84_status"].get("student_implementation_ready") and info["bb84_status"].get("protocol") == "bb84":
        info["detection_method"] = "bb84_status_file"
    elif info["b92_status"].get("student_implementation_ready"):
        info["detection_method"] = "b92_status_file"
    elif os.path.exists("student_b92_implementation_status.json.disabled"):
        info["detection_method"] = "b92_disabled_default_bb84"
    else:
        info["detection_method"] = "default_bb84"
    
    return info

def print_protocol_status():
    """
    Print current protocol status for debugging.
    """
    info = get_protocol_info()
    print("🔍 Protocol Detection Status:")
    print("=" * 40)
    print(f"🎯 Active Protocol: {info['active_protocol']}")
    print(f"🔧 Detection Method: {info['detection_method']}")
    
    if info["bb84_status"]:
        ready = info["bb84_status"].get("student_implementation_ready", False)
        protocol = info["bb84_status"].get("protocol", "unknown")
        print(f"🔐 BB84 Status: Ready={ready}, Protocol={protocol}")
    else:
        print("🔐 BB84 Status: No status file")
    
    if info["b92_status"]:
        if info["b92_status"].get("status") == "disabled":
            print("🔬 B92 Status: Disabled")
        else:
            ready = info["b92_status"].get("student_implementation_ready", False)
            print(f"🔬 B92 Status: Ready={ready}")
    else:
        print("🔬 B92 Status: No status file")

if __name__ == "__main__":
    print_protocol_status()
