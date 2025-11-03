"""
Configuration API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.config.settings import Settings
from src.config.config_manager import ConfigManager

router = APIRouter()

class ConfigUpdate(BaseModel):
    """Configuration update model"""
    key: str
    value: Any

@router.get("/api/config")
async def get_config(settings: Settings):
    """Get current configuration"""
    return settings.model_dump()

@router.post("/api/config")
async def update_config(update: ConfigUpdate, config_manager: ConfigManager):
    """Update configuration"""
    success = config_manager.update_setting(update.key, update.value)
    if success:
        return {"status": "updated", "key": update.key, "value": update.value}
    raise HTTPException(status_code=400, detail="Invalid setting")

