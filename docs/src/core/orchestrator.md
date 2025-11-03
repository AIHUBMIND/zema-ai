# orchestrator.py Documentation

## File Location
`src/core/orchestrator.py`

## Purpose
Core orchestrator that coordinates all Zema AI components. This is the central coordinator that manages the lifecycle of all system components and orchestrates the main conversation loop.

## Why It Was Created
The orchestrator pattern is used to:
- Decouple components (they don't directly depend on each other)
- Centralize coordination logic
- Manage component lifecycle (startup/shutdown)
- Handle the main conversation loop
- Coordinate between voice, vision, AI, and tools

## How It Works

### Class: `Orchestrator`

#### `__init__(settings)`
**Purpose**: Initialize orchestrator
**How it works**:
1. Stores settings reference
2. Sets `running` flag to `False`
3. Logs initialization

**Parameters**:
- `settings`: `Settings` instance with all configuration

#### `start()`
**Purpose**: Start the main conversation loop
**How it works**:
1. Sets `running` flag to `True`
2. (TODO) Initialize all components:
   - AudioIO for voice input/output
   - WakeWordDetector for wake word detection
   - STT for speech-to-text
   - TTS for text-to-speech
   - Camera for vision (if enabled)
   - LLMClient for AI responses
   - ToolManager for assistant tools
3. (TODO) Enter main loop:
   - Listen for wake word
   - When wake word detected, start listening
   - Process voice input
   - Generate response
   - Speak response

**Current status**: Partially implemented - main loop is TODO

#### `shutdown()`
**Purpose**: Graceful shutdown
**How it works**:
1. Sets `running` flag to `False`
2. (TODO) Stop all components:
   - Close audio streams
   - Release camera
   - Close database connections
   - Clean up resources

**Current status**: Partially implemented - cleanup is TODO

## Main Conversation Loop (Planned)
```
1. Listen for wake word ("Hey Zema")
2. When detected:
   a. Start recording audio
   b. Detect voice activity (VAD)
   c. Stop recording when silence detected
   d. Convert speech to text (STT)
   e. Process with LLM (with context)
   f. Parse response (tool calls?)
   g. Execute tools if needed
   h. Generate final response
   i. Convert text to speech (TTS)
   j. Play audio response
3. Return to step 1
```

## Dependencies
- `logging`: Logging support
- `src.config.settings`: Application settings

## Integration
The orchestrator:
- Is initialized by `src/main.py`
- Coordinates all other modules
- Manages the main application loop
- Handles component lifecycle

## Future Components to Initialize
- `AudioIO`: Audio input/output
- `WakeWordDetector`: Wake word detection
- `SpeechToText`: Speech-to-text conversion
- `TextToSpeech`: Text-to-speech conversion
- `Camera`: Camera interface (if enabled)
- `LLMClient`: LLM communication
- `ContextManager`: Conversation context
- `ToolManager`: Tool execution
- `EventBus`: Component communication

## Key Design Patterns
- **Orchestrator Pattern**: Central coordinator
- **Component Pattern**: Modular components
- **Event-Driven**: Components communicate via events
- **Async/Await**: Non-blocking I/O operations

## Current Status
- ✅ Basic structure
- ✅ Initialization skeleton
- ⏳ Component initialization (TODO)
- ⏳ Main loop (TODO)
- ⏳ Graceful shutdown (TODO)

