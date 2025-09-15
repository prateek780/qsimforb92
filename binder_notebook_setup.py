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
    binder_port = os.environ.get('BINDER_PORT', '5174')
    
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
