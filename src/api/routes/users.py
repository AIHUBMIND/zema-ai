"""
User Management API Routes
"""

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@router.get("/api/users")
async def list_users() -> Dict[str, Any]:
    """List all users"""
    return {"users": []}

@router.post("/api/users")
async def create_user() -> Dict[str, str]:
    """Create new user"""
    return {"status": "created"}

