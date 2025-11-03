# Source Code Folder (src/)

## Purpose
The `src/` folder contains all the main application source code. This is the core of Zema AI, organized into logical modules for different functionalities.

## Folder Structure

### `core/`
Core system components: orchestrator, state management, event bus

### `config/`
Configuration management: settings, config manager

### `voice/`
Voice processing: audio I/O, wake word detection, speech-to-text, text-to-speech

### `vision/`
Vision processing: camera interface, object detection, scene analysis, gestures

### `ai/`
AI/LLM components: LLM client, context management, response parsing, system prompts

### `tools/`
Personal assistant tools: tasks, notes, knowledge base, web search, system config

### `api/`
FastAPI server and routes: REST API, WebSocket, dashboard

### `utils/`
Utility functions: logging, helpers, constants, performance monitoring

## Architecture Principles
- **Modular**: Each folder has a single responsibility
- **Async-first**: Uses async/await for I/O operations
- **Type-hinted**: All functions have type hints
- **Documented**: All public functions have docstrings

## Import Pattern
```python
# From src folder
from core.orchestrator import Orchestrator
from config.settings import settings
from voice.audio_io import AudioIO
```

## Main Entry Point
`src/main.py` - Application entry point, initializes orchestrator and starts system

