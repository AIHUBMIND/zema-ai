"""
User Management API Routes
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/api/users")
async def list_users():
    """List all users"""
    return {"users": []}

@router.post("/api/users")
async def create_user():
    """Create new user"""
    return {"status": "created"}

