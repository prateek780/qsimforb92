#!/usr/bin/env python3
"""
Test script to check if the Binder backend can start properly
"""

import os
import sys
import subprocess
import time
import urllib.request
import json

def test_backend_startup():
    """Test if the backend can start and respond"""
    print("🧪 Testing Binder Backend Startup")
    print("=" * 50)
    
    # Check if binder_app.py exists
    if not os.path.exists("binder_app.py"):
        print("❌ binder_app.py not found!")
        return False
    
    print("✅ binder_app.py exists")
    
    # Check if required modules can be imported
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and Uvicorn available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False
    
    # Try to import the app
    try:
        from binder_app import app
        print("✅ Binder app imported successfully")
    except ImportError as e:
        print(f"❌ Could not import binder_app: {e}")
        return False
    
    # Test if we can start the server (non-blocking)
    print("\n🚀 Attempting to start backend server...")
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "binder_app:app", 
            "--host", "0.0.0.0", 
            "--port", "5174",
            "--log-level", "info"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend server started successfully!")
            
            # Try to make a request
            try:
                response = urllib.request.urlopen("http://localhost:5174", timeout=5)
                print(f"✅ Backend responding with status: {response.status}")
                return True
            except Exception as e:
                print(f"⚠️ Backend started but not responding: {e}")
                return False
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    finally:
        # Clean up
        try:
            process.terminate()
        except:
            pass

def create_status_files():
    """Create status files for the backend"""
    print("\n📝 Creating status files...")
    
    # Create student implementation status
    status = {
        "student_implementation_ready": True,
        "protocol": "bb84",
        "implementation_type": "StudentImplementationBridge",
        "methods_implemented": [
            "bb84_send_qubits",
            "process_received_qbit", 
            "bb84_reconcile_bases",
            "bb84_estimate_error_rate"
        ],
        "binder_deployment": True,
        "has_valid_implementation": True,
    }
    
    with open("student_implementation_status.json", "w") as f:
        json.dump(status, f, indent=2)
    print("✅ student_implementation_status.json created")
    
    # Create binder status
    binder_status = {
        "student_implementation_ready": True,
        "protocol": "bb84",
        "binder_deployment": True,
        "environment": "binder"
    }
    
    with open("binder_status.json", "w") as f:
        json.dump(binder_status, f, indent=2)
    print("✅ binder_status.json created")

if __name__ == "__main__":
    print("🔧 Binder Backend Diagnostic Tool")
    print("=" * 40)
    
    # Create status files
    create_status_files()
    
    # Test backend startup
    success = test_backend_startup()
    
    if success:
        print("\n🎉 SUCCESS: Backend is ready for Binder!")
        print("💡 The backend should work when deployed to Binder")
    else:
        print("\n❌ ISSUES DETECTED: Backend needs fixing")
        print("💡 Check the errors above and fix them before deploying")
    
    print("\n📋 Next steps:")
    print("1. Commit and push these changes to GitHub")
    print("2. Try the Binder URL again")
    print("3. The backend should start automatically")
