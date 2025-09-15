"""
B92 World Event Manager
======================

Handles B92-specific event emission and broadcasting.
Separate from the main world system to avoid conflicts with BB84.
"""

import time
from typing import List, Dict, Any, Optional
from core.event_b92 import B92Event, B92EventType, LogLevel


class B92WorldEventManager:
    """Manages B92 events in the simulation world"""
    
    def __init__(self):
        self.event_listeners: List[callable] = []
        self.event_history: List[B92Event] = []
        self.max_history_size = 1000
        
    def add_event_listener(self, listener: callable):
        """Add an event listener"""
        if listener not in self.event_listeners:
            self.event_listeners.append(listener)
    
    def remove_event_listener(self, listener: callable):
        """Remove an event listener"""
        if listener in self.event_listeners:
            self.event_listeners.remove(listener)
    
    def emit_b92_event(self, event: B92Event):
        """Emit a B92 event to all listeners"""
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history_size:
            self.event_history.pop(0)
        
        # Notify all listeners
        for listener in self.event_listeners:
            try:
                listener(event)
            except Exception as e:
                print(f"Error in B92 event listener: {e}")
    
    def create_b92_event(self, event_type: B92EventType, node, **kwargs) -> B92Event:
        """Create a new B92 event"""
        return B92Event(event_type, node, **kwargs)
    
    def emit_b92_student_event(self, event_type: B92EventType, node, message: str, **kwargs):
        """Emit a B92 student implementation event"""
        event_data = {
            "message": message,
            "protocol": "B92",
            "timestamp": time.time(),
            **kwargs
        }
        
        event = self.create_b92_event(event_type, node, **event_data)
        self.emit_b92_event(event)
        return event
    
    def get_recent_events(self, count: int = 100) -> List[B92Event]:
        """Get recent B92 events"""
        return self.event_history[-count:] if self.event_history else []
    
    def get_events_by_type(self, event_type: B92EventType) -> List[B92Event]:
        """Get all events of a specific type"""
        return [event for event in self.event_history if event.event_type == event_type]
    
    def clear_history(self):
        """Clear event history"""
        self.event_history.clear()


# Global B92 event manager instance
b92_event_manager = B92WorldEventManager()
