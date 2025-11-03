# main.py Documentation

## File Location
`src/main.py`

## Purpose
Main entry point for Zema AI Assistant. This is the file that gets executed when running the application. It initializes the logging system and starts the orchestrator.

## Why It Was Created
Every Python application needs a main entry point. This file:
- Sets up logging before anything else runs
- Initializes the orchestrator
- Handles graceful shutdown (Ctrl+C)
- Catches and logs fatal errors

## How It Works

### Function: `main()`
**Purpose**: Main application entry point
**How it works**:
1. **Sets up logging**: Calls `setup_logging()` with log level from settings
2. **Logs startup info**: Prints version, environment, startup banner
3. **Initializes orchestrator**: (TODO) Creates orchestrator instance
4. **Starts main loop**: (TODO) Calls `orchestrator.start()`

**Current status**: Partially implemented - orchestrator initialization is commented out (TODO)

### Entry Point
```python
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
```

**How it works**:
1. Uses `asyncio.run()` to run async `main()` function
2. Catches `KeyboardInterrupt` (Ctrl+C) for graceful shutdown
3. Catches all other exceptions and logs them with traceback

## Dependencies
- `asyncio`: Async execution
- `logging`: Logging support
- `src.config.settings`: Application settings
- `src.utils.logger`: Logging setup and logger getter

## Usage
```bash
# Run from project root
python -m src.main

# Or if installed as package
zema
```

## Current Implementation Status
- ✅ Logging setup
- ✅ Startup logging
- ⏳ Orchestrator initialization (TODO)
- ⏳ Main loop (TODO)

## Future Implementation
When complete, this will:
1. Initialize all components (voice, vision, AI, tools)
2. Start the main conversation loop
3. Handle wake word detection
4. Process voice input
5. Generate responses
6. Handle graceful shutdown

## Error Handling
- **KeyboardInterrupt**: Graceful shutdown message
- **Other exceptions**: Logs error with full traceback (`exc_info=True`)
- **Fatal errors**: Application exits with error code

## Integration
This file is:
- Referenced in `setup.py` as entry point
- Called by `python -m src.main`
- Entry point for the entire application

