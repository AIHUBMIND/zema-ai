"""
Helper Utilities
Common utility functions
"""

import logging
from typing import Any, Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)


def ensure_directory(path: Path) -> Path:
    """
    Ensure directory exists
    
    Args:
        path: Directory path
        
    Returns:
        Created path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(filename: str) -> str:
    """
    Convert filename to safe filename
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    import re
    # Remove invalid characters
    safe = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe[:255]  # Limit length

