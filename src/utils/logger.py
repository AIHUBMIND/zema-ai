"""
Logging System for Zema AI
Provides structured logging with console (rich) and file (JSON) handlers
"""

import logging
import asyncio
import time
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path
from functools import wraps
from typing import Callable, Any

try:
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: rich library not available. Using basic console handler.")


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging with console (rich) and file (JSON) handlers
    
    CRITICAL: This function MUST be called before any other logging calls.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Steps:
    1. Create logs directory if it doesn't exist
    2. Clear existing handlers
    3. Configure console handler (rich if available)
    4. Configure file handler (JSON format)
    5. Set log levels
    6. Add handlers to root logger
    """
    # Step 1: Create logs directory
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 2: Get root logger and clear existing handlers
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.handlers.clear()
    
    # Step 3: Setup console handler
    if RICH_AVAILABLE:
        console_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=True,
            show_level=True
        )
    else:
        # Fallback to StreamHandler if rich not available
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_format)
    
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    # Step 4: Setup file handler with JSON formatting
    log_file = log_dir / "zema.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    class JSONFormatter(logging.Formatter):
        """JSON formatter for structured logging"""
        
        def format(self, record: logging.LogRecord) -> str:
            """Format log record as JSON"""
            log_data = {
                "timestamp": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "logger": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "message": record.getMessage()
            }
            
            # Add exception info if present
            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)
            
            # Add extra fields if present
            if hasattr(record, 'extra'):
                log_data.update(record.extra)
            
            return json.dumps(log_data, ensure_ascii=False)
    
    file_formatter = JSONFormatter(
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Step 5: Log initialization
    logger.info(f"Logging initialized with level: {log_level}")


def log_performance(func: Callable) -> Callable:
    """
    Decorator to log function execution time
    
    Usage:
        @log_performance
        async def my_function():
            pass
    
    Automatically detects if function is async or sync.
    """
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            start = time.time()
            func_name = f"{func.__module__}.{func.__name__}"
            
            try:
                logger.debug(f"Starting {func_name}")
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start) * 1000
                logger.debug(f"{func_name} completed in {duration_ms:.2f}ms")
                return result
            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                logger.error(
                    f"{func_name} failed after {duration_ms:.2f}ms: {e}",
                    exc_info=True
                )
                raise
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            start = time.time()
            func_name = f"{func.__module__}.{func.__name__}"
            
            try:
                logger.debug(f"Starting {func_name}")
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start) * 1000
                logger.debug(f"{func_name} completed in {duration_ms:.2f}ms")
                return result
            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                logger.error(
                    f"{func_name} failed after {duration_ms:.2f}ms: {e}",
                    exc_info=True
                )
                raise
        return sync_wrapper


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

