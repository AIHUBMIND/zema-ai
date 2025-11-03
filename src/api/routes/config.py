"""
Configuration API Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.config.settings import settings
from src.config.config_manager import ConfigManager
from src.core.event_bus import EventBus

router = APIRouter()

class ConfigUpdate(BaseModel):
    """Configuration update model"""
    key: str
    value: Any

class ConfigBulkUpdate(BaseModel):
    """Bulk configuration update model"""
    updates: Dict[str, Any]

def get_config_manager() -> ConfigManager:
    """Dependency to get ConfigManager instance"""
    event_bus = EventBus()
    return ConfigManager(settings, event_bus)

# User-facing settings (exposed in dashboard)
USER_FACING_SETTINGS = {
    # Privacy & Security
    'privacy_mode',
    'data_retention_days',
    # Voice & Audio
    'wakeword_keywords',
    'wakeword_sensitivity',
    'stt_language',
    'tts_voice',
    'tts_speed',
    'audio_input_device_index',  # Phase 0.5: Hardware verification
    'audio_output_device_index',  # Phase 0.5: Hardware verification
    # Camera & Vision
    'camera_tracking',
    'camera_gestures',
    'camera_device_path',  # Phase 0.5: Hardware verification
    # AI & Intelligence
    'llm_model',
    'llm_temperature',
    'llm_max_tokens',
    'llm_system_prompt',
    'ollama_url',  # Phase 0.5: Hardware verification
    # Features
    'feature_voice',
    'feature_vision',
    'feature_tasks',
    'feature_ethiopian',
    # Hardware Verification (Phase 0.5)
    'hardware_verification_enabled',
    'hardware_verification_camera_test',
    'hardware_verification_audio_test',
    'hardware_verification_ollama_test',
    # API Keys
    'gemini_api_key',
    'elevenlabs_api_key',
    # System
    'log_level',
}

@router.get("/api/config")
async def get_config(user_facing_only: bool = False) -> Dict[str, Any]:
    """
    Get current configuration
    
    Args:
        user_facing_only: If True, return only user-facing settings
    """
    all_settings = settings.model_dump()
    if user_facing_only:
        return {k: v for k, v in all_settings.items() if k in USER_FACING_SETTINGS}
    return all_settings

@router.get("/api/config/user-facing")
async def get_user_facing_config() -> Dict[str, Any]:
    """Get only user-facing configuration settings"""
    all_settings = settings.model_dump()
    return {k: v for k, v in all_settings.items() if k in USER_FACING_SETTINGS}

@router.post("/api/config")
async def update_config(
    update: ConfigUpdate, 
    config_manager: ConfigManager = Depends(get_config_manager)
) -> Dict[str, Any]:
    """
    Update a single configuration setting
    
    Only allows updating user-facing settings via API
    """
    # Validate that it's a user-facing setting
    if update.key not in USER_FACING_SETTINGS:
        raise HTTPException(
            status_code=403, 
            detail=f"Setting '{update.key}' is not user-configurable. Use .env file for technical settings."
        )
    
    success = config_manager.update_setting(update.key, update.value)
    if success:
        return {"status": "updated", "key": update.key, "value": update.value}
    raise HTTPException(status_code=400, detail="Invalid setting or value")

@router.post("/api/config/bulk")
async def update_config_bulk(
    updates: ConfigBulkUpdate,
    config_manager: ConfigManager = Depends(get_config_manager)
) -> Dict[str, Any]:
    """
    Update multiple configuration settings at once
    
    Only allows updating user-facing settings via API
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Bulk config update requested: {len(updates.updates)} settings")
    logger.debug(f"Settings to update: {updates.updates}")
    
    results = {}
    errors = []
    
    for key, value in updates.updates.items():
        logger.debug(f"Processing update: {key} = {value} (type: {type(value).__name__})")
        
        # Validate that it's a user-facing setting
        if key not in USER_FACING_SETTINGS:
            error_msg = f"'{key}' is not a user-facing setting"
            logger.warning(error_msg)
            errors.append(error_msg)
            results[key] = {"status": "error", "message": "Not a user-facing setting"}
            continue
        
        # Update setting
        try:
            success = config_manager.update_setting(key, value)
            if success:
                logger.info(f"Successfully updated setting: {key} = {value}")
                results[key] = {"status": "updated", "value": value}
            else:
                error_msg = f"Failed to update '{key}'"
                logger.error(error_msg)
                errors.append(error_msg)
                results[key] = {"status": "error", "message": "Update failed"}
        except Exception as e:
            error_msg = f"Exception updating '{key}': {str(e)}"
            logger.error(error_msg, exc_info=True)
            errors.append(error_msg)
            results[key] = {"status": "error", "message": str(e)}
    
    if errors:
        logger.warning(f"Bulk update completed with {len(errors)} errors: {errors}")
        return {
            "status": "partial",
            "results": results,
            "errors": errors,
            "message": f"Updated {len(results) - len(errors)}/{len(updates.updates)} settings. {len(errors)} errors."
        }
    
    logger.info(f"Bulk update successful: {len(results)} settings updated")
    return {
        "status": "success",
        "results": results,
        "message": f"Successfully updated {len(results)} settings"
    }

