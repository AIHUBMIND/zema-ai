"""
Conversation History API Routes
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/api/conversations")
async def get_conversations():
    """Get conversation history"""
    return {"conversations": []}

