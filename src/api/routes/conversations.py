"""
Conversation History API Routes
"""

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@router.get("/api/conversations")
async def get_conversations() -> Dict[str, Any]:
    """Get conversation history"""
    return {"conversations": []}

