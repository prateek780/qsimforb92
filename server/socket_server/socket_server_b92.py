"""
B92 Socket Server
================

Handles B92-specific WebSocket events and connections.
Separate from the main socket server to avoid conflicts with BB84.
"""

import asyncio
import json
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from utils.singleton import singleton
from core.event_b92 import B92Event, B92EventType


@singleton
class B92ConnectionManager:
    """Manages B92-specific WebSocket connections"""
    
    def __init__(self):
        # Store active WebSocket connections for B92
        self.active_connections: List[WebSocket] = []
        self.b92_events: List[Dict[str, Any]] = []
        self.max_events = 1000
        
        # B92 simulation manager will connect to this socket manager

    async def connect(self, websocket: WebSocket):
        """Accepts a new WebSocket connection for B92 events"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New B92 connection accepted: {websocket.client}")
        
        # Send recent B92 events to the new connection
        await self._send_recent_b92_events(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection from B92 connections"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"B92 connection closed: {websocket.client}")

    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """Sends a B92 message to a specific WebSocket"""
        try:
            if isinstance(message, str):
                await websocket.send_text(message)
            else:
                await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending B92 personal message to {websocket.client}: {e}")

    async def broadcast(self, message: Any):
        """Broadcasts B92 messages to all active connections"""
        if not self.active_connections:
            return
            
        # Create tasks for sending messages concurrently
        tasks = []
        disconnected_clients = []

        # First log the B92 message
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "b92_event",
                "data": message
            }
            self.b92_events.append(log_entry)
            if len(self.b92_events) > self.max_events:
                self.b92_events.pop(0)
        except Exception as e:
            print(f"Error logging B92 message: {e}")

        # Send to all connections
        for connection in self.active_connections:
            task = asyncio.create_task(self._send_to_connection(connection, message))
            tasks.append(task)

        # Wait for all tasks to complete
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Remove disconnected clients
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    disconnected_clients.append(self.active_connections[i])
            
            for client in disconnected_clients:
                self.disconnect(client)

    async def _send_to_connection(self, connection: WebSocket, message: Any):
        """Send message to a specific connection"""
        try:
            if isinstance(message, str):
                await connection.send_text(message)
            else:
                await connection.send_json(message)
        except WebSocketDisconnect:
            raise
        except Exception as e:
            print(f"Error sending B92 message to {connection.client}: {e}")
            raise

    async def _send_recent_b92_events(self, websocket: WebSocket):
        """Send recent B92 events to a new connection"""
        try:
            # Send recent events from local storage
            recent_events = self.b92_events[-50:] if self.b92_events else []
            for event in recent_events:
                await self.send_personal_message(event, websocket)
        except Exception as e:
            print(f"Error sending recent B92 events: {e}")

    def get_b92_events(self) -> List[Dict[str, Any]]:
        """Get all B92 events"""
        return self.b92_events.copy()

    def clear_b92_events(self):
        """Clear all B92 events"""
        self.b92_events.clear()


# Global B92 connection manager instance
b92_connection_manager = B92ConnectionManager()
