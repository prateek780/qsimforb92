from fastapi import APIRouter
import importlib, json, os
from protocol_detection_utils import detect_active_protocol

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.get("/student-implementation-status/")
def student_impl_status():
    # Prefer plugin discovery (server mode)
    try:
        mod = importlib.import_module("student_plugin")
        if hasattr(mod, "StudentImplementation"):
            return {"student_implementation_ready": True, "source": "plugin"}
    except Exception:
        pass
    # Optional JSON fallback
    try:
        if os.path.exists("student_implementation_status.json"):
            with open("student_implementation_status.json", "r", encoding="utf-8") as f:
                payload = json.load(f)
            payload.setdefault("student_implementation_ready", True)
            payload.setdefault("source", "json")
            return payload
    except Exception:
        pass
    return {"student_implementation_ready": False, "source": "none"}

@router.get("/student-implementation-status-b92/")
def student_impl_status_b92():
    """B92-specific student implementation status endpoint"""
    # Check for B92 implementation status
    try:
        if os.path.exists("student_b92_implementation_status.json"):
            with open("student_b92_implementation_status.json", "r", encoding="utf-8") as f:
                payload = json.load(f)
            payload.setdefault("student_implementation_ready", True)
            payload.setdefault("source", "b92_json")
            payload.setdefault("has_valid_implementation", True)
            return payload
    except Exception as e:
        print(f"Error reading B92 status: {e}")
        pass
    
    # Fallback to BB84 status if B92 not found
    try:
        if os.path.exists("student_implementation_status.json"):
            with open("student_implementation_status.json", "r", encoding="utf-8") as f:
                payload = json.load(f)
            # Override protocol to B92 for compatibility
            payload["protocol"] = "b92"
            payload.setdefault("student_implementation_ready", True)
            payload.setdefault("source", "bb84_fallback")
            payload.setdefault("has_valid_implementation", True)
            return payload
    except Exception:
        pass
    
    return {
        "student_implementation_ready": False, 
        "source": "none",
        "has_valid_implementation": False,
        "protocol": "b92"
    }

@router.get("/student-implementation-status-auto/")
def student_impl_status_auto():
    """
    Automatically detect protocol and return appropriate status.
    This endpoint replaces the need for separate BB84/B92 endpoints.
    """
    try:
        protocol = detect_active_protocol()
        
        if protocol == "B92":
            return student_impl_status_b92()
        else:
            return student_impl_status()
    except Exception as e:
        return {
            "student_implementation_ready": False,
            "source": "error",
            "has_valid_implementation": False,
            "protocol": "unknown",
            "error": str(e)
        }