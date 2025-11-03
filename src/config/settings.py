"""Application settings using Pydantic."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings."""

    # Application
    app_name: str = Field(default="Zema AI Personal Assistant", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # API
    api_host: str = Field(default="127.0.0.1", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # LLM (Ollama)
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    ollama_model: str = Field(default="llama2:13b", description="Ollama model name")
    
    # Voice
    wake_word_enabled: bool = Field(default=True, description="Enable wake word detection")
    sample_rate: int = Field(default=16000, description="Audio sample rate")
    channels: int = Field(default=1, description="Audio channels")
    chunk_size: int = Field(default=1024, description="Audio chunk size")
    
    # Vision
    camera_enabled: bool = Field(default=False, description="Enable camera")
    camera_index: int = Field(default=0, description="Camera device index")
    
    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/db/zema.db",
        description="Database URL"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="./data/logs/zema.log", description="Log file path")
    
    # Paths
    data_dir: str = Field(default="./data", description="Data directory")
    models_dir: str = Field(default="./data/models", description="Models directory")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()

