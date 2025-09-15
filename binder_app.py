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

# Import your existing backend modules
try:
    from server.app import app as backend_app
    from server.routes import router as api_router
    print("✅ Backend modules imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import backend modules: {e}")
    # Create a minimal FastAPI app if backend modules aren't available
    backend_app = FastAPI(title="Quantum Networking API")

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

# Mount the API routes
try:
    app.mount("/api", backend_app)
    print("✅ API routes mounted at /api")
except Exception as e:
    print(f"⚠️ Could not mount API routes: {e}")

# Check if React build exists
react_build_path = current_dir / "ui" / "dist"
if react_build_path.exists():
    print(f"✅ React build found at: {react_build_path}")
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(react_build_path / "static")), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def serve_react_app():
        """Serve the React application"""
        return FileResponse(str(react_build_path / "index.html"))
    
    @app.get("/{path:path}")
    async def serve_react_routes(path: str):
        """Serve React routes (SPA routing)"""
        # Check if it's an API route
        if path.startswith("api/"):
            # Let the API handle it
            pass
        else:
            # Serve the React app for all other routes
            return FileResponse(str(react_build_path / "index.html"))
    
    print("✅ React app configured for SPA routing")
    
else:
    print("⚠️ React build not found, serving basic HTML")
    
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
    print(f"🌐 Server will be available at: http://localhost:5174")
    print(f"🔗 Binder proxy URL: https://mybinder.org/v2/gh/YOUR_USERNAME/YOUR_REPO/HEAD?urlpath=proxy/5174")
    
    uvicorn.run(
        "binder_app:app",
        host="0.0.0.0",
        port=5174,
        reload=False,  # Disable reload for Binder
        log_level="info"
    )
