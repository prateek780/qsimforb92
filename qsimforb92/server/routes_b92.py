"""
B92 WebSocket Routes
===================

Handles B92-specific WebSocket connections.
Separate from the main routes to avoid conflicts with BB84.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from server.socket_server.socket_server_b92 import b92_connection_manager

router = APIRouter()

@router.websocket("/ws/b92")
async def websocket_b92_endpoint(websocket: WebSocket):
    """B92 WebSocket endpoint"""
    await b92_connection_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        b92_connection_manager.disconnect(websocket)
    except Exception as e:
        print(f"B92 WebSocket error: {e}")
        b92_connection_manager.disconnect(websocket)
