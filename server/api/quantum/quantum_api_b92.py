"""
B92 Quantum API Routes
=====================

Handles B92-specific API endpoints for the quantum simulation.
Separate from the main quantum API to avoid conflicts with BB84.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from server.api.simulation.manager_b92 import b92_simulation_manager
from server.socket_server.socket_server_b92 import b92_connection_manager

router = APIRouter(prefix="/api/b92", tags=["B92 Quantum"])

@router.get("/events")
async def get_b92_events():
    """Get all B92 events"""
    try:
        events = b92_simulation_manager.get_b92_events()
        return {
            "success": True,
            "events": events,
            "count": len(events)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting B92 events: {str(e)}")

@router.get("/events/recent")
async def get_recent_b92_events(count: int = 100):
    """Get recent B92 events"""
    try:
        events = b92_simulation_manager.get_recent_b92_events(count)
        return {
            "success": True,
            "events": events,
            "count": len(events)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recent B92 events: {str(e)}")

@router.post("/simulation/start")
async def start_b92_simulation():
    """Start B92 simulation"""
    try:
        b92_simulation_manager.start_b92_simulation()
        return {
            "success": True,
            "message": "B92 simulation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting B92 simulation: {str(e)}")

@router.post("/simulation/stop")
async def stop_b92_simulation():
    """Stop B92 simulation"""
    try:
        b92_simulation_manager.stop_b92_simulation()
        return {
            "success": True,
            "message": "B92 simulation stopped"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping B92 simulation: {str(e)}")

@router.delete("/events")
async def clear_b92_events():
    """Clear all B92 events"""
    try:
        b92_simulation_manager.clear_b92_events()
        b92_connection_manager.clear_b92_events()
        return {
            "success": True,
            "message": "B92 events cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing B92 events: {str(e)}")

@router.get("/status")
async def get_b92_status():
    """Get B92 simulation status"""
    try:
        return {
            "success": True,
            "is_running": b92_simulation_manager.is_running,
            "event_count": len(b92_simulation_manager.b92_events),
            "connection_count": len(b92_connection_manager.active_connections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting B92 status: {str(e)}")
