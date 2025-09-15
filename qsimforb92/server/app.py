from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.socket_server.socket_server import websocket_endpoint

REACT_BUILD_FOLDER = "../ui/dist"

# Create a new app factory function
def get_app(lifespan):
    app = FastAPI(title="Network Simulator API", version="1.0.0", lifespan=lifespan)
    
    # Add CORS middleware with specific configuration for WebSocket
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with your frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    
    # Register routes
    from server.routes import register_routes
    register_routes(app)
    
    # Register B92 routes AFTER main routes to avoid catch-all route conflicts
    from server.routes_b92 import router as b92_router
    app.include_router(b92_router)
    
    # Register B92 API routes AFTER main routes to avoid catch-all route conflicts
    # Use simplified B92 API routes to avoid WebSocket connection issues
    from server.api.quantum.quantum_api_b92_simple import router as b92_api_router
    app.include_router(b92_api_router)
    
    
    
    # Add WebSocket route with explicit configuration
    from fastapi import WebSocket
    @app.websocket("/ws")  # Changed from /api/ws to /ws
    async def websocket_route(websocket: WebSocket):
        await websocket_endpoint(websocket)
        
    @app.websocket("/api/ws")  # Keep old endpoint for compatibility
    async def websocket_route_api(websocket: WebSocket):
        await websocket_endpoint(websocket)
    
    # Add route for simulation status
    @app.get("/api/simulation/status")
    async def get_simulation_status():
        try:
            from server.api.simulation.manager import SimulationManager
            manager = SimulationManager.get_instance()
            
            if manager is None:
                return {
                    "is_running": False,
                    "status": "not_initialized",
                    "message": "Simulation manager not available"
                }
            
            return {
                "is_running": getattr(manager, 'is_running', False),
                "status": "running" if getattr(manager, 'is_running', False) else "stopped",
                "message": "Simulation is running" if getattr(manager, 'is_running', False) else "Simulation is stopped"
            }
        except Exception as e:
            print(f"Error getting simulation status: {e}")
            import traceback
            traceback.print_exc()
            return {
                "is_running": False,
                "status": "error",
                "message": f"Error getting simulation status: {str(e)}"
            }
    
    return app
