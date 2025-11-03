# Utils Module Documentation

## Purpose
The `src/utils/` folder contains utility functions, helpers, constants, logging, and performance monitoring used throughout the application.

## Files in This Folder

### `logger.py`
Structured logging system using `rich` for console output and `RotatingFileHandler` for JSON log files. Provides `log_performance` decorator for timing functions.

### `helpers.py`
Common utility functions: directory creation, filename sanitization, and other helper utilities.

### `constants.py`
Application-wide constants: app name/version, audio constants, camera constants, LLM constants, file paths.

### `performance.py`
Performance monitoring system. Tracks system and component performance metrics, records operation durations, provides statistics.

## Usage Examples
```python
# Logging
from src.utils.logger import setup_logging, logger
setup_logging()
logger.info("System started")

# Performance monitoring
from src.utils.performance import PerformanceMonitor
monitor = PerformanceMonitor()
monitor.record("voice", "stt", 150.5)  # ms

# Constants
from src.utils.constants import DEFAULT_SAMPLE_RATE, APP_NAME

# Helpers
from src.utils.helpers import ensure_directory, safe_filename
```

## Key Features
- Structured logging (JSON + console)
- Performance tracking
- Centralized constants
- Helper utilities
- Cross-module support

