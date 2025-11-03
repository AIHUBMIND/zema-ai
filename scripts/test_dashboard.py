"""
Dashboard Test Server
Standalone script to test the dashboard UI
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import asyncio
import logging
from src.config.settings import settings
from src.utils.logger import setup_logging
from src.api.server import start_dashboard

def main() -> None:
    """Run dashboard server for testing"""
    # Setup logging
    setup_logging(settings.log_level)
    
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting Zema Dashboard Test Server")
    logger.info(f"Dashboard URL: http://{settings.dashboard_host}:{settings.dashboard_port}")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    try:
        # Run dashboard server
        asyncio.run(start_dashboard(settings))
    except KeyboardInterrupt:
        logger.info("Dashboard server stopped")

if __name__ == "__main__":
    main()

