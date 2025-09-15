"""
Simple B92 Quantum API Routes
============================

Simplified B92 API endpoints without WebSocket dependencies
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/b92", tags=["B92 Quantum Simple"])

@router.get("/status")
async def get_b92_status():
    """Get B92 simulation status (simplified)"""
    try:
        return {
            "success": True,
            "is_running": False,
            "event_count": 0,
            "connection_count": 0,
            "message": "B92 simulation ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting B92 status: {str(e)}")

@router.get("/events")
async def get_b92_events():
    """Get all B92 events (simplified)"""
    try:
        return {
            "success": True,
            "events": [],
            "count": 0,
            "message": "No events yet"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting B92 events: {str(e)}")

@router.get("/events/recent")
async def get_recent_b92_events(count: int = 100):
    """Get recent B92 events (simplified)"""
    try:
        return {
            "success": True,
            "events": [],
            "count": 0,
            "message": "No events yet"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recent B92 events: {str(e)}")

@router.post("/simulation/start")
async def start_b92_simulation():
    """Start B92 simulation (simplified)"""
    try:
        return {
            "success": True,
            "message": "B92 simulation started (simplified mode)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting B92 simulation: {str(e)}")

@router.post("/simulation/stop")
async def stop_b92_simulation():
    """Stop B92 simulation (simplified)"""
    try:
        return {
            "success": True,
            "message": "B92 simulation stopped (simplified mode)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping B92 simulation: {str(e)}")

@router.delete("/events")
async def clear_b92_events():
    """Clear all B92 events (simplified)"""
    try:
        return {
            "success": True,
            "message": "B92 events cleared (simplified mode)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing B92 events: {str(e)}")


