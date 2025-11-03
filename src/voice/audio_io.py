"""
Audio I/O Module
Handles microphone input and speaker output for Zema
"""

import logging
from typing import Optional, Callable, Dict, Any
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class AudioIO:
    """
    Audio input/output manager
    
    CRITICAL: Handles all audio I/O operations including:
    - Device detection (Insta360 Link 2 microphone preferred)
    - Audio recording (async)
    - Audio playback (async)
    - Stream management
    - Error recovery
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize AudioIO
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.pyaudio = None
        self.input_stream = None
        self.output_stream = None
        self.input_device_index = None
        self.output_device_index = None
        self.device_info = {}
        
        logger.info("AudioIO initialized (PyAudio initialization pending)")
    
    def cleanup(self) -> None:
        """Clean up audio resources"""
        logger.info("AudioIO cleanup")

