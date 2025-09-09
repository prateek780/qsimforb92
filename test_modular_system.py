# test_modular_system.py
# ======================
# Test script for the modular QKD system

import sys
import os

def test_protocol_detection():
    """Test protocol detection system"""
    print("🧪 Testing Protocol Detection System")
    print("=" * 40)
    
    try:
        from protocol_detector import detect_qkd_protocol, get_protocol_manager
        
        # Test BB84 detection
        print("🔍 Testing BB84 detection...")
        protocol = detect_qkd_protocol("bb84_send_qubits StudentQuantumHost")
        print(f"   Detected: {protocol}")
        
        # Test B92 detection  
        print("🔍 Testing B92 detection...")
        protocol = detect_qkd_protocol("b92_send_qubits StudentB92Host")
        print(f"   Detected: {protocol}")
        
        print("✅ Protocol detection working!")
        return True
        
    except Exception as e:
        print(f"❌ Protocol detection failed: {e}")
        return False

def test_bb84_integration():
    """Test BB84 integration"""
    print("\n🧪 Testing BB84 Integration")
    print("=" * 40)
    
    try:
        from bb84_impl import BB84ProtocolManager
        
        manager = BB84ProtocolManager()
        print(f"   Created BB84 manager: {type(manager).__name__}")
        
        # Test student host creation
        alice, bob = manager.create_student_hosts("TestAlice", "TestBob")
        print(f"   Created hosts: {alice.name}, {bob.name}")
        
        # Test enhanced bridge creation
        bridge = manager.create_enhanced_bridge("TestAlice", "TestBob")
        print(f"   Created bridge: {type(bridge).__name__}")
        
        print("✅ BB84 integration working!")
        return True
        
    except Exception as e:
        print(f"❌ BB84 integration failed: {e}")
        return False

def test_b92_integration():
    """Test B92 integration"""
    print("\n🧪 Testing B92 Integration")
    print("=" * 40)
    
    try:
        from b92_impl import B92ProtocolManager
        
        manager = B92ProtocolManager()
        print(f"   Created B92 manager: {type(manager).__name__}")
        
        # Test student host creation
        alice, bob = manager.create_student_hosts("TestAlice", "TestBob")
        print(f"   Created hosts: {alice.name}, {bob.name}")
        
        # Test enhanced bridge creation
        bridge = manager.create_enhanced_bridge("TestAlice", "TestBob")
        print(f"   Created bridge: {type(bridge).__name__}")
        
        print("✅ B92 integration working!")
        return True
        
    except Exception as e:
        print(f"❌ B92 integration failed: {e}")
        return False

def test_unified_simulation():
    """Test unified simulation system"""
    print("\n🧪 Testing Unified Simulation System")
    print("=" * 40)
    
    try:
        from unified_simulation import UnifiedQKDSimulation
        
        simulation = UnifiedQKDSimulation()
        print(f"   Created unified simulation: {type(simulation).__name__}")
        
        # Test protocol detection
        protocol = simulation.detect_and_setup("bb84_send_qubits")
        print(f"   Detected protocol: {protocol}")
        
        # Test simulation info
        info = simulation.get_simulation_info()
        print(f"   Simulation info: {info}")
        
        print("✅ Unified simulation working!")
        return True
        
    except Exception as e:
        print(f"❌ Unified simulation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Modular QKD System")
    print("=" * 50)
    
    tests = [
        test_protocol_detection,
        test_bb84_integration,
        test_b92_integration,
        test_unified_simulation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modular system is working correctly!")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
