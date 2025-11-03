"""
System API Routes
"""

from fastapi import APIRouter
from typing import Dict, Any
import psutil
import time

router = APIRouter()

@router.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Get system status"""
    return {
        "status": "listening",
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "uptime": time.time()  # Simplified
    }

