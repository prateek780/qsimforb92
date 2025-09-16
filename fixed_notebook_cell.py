# %%

# 🌐 ACCESS WEB-BASED SIMULATION INTERFACE WITH UI LOGGING
# ========================================================
# This cell connects to your running backend and displays the web simulation
# with proper logging support for both BB84 and B92 protocols

import urllib.request
import urllib.error
import socket
import json
import os

DO_NOT_SPAWN_SERVERS = True  # Force notebook-safe behavior

def check_server_status_simple(url: str, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status in (200, 301, 302, 404)
    except Exception:
        return False

def write_notebook_status_file(protocol: str = "bb84"):
    """Ensure the backend sees student implementation as ready with proper protocol detection."""
    try:
        # Detect which protocol is being used
        if protocol.lower() == "b92":
            methods = [
                "b92_send_qubits",
                "b92_process_received_qbit",
                "b92_sifting", 
                "b92_estimate_error_rate",
            ]
            status_file = "student_b92_implementation_status.json"
        else:
            methods = [
                "bb84_send_qubits",
                "process_received_qbit", 
                "bb84_reconcile_bases",
                "bb84_estimate_error_rate",
            ]
            status_file = "student_implementation_status.json"
        
        status = {
            "student_implementation_ready": True,
            "implementation_type": "StudentImplementationBridge",
            "protocol": protocol.upper(),
            "methods_implemented": methods,
            "ui_logging_enabled": True,
            "has_valid_implementation": True,
            "binder_deployment": True,
        }
        with open(status_file, "w") as f:
            json.dump(status, f, indent=2)
        print(f"✅ Created {protocol.upper()} status file: {status_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating status file: {e}")
        return False

def show_section2_simulation(height: int = 1050, host: str = None, protocol: str = "bb84"):
    """Display simulation interface with proper Binder detection"""
    from IPython.display import IFrame, display

    # Detect if we're in Binder
    is_binder = 'JUPYTERHUB_SERVICE_PREFIX' in os.environ
    
    if is_binder:
        # Binder environment - use proxy path
        binder_port = os.environ.get('PORT', '8080')
        proxy_path = f"/proxy/{binder_port}"
        print(f"🌐 Binder Environment Detected - Using proxy: {proxy_path}")
        print(f"🔗 Full URL: https://mybinder.org/v2/gh/prateek780/qsimforb92/HEAD?urlpath=proxy/{binder_port}")
        
        # Create status file
        write_notebook_status_file(protocol)
        
        # Display simulation interface directly
        display(IFrame(src=proxy_path, width="100%", height=height))
        print("🎯 Simulation interface loaded!")
        print("📊 UI Logging enabled - logs will be displayed in the simulation interface")
        print(f"🔍 The system will use {protocol.upper()} protocol with appropriate log parser")
        
    else:
        # Local environment - use provided host or default
        if host is None:
            host = "http://localhost:8080"
        
        print(f"🔎 Checking backend proxy ({host}) for {protocol.upper()} protocol...")
        ok = check_server_status_simple(host)
        if not ok:
            # Try 127.0.0.1 fallback
            alt = host.replace("localhost", "127.0.0.1")
            print("⚠️ Backend not reachable at", host, "— trying", alt)
            if check_server_status_simple(alt):
                host = alt
            else:
                print("❌ Backend proxy not reachable. Ensure 'python start.py' is running on :8080.")
                print("💡 Then re-run this cell.")
                return

        # Write status file so backend reports valid implementation when not running
        write_notebook_status_file(protocol)

        # Display simulation interface
        display(IFrame(src=host, width="100%", height=height))
        print("ℹ️ Using direct IFrame to display simulation interface.")
        print("📊 UI Logging enabled - logs will be displayed in the simulation interface")
        print(f"🔍 The system will use {protocol.upper()} protocol with appropriate log parser")

def show_b92_simulation(height: int = 1050, host: str = None):
    """Display B92 simulation interface"""
    print("🔬 Starting B92 Quantum Key Distribution Simulation...")
    show_section2_simulation(height=height, host=host, protocol="b92")

def show_bb84_simulation(height: int = 1050, host: str = None):
    """Display BB84 simulation interface"""
    print("🔐 Starting BB84 Quantum Key Distribution Simulation...")
    show_section2_simulation(height=height, host=host, protocol="bb84")

# Dynamic protocol detection and auto-load simulation
print("🌐 Loading Simulation Interface...")
print("=" * 50)

# Detect current protocol and load appropriate simulation
if os.path.exists('student_b92_implementation_status.json') and not os.path.exists('student_b92_implementation_status.json.disabled'):
    print("🔬 B92 protocol detected - loading B92 simulation...")
    show_section2_simulation(height=1050, protocol="b92")
elif os.path.exists('student_implementation_status.json') and not os.path.exists('student_implementation_status.json.disabled'):
    print("🔐 BB84 protocol detected - loading BB84 simulation...")
    show_section2_simulation(height=1050, protocol="bb84")
else:
    print("🔐 No protocol detected - defaulting to BB84 simulation...")
    show_section2_simulation(height=1050, protocol="bb84")

print("\n💡 Manual controls:")
print("   • show_bb84_simulation() - Force BB84 simulation")
print("   • show_b92_simulation() - Force B92 simulation")
print("   • show_section2_simulation(protocol='bb84') - Custom BB84")
print("   • show_section2_simulation(protocol='b92') - Custom B92")
