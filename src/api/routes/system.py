"""
System API Routes
"""

from fastapi import APIRouter
from typing import Dict, Any
import psutil
import time

router = APIRouter()

# Track start time for uptime calculation
start_time = time.time()

def get_system_status() -> Dict[str, Any]:
    """Get system status - shared function for API and WebSocket"""
    # Calculate uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    
    return {
        "listening": True,  # TODO: Get actual listening status from core
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "uptime": uptime_seconds
    }

@router.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Get system status"""
    return get_system_status()

