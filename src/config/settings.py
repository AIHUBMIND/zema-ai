"""
Configuration Settings for Zema AI
Uses Pydantic Settings for type-safe configuration management
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional, List, Any
from enum import Enum


class PrivacyMode(str, Enum):
    """Privacy mode options"""
    LOCAL = "local"
    HYBRID = "hybrid"
    CLOUD = "cloud"


class Settings(BaseSettings):
    """Application settings with validation"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # General Settings
    environment: str = Field(default="production", description="Environment: development, production")
    log_level: str = Field(default="INFO", description="Log level: DEBUG, INFO, WARNING, ERROR")
    hostname: str = Field(default="zema", description="System hostname")
    
    # Dashboard Settings
    enable_dashboard: bool = Field(default=True, description="Enable web dashboard")
    dashboard_port: int = Field(default=8000, ge=1024, le=65535, description="Dashboard port")
    dashboard_host: str = Field(default="0.0.0.0", description="Dashboard host")
    
    # Wake Word Settings
    wakeword_keywords: List[str] = Field(default=["hey zema", "zema"], description="Wake word keywords")
    wakeword_sensitivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Wake word sensitivity")
    
    # Privacy Settings
    privacy_mode: PrivacyMode = Field(default=PrivacyMode.LOCAL, description="Privacy mode")
    data_retention_days: int = Field(default=30, ge=1, le=365, description="Data retention in days")
    
    # Audio Settings
    audio_sample_rate: int = Field(default=16000, description="Audio sample rate in Hz")
    audio_channels: int = Field(default=1, ge=1, le=2, description="Audio channels")
    audio_device_name: Optional[str] = Field(default=None, description="Audio device name")
    
    # Voice Settings
    stt_model: str = Field(default="base", description="STT model: tiny, base, small")
    stt_language: str = Field(default="en", description="STT language: en, am, auto")
    tts_engine: str = Field(default="piper", description="TTS engine")
    tts_voice: str = Field(default="en_US-lessac-medium", description="TTS voice")
    tts_speed: float = Field(default=1.0, ge=0.5, le=2.0, description="TTS speed multiplier")
    
    # Camera Settings
    camera_device: int = Field(default=0, description="Camera device index")
    camera_width: int = Field(default=1920, description="Camera width")
    camera_height: int = Field(default=1080, description="Camera height")
    camera_fps: int = Field(default=30, ge=1, le=60, description="Camera FPS")
    camera_tracking: bool = Field(default=True, description="Enable camera tracking")
    camera_gestures: bool = Field(default=True, description="Enable gesture recognition")
    
    # LLM Settings
    llm_model: str = Field(default="llama2:13b", description="Ollama model name")
    llm_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="LLM temperature")
    llm_max_tokens: int = Field(default=512, ge=1, le=4096, description="Max tokens per response")
    llm_system_prompt: str = Field(
        default="You are Zema, a helpful privacy-first AI assistant.",
        description="System prompt for LLM"
    )
    
    # Vision Settings
    vision_detection_model: str = Field(default="yolov8n", description="Detection model")
    vision_confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence threshold")
    
    # Feature Flags
    feature_voice: bool = Field(default=True, description="Enable voice features")
    feature_vision: bool = Field(default=True, description="Enable vision features")
    feature_tasks: bool = Field(default=True, description="Enable task management")
    feature_ethiopian: bool = Field(default=False, description="Enable Ethiopian features")
    
    # API Keys (Optional)
    gemini_api_key: Optional[str] = Field(default=None, description="Gemini API key (optional)")
    elevenlabs_api_key: Optional[str] = Field(default=None, description="ElevenLabs API key (optional)")
    
    # Database Settings
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/db/zema.db",
        description="Database URL"
    )
    
    @field_validator('privacy_mode', mode='before')
    @classmethod
    def validate_privacy_mode(cls, v: Any) -> PrivacyMode:
        """Validate privacy mode"""
        if isinstance(v, str):
            v = v.lower()
            if v not in ['local', 'hybrid', 'cloud']:
                raise ValueError("privacy_mode must be 'local', 'hybrid', or 'cloud'")
            return PrivacyMode(v)
        return v
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()
    
    @field_validator('stt_model')
    @classmethod
    def validate_stt_model(cls, v: str) -> str:
        """Validate STT model"""
        valid_models = ['tiny', 'base', 'small', 'medium']
        if v.lower() not in valid_models:
            raise ValueError(f"stt_model must be one of {valid_models}")
        return v.lower()


# Global settings instance
settings = Settings()
