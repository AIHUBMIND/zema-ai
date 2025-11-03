"""
Wake Word Detection
Detects activation phrases like "Hey Zema"
"""

import logging
from typing import Optional, List
from src.config.settings import Settings
from src.voice.audio_io import AudioIO

logger = logging.getLogger(__name__)


class WakeWordDetector:
    """
    Detect wake words using Porcupine or openwakeword
    
    Supports multiple wake words with configurable sensitivity
    """
    
    def __init__(self, settings: Settings, audio_io: AudioIO):
        """
        Initialize wake word detector
        
        Args:
            settings: Application settings
            audio_io: AudioIO instance
        """
        self.settings = settings
        self.audio_io = audio_io
        self.keywords = settings.wakeword_keywords
        self.sensitivity = settings.wakeword_sensitivity
        
        logger.info(f"WakeWordDetector initialized with keywords: {self.keywords}")
    
    async def wait_for_wake_word(self) -> Optional[str]:
        """
        Wait for wake word detection
        
        Returns:
            Wake word detected (e.g., "hey zema") or None
        """
        # TODO: Implement wake word detection
        logger.info("Waiting for wake word...")
        return None
    
    def cleanup(self) -> None:
        """Clean up resources"""
        logger.info("WakeWordDetector cleanup")

