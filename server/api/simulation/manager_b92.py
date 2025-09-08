"""
B92 Simulation Manager
=====================

Handles B92-specific simulation management and event broadcasting.
Separate from the main simulation manager to avoid conflicts with BB84.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.event_b92 import B92Event, B92EventType
from core.world_b92 import b92_event_manager
from server.socket_server.socket_server import ConnectionManager


class B92SimulationManager:
    """Manages B92 simulation events and WebSocket broadcasting"""
    
    def __init__(self):
        self.socket_conn: Optional[ConnectionManager] = None
        self.is_running = False
        self.b92_events: List[B92Event] = []
        self.max_events = 1000
        
        # Register with B92 event manager
        b92_event_manager.add_event_listener(self._handle_b92_event)
    
    def set_socket_connection(self, socket_conn: ConnectionManager):
        """Set the WebSocket connection manager"""
        self.socket_conn = socket_conn
    
    def _handle_b92_event(self, event: B92Event):
        """Handle incoming B92 events"""
        # Add to local event list
        self.b92_events.append(event)
        if len(self.b92_events) > self.max_events:
            self.b92_events.pop(0)
        
        # Broadcast to WebSocket clients
        if self.socket_conn:
            asyncio.create_task(self._broadcast_b92_event(event))
    
    async def _broadcast_b92_event(self, event: B92Event):
        """Broadcast B92 event to all WebSocket clients"""
        try:
            if self.socket_conn:
                message = event.to_websocket_message()
                await self.socket_conn.broadcast(message)
                print(f"B92 Event broadcasted: {event.event_type.value} from {event.node.name}")
        except Exception as e:
            print(f"Error broadcasting B92 event: {e}")
    
    def emit_b92_student_event(self, event_type: B92EventType, node, message: str, **kwargs):
        """Emit a B92 student implementation event"""
        return b92_event_manager.emit_b92_student_event(event_type, node, message, **kwargs)
    
    def get_b92_events(self) -> List[Dict[str, Any]]:
        """Get all B92 events as dictionaries"""
        return [event.to_dict() for event in self.b92_events]
    
    def get_recent_b92_events(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get recent B92 events as dictionaries"""
        recent_events = self.b92_events[-count:] if self.b92_events else []
        return [event.to_dict() for event in recent_events]
    
    def start_b92_simulation(self):
        """Start B92 simulation"""
        self.is_running = True
        print("B92 Simulation Manager started")
    
    def stop_b92_simulation(self):
        """Stop B92 simulation"""
        self.is_running = False
        print("B92 Simulation Manager stopped")
    
    def clear_b92_events(self):
        """Clear all B92 events"""
        self.b92_events.clear()
        b92_event_manager.clear_history()


# Global B92 simulation manager instance
b92_simulation_manager = B92SimulationManager()
