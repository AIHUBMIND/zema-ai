"""
Context Manager
Manages conversation context and multi-turn conversations
"""

import logging
from typing import List, Dict, Any, Optional
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class ContextManager:
    """
    Manages conversation context
    
    Handles:
    - Multi-turn conversations
    - Context building
    - Memory management
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize context manager
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.max_history_length = 20  # Maximum conversation turns to keep
        logger.info("ContextManager initialized")
    
    def build_context(self, conversation_history: List[Dict], current_input: str, 
                     vision_context: Optional[str] = None,
                     tool_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Build context dictionary for LLM
        
        Args:
            conversation_history: Previous conversation turns
            current_input: Current user input
            vision_context: Optional vision description
            tool_context: Optional tool execution results
            
        Returns:
            Context dictionary
        """
        context = {
            "conversation_history": conversation_history[-self.max_history_length:],
            "current_input": current_input,
        }
        
        if vision_context:
            context["vision_description"] = vision_context
        
        if tool_context:
            context["tool_results"] = tool_context
        
        return context
    
    def extract_key_info(self, conversation_turns: List[Dict]) -> Dict[str, Any]:
        """
        Extract key information from conversation
        
        Args:
            conversation_turns: List of conversation turns
            
        Returns:
            Dictionary with extracted key information
        """
        # TODO: Implement information extraction
        return {}

