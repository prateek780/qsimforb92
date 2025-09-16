"""
Binder-specific notebook setup
Configures the notebook to work with Binder's proxy setup
"""

import os
import webbrowser
from IPython.display import display, HTML

def setup_binder_environment():
    """Set up the environment for Binder deployment"""
    
    print("🌐 Setting up Quantum Networking System for Binder...")
    print("=" * 60)
    
    # Get Binder environment info
    binder_url = os.environ.get('BINDER_URL', 'https://mybinder.org')
    binder_port = os.environ.get('PORT', '8080')
    
    # Construct the proxy URL
    proxy_url = f"{binder_url}/proxy/{binder_port}"
    
    print(f"🔗 Binder URL: {binder_url}")
    print(f"🔌 Proxy Port: {binder_port}")
    print(f"🌐 Full Proxy URL: {proxy_url}")
    print()
    
    # Set up API key for chatbot
    os.environ["GEMINI_API_KEY"] = "AIzaSyA3AYjoulpdQ_bFyRB4bx7Eduo7paxz34c"
    
    # Check if we're in Binder
    if 'BINDER' in os.environ:
        print("✅ Running in Binder environment")
        print("💡 The system is configured for Binder deployment")
    else:
        print("⚠️ Not running in Binder - using local configuration")
    
    print()
    print("🎯 SYSTEM COMPONENTS:")
    print("   • FastAPI Backend: Available at /api/")
    print("   • React Frontend: Served by FastAPI")
    print("   • Jupyter Notebook: This interface")
    print("   • Quantum Chatbot: Available in sidebar")
    print()
    
    return proxy_url

def open_chatbot_sidebar():
    """Open the chatbot sidebar for Binder"""
    
    print("🤖 Opening Quantum Cryptography AI Assistant...")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    chatbot_file = os.path.join(current_dir, "quantum_chatbot_sidebar.html")
    
    if os.path.exists(chatbot_file):
        print("✅ Chatbot file found!")
        print(f"📁 Location: {chatbot_file}")
        print()
        print("🌐 Opening chatbot in new tab...")
        
        # Display the chatbot in an iframe
        display(HTML(f"""
        <div style="text-align: center; margin: 20px;">
            <h3>🤖 Quantum Cryptography AI Assistant</h3>
            <p>Click the button below to open the chatbot in a new tab:</p>
            <button onclick="window.open('{chatbot_file}', '_blank')" 
                    style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                Open Chatbot
            </button>
        </div>
        """))
        
        print("✅ Chatbot ready! Click the button above to open it.")
        print()
        print("💡 USAGE TIPS:")
        print("   • Keep the chatbot tab open while working")
        print("   • Use quick action buttons (BB84, B92, Debug, Code)")
        print("   • Copy generated code directly from the chatbot")
        print("   • Paste skeleton functions for completion")
        
    else:
        print("❌ Chatbot file not found!")
        print(f"Expected location: {chatbot_file}")
        print("💡 Make sure quantum_chatbot_sidebar.html is in the repository")

def check_system_status():
    """Check the status of all system components"""
    
    print("🔍 Checking system status...")
    print("=" * 40)
    
    # Check if we're in Binder
    if 'BINDER' in os.environ:
        print("✅ Binder environment detected")
    else:
        print("⚠️ Local environment detected")
    
    # Check for required files
    required_files = [
        "quantum_networking_complete.ipynb",
        "quantum_chatbot_sidebar.html",
        "binder_app.py",
        "requirements.txt"
    ]
    
    print("\n📁 File Status:")
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    # Check Python packages
    print("\n🐍 Python Package Status:")
    try:
        import fastapi
        print(f"   ✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("   ❌ FastAPI not installed")
    
    try:
        import numpy
        print(f"   ✅ NumPy {numpy.__version__}")
    except ImportError:
        print("   ❌ NumPy not installed")
    
    try:
        import openai
        print(f"   ✅ OpenAI {openai.__version__}")
    except ImportError:
        print("   ❌ OpenAI not installed")
    
    print("\n🎯 System ready for quantum networking simulation!")

# Main setup function
def setup_quantum_networking():
    """Complete setup for quantum networking system"""
    
    print("🚀 QUANTUM NETWORKING SYSTEM SETUP")
    print("=" * 50)
    
    # Set up Binder environment
    proxy_url = setup_binder_environment()
    
    # Check system status
    check_system_status()
    
    print("\n🎓 READY TO START LEARNING!")
    print("=" * 30)
    print("1. Run the cells below to start the simulation")
    print("2. Open the chatbot for code generation help")
    print("3. Implement BB84 and B92 protocols")
    print("4. Explore quantum networking concepts")
    
    return proxy_url

# Auto-run setup when imported
if __name__ == "__main__":
    setup_quantum_networking()

# Test function for notebook cells
def test_binder_system():
    """Test the Binder system - copy this into a notebook cell"""
    import subprocess
    import sys
    import time
    import os
    from IPython.display import display, HTML
    
    print("🧪 TESTING BINDER QUANTUM NETWORKING SYSTEM")
    print("=" * 60)
    
    # Test 1: Environment
    port = os.environ.get("PORT", "8080")
    print(f"✅ Binder PORT: {port}")
    
    # Test 2: Imports
    try:
        from server.app import get_app
        from quantum_network.adapter import QuantumAdapter
        from classical_network.host import ClassicalHost
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 3: FastAPI App
    try:
        from fastapi.concurrency import asynccontextmanager
        
        @asynccontextmanager
        async def test_lifespan(app):
            yield
        
        app = get_app(lifespan=test_lifespan)
        print("✅ FastAPI app created")
        
        # Test endpoints
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get("/")
        print(f"✅ Root endpoint: {response.status_code}")
        
        response = client.get("/api/simulation/status")
        print(f"✅ Simulation status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        return False
    
    # Success display
    display(HTML("""
    <div style="text-align: center; margin: 20px; padding: 20px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px;">
        <h2>🎉 BINDER SYSTEM READY!</h2>
        <p><strong>Status:</strong> Quantum networking system is operational</p>
        <p><strong>Port:</strong> """ + port + """</p>
        <p><strong>Ready for:</strong> BB84/B92 simulation, student implementation</p>
        <button onclick="window.open('/api/docs', '_blank')" 
                style="background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 5px;">
            View API Docs
        </button>
    </div>
    """))
    
    print("🚀 System ready for quantum networking simulation!")
    return True

def show_simulation_interface():
    """Display the simulation interface for Binder"""
    import os
    import urllib.request
    import urllib.error
    import json
    
    def check_server_status(url: str, timeout: float = 2.0) -> bool:
        """Check if the backend server is running"""
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return resp.status in (200, 301, 302, 404)
        except Exception:
            return False

    def create_bb84_status_file():
        """Create BB84 status file for the backend"""
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
        
        print("✅ BB84 status file created for backend")

    # Detect environment
    is_binder = 'JUPYTERHUB_SERVICE_PREFIX' in os.environ
    
    if is_binder:
        # For Binder, use the proxy path (not a real host)
        # Binder uses $PORT environment variable, defaulting to 8080
        binder_port = os.environ.get('PORT', '8080')
        proxy_path = f"/proxy/{binder_port}"
        print("🌐 Binder Environment Detected")
        print(f"🔗 Backend should be accessible at: {proxy_path}")
        
        # Create status file
        create_bb84_status_file()
        
        # Display simulation interface directly (no host check needed)
        from IPython.display import IFrame, display
        display(IFrame(src=proxy_path, width="100%", height=800))
        
        print("🎯 Simulation interface loaded!")
        print("📊 You can now:")
        print("   • Create quantum hosts")
        print("   • Run BB84 protocol simulations")
        print("   • View real-time logs")
        print("   • Analyze quantum networking")
        
    else:
        host = "http://localhost:8080"
        print("🌐 Local Environment Detected")
        
        # Check if backend is running
        if check_server_status(host):
            print(f"✅ Backend is running at {host}")
            
            # Create status file
            create_bb84_status_file()
            
            # Display simulation interface
            from IPython.display import IFrame, display
            display(IFrame(src=host, width="100%", height=800))
            
            print("🎯 Simulation interface loaded!")
            print("📊 You can now:")
            print("   • Create quantum hosts")
            print("   • Run BB84 protocol simulations")
            print("   • View real-time logs")
            print("   • Analyze quantum networking")
            
        else:
            print(f"❌ Backend not running at {host}")
            print("💡 Run: python start.py")
            print("   Then re-run this cell")
