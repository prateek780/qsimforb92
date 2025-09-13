# 🔄 UNIFIED PROTOCOL RUNNER
# ==========================
# This file provides a unified interface for running both BB84 and B92 protocols
# while maintaining compatibility with the existing system

import sys
import os
import json
import time
import argparse

def check_protocol_completion(protocol):
    """Check if a protocol has been completed"""
    protocol_file = f"{protocol}_done.json"
    if os.path.exists(protocol_file):
        try:
            with open(protocol_file, 'r') as f:
                data = json.load(f)
                if data.get("status") == "completed":
                    print(f"✅ {protocol.upper()} protocol completed!")
                    return True
        except Exception as e:
            print(f"⚠️ Error reading {protocol} status: {e}")
    return False

def create_protocol_completion_file(protocol):
    """Create a protocol completion file"""
    protocol_file = f"{protocol}_done.json"
    protocol_data = {
        "protocol": protocol,
        "status": "completed",
        "timestamp": "2025-01-10T22:15:00Z"
    }
    with open(protocol_file, 'w') as f:
        json.dump(protocol_data, f, indent=2)
    print(f"✅ Created {protocol.upper()} completion file")

def run_bb84_simulation():
    """Run BB84 simulation using existing infrastructure"""
    print("🔬 BB84 QUANTUM SIMULATION")
    print("=" * 40)
    
    # Ensure we can import from current directory  
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    try:
        from complete_quantum_simulation import run_complete_quantum_simulation_with_instances
        from student_bb84_impl import StudentQuantumHost
        
        # Create BB84 student hosts
        print("🔹 Creating BB84 student hosts...")
        alice_bb84 = StudentQuantumHost("Alice")
        bob_bb84 = StudentQuantumHost("Bob")
        print("✅ BB84 student hosts created")
        
        # Run BB84 simulation
        print("🚀 Starting BB84 simulation...")
        success = run_complete_quantum_simulation_with_instances(alice_bb84, bob_bb84)
        
        if success:
            print("🎉 BB84 simulation completed successfully!")
            create_protocol_completion_file("bb84")
            return True
        else:
            print("❌ BB84 simulation encountered issues")
            return False
            
    except Exception as e:
        print(f"❌ Error running BB84 simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_b92_simulation():
    """Run B92 simulation using existing infrastructure"""
    print("🔬 B92 QUANTUM SIMULATION")
    print("=" * 40)
    
    # Check if BB84 is completed first
    if not check_protocol_completion("bb84"):
        print("❌ BB84 protocol must be completed before running B92!")
        print("💡 Run: python unified_protocol_runner.py --protocol bb84")
        return False
    
    # Ensure we can import from current directory  
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    try:
        from complete_quantum_simulation import run_complete_quantum_simulation_with_instances
        from student_b92_impl import StudentB92Host
        
        # Create B92 student hosts
        print("🔹 Creating B92 student hosts...")
        alice_b92 = StudentB92Host("Alice")
        bob_b92 = StudentB92Host("Bob")
        print("✅ B92 student hosts created")
        
        # Run B92 simulation
        print("🚀 Starting B92 simulation...")
        success = run_complete_quantum_simulation_with_instances(alice_b92, bob_b92)
        
        if success:
            print("🎉 B92 simulation completed successfully!")
            create_protocol_completion_file("b92")
            return True
        else:
            print("❌ B92 simulation encountered issues")
            return False
            
    except Exception as e:
        print(f"❌ Error running B92 simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_both_protocols():
    """Run both BB84 and B92 protocols in sequence"""
    print("🔄 RUNNING BOTH PROTOCOLS")
    print("=" * 50)
    
    # Run BB84 first
    print("🔬 Step 1: Running BB84 protocol...")
    bb84_success = run_bb84_simulation()
    
    if not bb84_success:
        print("❌ BB84 failed, cannot proceed to B92")
        return False
    
    print("\n🔬 Step 2: Running B92 protocol...")
    b92_success = run_b92_simulation()
    
    if bb84_success and b92_success:
        print("\n🎉 BOTH PROTOCOLS COMPLETED SUCCESSFULLY!")
        print("✅ BB84 and B92 implementations are working perfectly!")
        return True
    else:
        print("\n❌ Some protocols failed")
        return False

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Unified Protocol Runner for BB84 and B92")
    parser.add_argument("--protocol", choices=["bb84", "b92", "both"], 
                       default="both", help="Protocol to run")
    parser.add_argument("--check", action="store_true", 
                       help="Check protocol completion status")
    
    args = parser.parse_args()
    
    if args.check:
        print("🔍 CHECKING PROTOCOL STATUS")
        print("=" * 40)
        bb84_done = check_protocol_completion("bb84")
        b92_done = check_protocol_completion("b92")
        
        print(f"BB84: {'✅ Completed' if bb84_done else '❌ Not completed'}")
        print(f"B92: {'✅ Completed' if b92_done else '❌ Not completed'}")
        return
    
    if args.protocol == "bb84":
        success = run_bb84_simulation()
    elif args.protocol == "b92":
        success = run_b92_simulation()
    elif args.protocol == "both":
        success = run_both_protocols()
    
    if success:
        print("\n🎉 PROTOCOL(S) COMPLETED SUCCESSFULLY!")
    else:
        print("\n❌ Protocol execution failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
