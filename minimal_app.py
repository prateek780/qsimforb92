from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Quantum Network Simulator Backend")

# Add CORS middleware for Binder compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Quantum Network Simulator Backend", 
        "status": "running",
        "environment": "binder",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok", 
        "backend": "running",
        "port": os.environ.get("PORT", "8080")
    }

@app.get("/api/test")
async def test_endpoint():
    return {
        "message": "Backend API is working!",
        "test": "successful",
        "binder": True
    }

# Additional endpoints for quantum simulation
@app.get("/api/quantum/status")
async def quantum_status():
    return {
        "quantum_simulator": "ready",
        "protocols": ["BB84", "B92"],
        "status": "operational"
    }
