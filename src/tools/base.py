"""
Tool Base Classes
Base classes for all personal assistant tools
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class Tool(ABC):
    """
    Base class for all tools
    
    All tools must implement:
    - execute() - Execute the tool action
    - get_description() - Get tool description for LLM
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize tool
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.name = self.__class__.__name__
        logger.info(f"Tool initialized: {self.name}")
    
    @abstractmethod
    async def execute(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool action
        
        Args:
            action: Action name
            parameters: Action parameters
            
        Returns:
            Result dictionary
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get tool description for LLM
        
        Returns:
            Tool description string
        """
        pass
    
    def get_available_actions(self) -> List[str]:
        """
        Get list of available actions
        
        Returns:
            List of action names
        """
        return []

