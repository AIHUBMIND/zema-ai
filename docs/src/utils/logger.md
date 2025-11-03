# logger.py Documentation

## File Location
`src/utils/logger.py`

## Purpose
Structured logging system providing both console output (with rich formatting) and JSON file logging. Includes performance monitoring decorator.

## Why It Was Created
Proper logging is essential for:
- Debugging issues
- Monitoring system behavior
- Performance tracking
- Audit trails
- Production diagnostics

## How It Works

### Function: `setup_logging(log_level)`
**Purpose**: Initialize logging system
**How it works**:
1. **Creates logs directory**: `data/logs/` if it doesn't exist
2. **Clears existing handlers**: Prevents duplicate logs
3. **Sets up console handler**:
   - Uses `RichHandler` if `rich` library available (pretty formatting)
   - Falls back to `StreamHandler` if not available
   - Shows time, level, module, line number
4. **Sets up file handler**:
   - Uses `RotatingFileHandler` (10MB max, 5 backups)
   - JSON format for structured logging
   - UTF-8 encoding
5. **Sets log levels**:
   - Console: INFO level (less verbose)
   - File: DEBUG level (more verbose)

**Must be called first**: Before any other logging calls

### Class: `JSONFormatter`
**Purpose**: Formats log records as JSON
**How it works**:
1. Extracts log record fields
2. Formats as JSON dictionary:
   - `timestamp`: Formatted timestamp
   - `level`: Log level (DEBUG, INFO, etc.)
   - `logger`: Logger name
   - `module`: Module name
   - `function`: Function name
   - `line`: Line number
   - `message`: Log message
   - `exception`: Exception info (if present)
3. Returns JSON string

**Benefits**: Structured logs can be parsed by log analysis tools

### Function: `get_logger(name)`
**Purpose**: Get logger instance for a module
**Usage**:
```python
logger = get_logger(__name__)
logger.info("System started")
```

### Decorator: `log_performance`
**Purpose**: Log function execution time
**How it works**:
1. Wraps function execution
2. Records start time
3. Executes function
4. Records end time
5. Calculates duration
6. Logs performance metric

**Supports**: Both sync and async functions

**Usage**:
```python
@log_performance
def my_function():
    # Function code
    pass

@log_performance
async def my_async_function():
    # Async function code
    pass
```

## Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages (non-critical issues)
- **ERROR**: Error messages (handled exceptions)
- **CRITICAL**: Critical errors (may cause shutdown)

## Log Output

### Console Output (Rich)
```
2025-11-02 14:30:45 [INFO] src.main:main:22 - Zema AI Assistant Starting...
```

### File Output (JSON)
```json
{
  "timestamp": "2025-11-02 14:30:45",
  "level": "INFO",
  "logger": "src.main",
  "module": "main",
  "function": "main",
  "line": 22,
  "message": "Zema AI Assistant Starting..."
}
```

## Dependencies
- `logging`: Python logging module
- `rich`: Pretty console output (optional)
- `RotatingFileHandler`: File rotation
- `asyncio`: Async function support
- `json`: JSON serialization
- `time`: Time measurement
- `functools`: Decorator support

## Usage Examples

### Basic Logging
```python
from src.utils.logger import setup_logging, get_logger

# Setup (call once at startup)
setup_logging("INFO")

# Get logger
logger = get_logger(__name__)

# Log messages
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Performance Logging
```python
from src.utils.logger import log_performance

@log_performance
def process_data(data):
    # Processing code
    return result

# Output: Performance: process_data took 150.5ms
```

### Error Logging with Exception
```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True)
    # Logs full traceback
```

## Log File Rotation
- **Max size**: 10MB per file
- **Backups**: 5 backup files
- **Naming**: `zema.log`, `zema.log.1`, `zema.log.2`, etc.
- **Automatic**: Rotates when size limit reached

## Integration
Used throughout the application:
- `src/main.py`: Application startup logging
- `src/core/orchestrator.py`: Component lifecycle logging
- All modules: Standard logging interface

## Benefits
1. **Structured logging**: JSON format for analysis
2. **Pretty console**: Rich formatting for readability
3. **Performance tracking**: Built-in performance decorator
4. **File rotation**: Prevents log files from growing too large
5. **Level filtering**: Different levels for console vs file

## Configuration
Log level can be set via:
- `settings.log_level` (from `src/config/settings.py`)
- Environment variable: `LOG_LEVEL=DEBUG`
- `.env` file: `LOG_LEVEL=DEBUG`

