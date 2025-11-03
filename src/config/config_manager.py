"""
Configuration Manager
Manages live configuration updates without restart
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.config.settings import Settings
from src.core.event_bus import EventBus

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Configuration manager for live updates
    
    Handles:
    - Configuration updates
    - Validation
    - Event broadcasting
    - Persistent storage
    """
    
    def __init__(self, settings: Settings, event_bus: Optional[EventBus] = None):
        """
        Initialize configuration manager
        
        Args:
            settings: Application settings instance
            event_bus: Optional event bus for broadcasting changes
        """
        self.settings = settings
        self.event_bus = event_bus or EventBus()
        self.config_file = Path("data/config/settings.json")
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        self._load_config()
        logger.info("ConfigManager initialized")
    
    def _load_config(self) -> None:
        """Load configuration from file if it exists"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    # Update settings with saved values
                    for key, value in saved_config.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
                logger.info("Configuration loaded from file")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
    
    def update_setting(self, key: str, value: Any) -> bool:
        """
        Update a single setting
        
        Args:
            key: Setting name
            value: New value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate setting exists
            if not hasattr(self.settings, key):
                logger.error(f"Setting '{key}' not found")
                return False
            
            # Store old value
            old_value = getattr(self.settings, key)
            
            # Update setting
            setattr(self.settings, key, value)
            
            # Save to file
            self._save_config()
            
            # Broadcast change
            self.event_bus.emit('config_changed', {
                'key': key,
                'old_value': old_value,
                'new_value': value
            })
            
            logger.info(f"Setting updated: {key} = {value}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to update setting: {e}")
            return False
    
    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            config_dict = self.settings.model_dump()
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            logger.debug("Configuration saved")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return self.settings.model_dump()

