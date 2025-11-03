"""
Main entry point for Zema AI Assistant
"""

import asyncio
import logging
from src.config.settings import settings
from src.utils.logger import setup_logging, get_logger

logger = get_logger(__name__)

# Version
__version__ = "0.1.0"


async def main():
    """Main application entry point"""
    # Setup logging
    setup_logging(settings.log_level)
    
    logger.info("=" * 60)
    logger.info("Zema AI Assistant Starting...")
    logger.info(f"Version: {__version__}")
    logger.info(f"Environment: {settings.environment}")
    logger.info("=" * 60)
    
    # TODO: Initialize orchestrator and start main loop
    # from src.core.orchestrator import Orchestrator
    # orchestrator = Orchestrator(settings)
    # await orchestrator.start()
    
    logger.info("Zema AI Assistant initialized")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)


