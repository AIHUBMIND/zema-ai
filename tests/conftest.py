"""
Pytest Configuration
Shared fixtures and configuration for tests
"""

import pytest
import asyncio
from src.config.settings import Settings


@pytest.fixture
def settings():
    """Create settings instance for testing"""
    return Settings()


@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

