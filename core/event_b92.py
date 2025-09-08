"""
B92 Event System
================

Handles B92-specific events for the quantum simulation system.
Separate from the main event system to avoid conflicts with BB84.
"""

import time
from typing import TYPE_CHECKING
from enum import Enum

try:
    from data.models.simulation.log_model import LogLevel
except Exception:
    # Fallback when Redis models are unavailable
    class LogLevel(str, Enum):
        DEBUG = "debug"
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        CRITICAL = "critical"
        PROTOCOL = "protocol"
        STORY = "story"
        NETWORK = "network"

from utils.encoding import transform_val

if TYPE_CHECKING:
    from core.s_object import Sobject


class B92EventType(str, Enum):
    """B92-specific event types"""
    B92_QUBIT_PREPARATION = "b92_qubit_preparation"
    B92_QUBIT_TRANSMISSION = "b92_qubit_transmission"
    B92_QUBIT_MEASUREMENT = "b92_qubit_measurement"
    B92_SIFTING_START = "b92_sifting_start"
    B92_SIFTING_COMPLETE = "b92_sifting_complete"
    B92_ERROR_ESTIMATION = "b92_error_estimation"
    B92_PROTOCOL_START = "b92_protocol_start"
    B92_PROTOCOL_COMPLETE = "b92_protocol_complete"
    B92_STUDENT_SEND_START = "student_b92_send_start"
    B92_STUDENT_SEND_COMPLETE = "student_b92_send_complete"
    B92_STUDENT_MEASURE_START = "student_b92_measure_start"
    B92_STUDENT_MEASURE_COMPLETE = "student_b92_measure_complete"
    B92_STUDENT_RECONCILE_START = "student_b92_reconcile_start"
    B92_STUDENT_RECONCILE_COMPLETE = "student_b92_reconcile_complete"
    B92_STUDENT_ERROR_START = "student_b92_error_start"
    B92_STUDENT_ERROR_COMPLETE = "student_b92_error_complete"
    B92_STUDENT_READY = "student_b92_ready"
    B92_STUDENT_TRIGGER = "student_b92_trigger"
    B92_STUDENT_COMPLETE = "student_b92_complete"


class B92Event:
    """B92-specific event class"""
    
    def __init__(self, event_type: B92EventType, node: 'Sobject', **kwargs):
        self.event_type = event_type
        self.node = node
        self.timestamp = time.time()
        self.data = kwargs
        self.log_level = kwargs.get("log_level", LogLevel.INFO)
        self.protocol = "B92"  # Always mark as B92 protocol

    def to_dict(self):
        return {
            "event_type": self.event_type.value,
            "node": self.node.name,
            "timestamp": self.timestamp,
            "data": {k: transform_val(v) for k, v in self.data.items()},
            "log_level": self.log_level.value if hasattr(self.log_level, 'value') else str(self.log_level),
            "protocol": self.protocol,
        }

    def to_websocket_message(self):
        """Convert to WebSocket message format"""
        return {
            "type": "b92_event",
            "event_type": self.event_type.value,
            "node": self.node.name,
            "timestamp": self.timestamp,
            "data": {k: transform_val(v) for k, v in self.data.items()},
            "log_level": self.log_level.value if hasattr(self.log_level, 'value') else str(self.log_level),
            "protocol": self.protocol,
        }
