"""
Speech-to-Text Module
Converts audio to text using Whisper
"""

import logging
from typing import Optional, Tuple
import numpy as np
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Convert speech audio to text using Whisper
    
    Supports multiple languages (English, Amharic)
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize STT
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.model = None  # Will be initialized when faster-whisper is available
        self.model_size = settings.stt_model  # tiny, base, small
        self.language = settings.stt_language  # en, am, or None (auto)
        
        logger.info(f"SpeechToText initialized with model: {self.model_size}, language: {self.language}")
    
    async def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Tuple[str, float]:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio samples (numpy array)
            sample_rate: Sample rate in Hz
            
        Returns:
            Tuple of (transcription, confidence)
        """
        # TODO: Implement transcription
        logger.info("Transcribing audio...")
        return "", 0.0
    
    def update_language(self, language: str):
        """
        Update transcription language
        
        Args:
            language: Language code (en, am, auto)
        """
        self.language = language
        logger.info(f"STT language set to: {language}")

