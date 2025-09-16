"""
Binder-compatible FastAPI application
Serves both the React frontend and API endpoints
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Create a simple backend app without complex dependencies
backend_app = FastAPI(title="Quantum Networking API")
print("Simple backend app created")

# Create the main app
app = FastAPI(
    title="Quantum Networking System",
    description="Complete quantum networking simulation with BB84/B92 protocols",
    version="1.0.0"
)

# Add CORS middleware for Binder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Binder
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add simple API routes directly to main app
@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "status": "running",
        "backend": "FastAPI",
        "protocols": ["BB84", "B92"],
        "binder_deployment": True,
        "student_implementation_ready": True
    }

@app.get("/api/bb84")
async def get_bb84_info():
    """Get BB84 protocol information"""
    return {
        "protocol": "BB84",
        "description": "Quantum Key Distribution Protocol",
        "states": ["|0⟩", "|1⟩", "|+⟩", "|-⟩"],
        "bases": ["Z-basis (rectilinear)", "X-basis (diagonal)"],
        "security": "Unconditional security based on quantum mechanics"
    }

@app.get("/api/b92")
async def get_b92_info():
    """Get B92 protocol information"""
    return {
        "protocol": "B92",
        "description": "Simplified Quantum Key Distribution Protocol",
        "states": ["|0⟩", "|+⟩"],
        "bases": ["Z-basis", "X-basis"],
        "security": "Based on non-orthogonal quantum states"
    }

print("API routes added")

# Always serve simple HTML interface (no React dependency)
print("Serving simple HTML interface")

@app.get("/", response_class=HTMLResponse)
async def serve_basic_app():
    """Serve a basic HTML page when React build is not available"""
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quantum Networking System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; }
                .content { margin: 20px 0; }
                .api-link { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
                .api-link a { color: #007bff; text-decoration: none; }
                .api-link a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 Quantum Networking System</h1>
                    <p>Complete quantum networking simulation with BB84/B92 protocols</p>
                </div>
                <div class="content">
                    <h2>🚀 System Status</h2>
                    <p>✅ FastAPI backend is running</p>
                    <p>⚠️ React frontend build not found</p>
                    <p>💡 This is normal for Binder deployment</p>
                    
                    <h2>🔗 Available Endpoints</h2>
                    <div class="api-link">
                        <strong>API Documentation:</strong> <a href="/api/docs" target="_blank">/api/docs</a>
                    </div>
                    <div class="api-link">
                        <strong>API Health Check:</strong> <a href="/api/health" target="_blank">/api/health</a>
                    </div>
                    <div class="api-link">
                        <strong>Simulation Status:</strong> <a href="/api/simulation/status" target="_blank">/api/simulation/status</a>
                    </div>
                    
                    <h2>📚 Next Steps</h2>
                    <p>1. Open the Jupyter notebook: <code>quantum_networking_complete.ipynb</code></p>
                    <p>2. Run the cells to start the quantum simulation</p>
                    <p>3. Use the chatbot for code generation and help</p>
                </div>
            </div>
        </body>
        </html>
        """

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Binder"""
    return {
        "status": "healthy",
        "service": "quantum-networking",
        "version": "1.0.0",
        "binder": True
    }

# Example API endpoint
@app.get("/api/hello")
async def hello_world():
    """Example API endpoint"""
    return {
        "message": "Hello from Quantum Networking System!",
        "status": "running",
        "binder": True
    }

if __name__ == "__main__":
    # Run the app
    print("🚀 Starting Quantum Networking System for Binder...")
    print(f"📁 Working directory: {current_dir}")
    port = int(os.environ.get("PORT", "8080"))
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"🔗 Binder proxy URL: https://mybinder.org/v2/gh/YOUR_USERNAME/YOUR_REPO/HEAD?urlpath=proxy/{port}")
    
    uvicorn.run(
        "binder_app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        reload=False,  # Disable reload for Binder
        log_level="info"
    )
