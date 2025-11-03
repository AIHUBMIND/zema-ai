"""
Voice Activity Detection
Detects when user is speaking vs silence
"""

import logging
from typing import List, Tuple
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class VoiceActivityDetector:
    """
    Detect voice activity in audio stream
    
    Uses WebRTC VAD library to detect speech vs silence
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize VAD
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.vad = None  # Will be initialized when webrtcvad is available
        self.sample_rate = settings.audio_sample_rate
        self.silence_threshold_ms = 900  # ms of silence before considering speech ended
        
        logger.info("VoiceActivityDetector initialized")
    
    def is_speech(self, audio_chunk: bytes) -> bool:
        """
        Check if audio chunk contains speech
        
        Args:
            audio_chunk: Raw audio bytes
            
        Returns:
            True if speech detected
        """
        # TODO: Implement VAD check
        return False
    
    async def detect_speech_segments(self, audio_stream) -> List[Tuple]:
        """
        Detect speech segments from audio stream
        
        Args:
            audio_stream: Async generator yielding audio chunks
            
        Returns:
            List of (audio_data, duration) tuples
        """
        # TODO: Implement speech segment detection
        return []

