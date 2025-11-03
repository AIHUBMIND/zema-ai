"""
LLM Client
Interface to Ollama for AI responses (100% OFFLINE)
"""

import httpx
import json
import logging
from typing import List, Dict, Optional, AsyncGenerator
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Client for Ollama LLM - OFFLINE ONLY
    
    CRITICAL: All LLM calls must go to localhost:11434.
    No internet required. Fully offline operation.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize LLM client
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        # CRITICAL: Local only - no internet required
        self.base_url = "http://localhost:11434"  # Local Ollama server
        self.model = settings.llm_model  # e.g., "llama2:13b"
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens
        self.system_prompt = settings.llm_system_prompt
        
        self.conversation_history: List[Dict[str, str]] = []
        logger.info(f"LLMClient initialized with model: {self.model}")
    
    async def check_ollama_available(self) -> bool:
        """
        Check if local Ollama server is running
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            return False
    
    async def generate(self, user_input: str, context: Optional[Dict] = None) -> str:
        """
        Generate response from LLM (OFFLINE)
        
        This ALWAYS uses local Ollama. No internet required.
        
        Args:
            user_input: User's input text
            context: Optional context (vision, tools, etc.)
            
        Returns:
            Generated response text
        """
        if not await self.check_ollama_available():
            raise ConnectionError("Ollama server not running locally")
        
        # Build messages with conversation history
        messages = self._build_messages(user_input, context)
        
        # Call LOCAL Ollama API
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({
                "role": "assistant",
                "content": result["message"]["content"]
            })
            
            return result["message"]["content"]
    
    async def generate_stream(self, user_input: str, context: Optional[Dict] = None) -> AsyncGenerator[str, None]:
        """
        Generate streaming response (OFFLINE)
        
        Yields tokens as they're generated from local Ollama.
        
        Args:
            user_input: User's input text
            context: Optional context
            
        Yields:
            Text chunks as they're generated
        """
        if not await self.check_ollama_available():
            raise ConnectionError("Ollama server not running locally")
        
        messages = self._build_messages(user_input, context)
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    }
                }
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
                        except json.JSONDecodeError:
                            continue
    
    def _build_messages(self, user_input: str, context: Optional[Dict]) -> List[Dict]:
        """
        Build message list for Ollama
        
        Args:
            user_input: User's input text
            context: Optional context
            
        Returns:
            List of message dictionaries
        """
        messages = []
        
        # System prompt
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # Add context if provided
        if context:
            if "vision_description" in context:
                messages.append({
                    "role": "system",
                    "content": f"Vision context: {context['vision_description']}"
                })
        
        # Conversation history
        messages.extend(self.conversation_history[-10:])  # Last 10 exchanges
        
        # Current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def update_model(self, model_name: str):
        """
        Update active model (must be installed locally)
        
        Args:
            model_name: New model name
        """
        self.model = model_name
        logger.info(f"Switched to model: {model_name}")

