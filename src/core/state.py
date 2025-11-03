"""
Application State Management
Manages global application state and conversation history
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Single conversation turn"""
    user_input: str
    assistant_response: str
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)


class ApplicationState:
    """
    Global application state
    
    Manages:
    - Conversation history
    - System state
    - User preferences
    """
    
    def __init__(self):
        self.conversation_history: List[ConversationTurn] = []
        self.is_listening: bool = False
        self.is_processing: bool = False
        self.current_user: Optional[str] = None
        
        logger.info("ApplicationState initialized")
    
    def add_conversation_turn(self, user_input: str, assistant_response: str, context: Dict[str, Any] = None) -> None:
        """
        Add a conversation turn to history
        
        Args:
            user_input: User's input text
            assistant_response: Assistant's response
            context: Additional context (vision, tools, etc.)
        """
        turn = ConversationTurn(
            user_input=user_input,
            assistant_response=assistant_response,
            context=context or {}
        )
        self.conversation_history.append(turn)
        
        # Keep only last 100 turns
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        logger.debug(f"Added conversation turn: {user_input[:50]}...")
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def get_recent_history(self, limit: int = 10) -> List[ConversationTurn]:
        """
        Get recent conversation history
        
        Args:
            limit: Number of recent turns to return
            
        Returns:
            List of recent conversation turns
        """
        return self.conversation_history[-limit:]

