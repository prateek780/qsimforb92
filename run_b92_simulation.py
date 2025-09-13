# 🚀 B92 QUANTUM SIMULATION RUNNER
# =================================
# This file runs the B92 simulation using the existing infrastructure
# while preserving BB84 functionality

import sys
import os
import json
import time

def run_b92_simulation():
    """
    Run B92 simulation using the existing complete_quantum_simulation.py
    but with B92-specific implementations
    """
    print("🔬 B92 QUANTUM SIMULATION RUNNER")
    print("=" * 50)
    
    # Ensure we can import from current directory  
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    # Check if BB84 is completed
    bb84_file = "bb84_done.json"
    if not os.path.exists(bb84_file):
        print("❌ BB84 protocol not completed yet!")
        print("💡 Please complete BB84 implementation first")
        return False
    
    try:
        with open(bb84_file, 'r') as f:
            bb84_data = json.load(f)
            if bb84_data.get("status") != "completed":
                print("❌ BB84 protocol not completed yet!")
                return False
    except Exception as e:
        print(f"❌ Error reading BB84 status: {e}")
        return False
    
    print("✅ BB84 protocol completed! Starting B92 simulation...")
    
    # Import B92-specific components
    try:
        from student_b92_impl import StudentB92Host
        from enhancedb92_bridge import EnhancedB92Bridge
        from b92_impl import B92ProtocolManager
        print("✅ B92 components imported successfully")
    except ImportError as e:
        print(f"❌ Error importing B92 components: {e}")
        return False
    
    # Create B92 student hosts
    print("🔹 Creating B92 student hosts...")
    alice_b92 = StudentB92Host("Alice")
    bob_b92 = StudentB92Host("Bob")
    print("✅ B92 student hosts created")
    
    # Create B92 enhanced bridge
    print("🔹 Creating B92 enhanced bridge...")
    b92_bridge = EnhancedB92Bridge(
        student_alice=alice_b92,
        student_bob=bob_b92,
        alice_name="Alice",
        bob_name="Bob"
    )
    print("✅ B92 enhanced bridge created")
    
    # Create B92 protocol manager
    print("🔹 Setting up B92 protocol manager...")
    b92_manager = B92ProtocolManager()
    b92_manager.student_alice = alice_b92
    b92_manager.student_bob = bob_b92
    b92_manager.enhanced_bridge = b92_bridge
    print("✅ B92 protocol manager ready")
    
    # Write B92 status file
    print("🔹 Writing B92 status file...")
    b92_manager.write_status_file()
    
    # Import and run the complete simulation with B92
    try:
        from complete_quantum_simulation import run_complete_quantum_simulation_with_instances
        
        print("🚀 Starting B92 simulation with complete quantum network...")
        success = run_complete_quantum_simulation_with_instances(alice_b92, bob_b92)
        
        if success:
            print("🎉 B92 simulation completed successfully!")
            print("✅ Your B92 implementation worked perfectly!")
            
            # Create B92 completion file
            b92_file = "b92_done.json"
            b92_data = {
                "protocol": "b92",
                "status": "completed",
                "timestamp": "2025-01-10T22:15:00Z"
            }
            with open(b92_file, 'w') as f:
                json.dump(b92_data, f, indent=2)
            print("✅ B92 completion file created")
            
            return True
        else:
            print("❌ B92 simulation encountered issues")
            return False
            
    except Exception as e:
        print(f"❌ Error running B92 simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_b92_simulation()
    if success:
        print("\n🎉 B92 PROTOCOL COMPLETED SUCCESSFULLY!")
        print("✅ Your B92 implementation is working perfectly!")
    else:
        print("\n❌ B92 simulation failed")
        print("💡 Check the error messages above for debugging")
