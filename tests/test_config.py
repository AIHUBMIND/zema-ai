"""Tests for configuration module."""
import pytest
from src.config.settings import Settings


def test_settings_creation():
    """Test that Settings can be instantiated."""
    settings = Settings()
    assert settings.app_name == "Zema AI Personal Assistant"
    assert settings.app_version == "0.1.0"
    assert settings.api_port == 8000


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()
    assert isinstance(settings.debug, bool)
    assert isinstance(settings.api_port, int)
    assert isinstance(settings.sample_rate, int)
    assert settings.sample_rate == 16000

