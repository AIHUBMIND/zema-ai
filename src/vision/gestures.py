"""
Gesture Detection
Detects gestures from Insta360 Link 2 camera
"""

import logging
from typing import Optional
import numpy as np
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class GestureDetector:
    """
    Detect gestures from camera
    
    Primary method: LED blink detection
    Fallback: MediaPipe hand detection
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize gesture detector
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        logger.info("GestureDetector initialized")
    
    async def detect_gesture(self, frame: np.ndarray) -> Optional[str]:
        """
        Detect gesture in frame
        
        Args:
            frame: Camera frame
            
        Returns:
            Gesture type (wave, thumbs_up, peace_sign) or None
        """
        # TODO: Implement gesture detection
        logger.debug("Detecting gestures...")
        return None

