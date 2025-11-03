# ZEMA AI - Detailed Code Documentation

**Purpose:** Beginner-friendly documentation explaining every file, function, and why it exists  
**Last Updated:** 2025-11-02  
**Auto-Updated:** Yes (after each task completion)  
**Location:** `docs/architecture/CODE_DOCUMENTATION.md`

---

## 📚 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [File-by-File Documentation](#file-by-file-documentation)
4. [Function Reference](#function-reference)
5. [How Components Work Together](#how-components-work-together)

---

## 🎯 Project Overview

**What is Zema AI?**
Zema AI is a privacy-first, offline voice assistant designed to run on a mini PC (BOSGAME P3 Lite). It uses local AI models (Ollama with Llama 13B) to process voice commands, handle conversations, and assist with tasks - all without requiring internet connection.

**Why Privacy-First?**
- All data stays on your device
- No cloud services
- No data collection
- Complete offline operation

**Key Technologies:**
- **Python 3.11+** - Modern Python with async/await
- **FastAPI** - Web framework for dashboard
- **Pydantic** - Data validation and settings
- **Ollama** - Local LLM inference
- **Faster Whisper** - Speech-to-text
- **PyAudio** - Audio I/O
- **OpenCV** - Computer vision

---

## 🏗️ Architecture Overview

### High-Level Flow

```
User Voice Input
    ↓
Wake Word Detection ("Hey Zema")
    ↓
Voice Activity Detection (detect when user stops speaking)
    ↓
Speech-to-Text (convert audio to text)
    ↓
LLM Processing (understand intent, generate response)
    ↓
Text-to-Speech (convert response to audio)
    ↓
Audio Output (speaker)
```

### Component Layers

```
┌─────────────────────────────────────────┐
│      Web Dashboard (FastAPI)            │
│      - Visual interface                 │
│      - Real-time status                 │
│      - Configuration                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Core Orchestrator                  │
│      - Coordinates all components       │
│      - Manages conversation loop       │
│      - Handles state                   │
└─────────────────────────────────────────┘
         ↓          ↓          ↓
    ┌────────┐ ┌────────┐ ┌────────┐
    │ Voice  │ │ Vision │ │ AI     │
    │ Module │ │ Module │ │ Module │
    └────────┘ └────────┘ └────────┘
```

---

## 📁 File-by-File Documentation

### Root Files

#### `src/main.py`
**Purpose:** Application entry point - where everything starts

**What it does:**
- Initializes logging system
- Sets up the main application
- Starts the orchestrator (main control loop)
- Handles shutdown gracefully

**Why it exists:**
Every Python application needs a starting point. This file is what you run to start Zema AI.

**Key Functions:**

```python
async def main() -> None:
    """Main application entry point"""
```

**What `main()` does:**
1. Calls `setup_logging()` to configure logging (console + file)
2. Logs startup information
3. Creates an `Orchestrator` instance
4. Starts the orchestrator (begins listening for voice commands)

**Why async?**
Modern Python uses async/await for I/O operations (like waiting for audio input, making API calls). This allows the program to do other things while waiting.

**Example Usage:**
```bash
python src/main.py
```

---

#### `src/config/settings.py`
**Purpose:** Comprehensive configuration management using Pydantic Settings

**What it does:**
- Defines all application settings organized by category
- Validates configuration values with type checking and constraints
- Loads settings from environment variables or `.env` file
- Provides sensible default values for all settings
- Includes field validators for complex validation logic

**Why it exists:**
Instead of hardcoding values throughout the code, all settings are centralized in one place. This makes it easy to:
- Change settings without editing code
- Validate that settings are correct (e.g., port must be 1024-65535)
- Use different settings for development/production
- Override settings via environment variables
- Get type-safe access to all configuration

**Key Classes:**

```python
class PrivacyMode(str, Enum):
    """Privacy mode options: LOCAL, HYBRID, CLOUD"""
    
class Settings(BaseSettings):
    """Application settings with validation"""
```

**What Settings contains:**

**General Settings:**
- `environment`: Environment mode ("development" or "production")
- `log_level`: Logging level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
- `hostname`: System hostname ("zema")

**Dashboard Settings:**
- `enable_dashboard`: Enable web dashboard (True/False)
- `dashboard_port`: Dashboard port (1024-65535, default: 8000)
- `dashboard_host`: Dashboard host ("0.0.0.0")

**Wake Word Settings:**
- `wakeword_keywords`: List of wake word phrases (default: ["hey zema", "zema"])
- `wakeword_sensitivity`: Sensitivity level (0.0-1.0, default: 0.5)

**Privacy Settings:**
- `privacy_mode`: Privacy mode (PrivacyMode enum: LOCAL, HYBRID, CLOUD)
- `data_retention_days`: Data retention period (1-365 days, default: 30)

**Audio Settings:**
- `audio_sample_rate`: Audio sample rate in Hz (default: 16000)
- `audio_channels`: Audio channels (1 or 2, default: 1)
- `audio_device_name`: Optional audio device name

**Voice Settings:**
- `stt_model`: Speech-to-text model ("tiny", "base", "small", "medium")
- `stt_language`: STT language ("en", "am", "auto")
- `tts_engine`: Text-to-speech engine ("piper")
- `tts_voice`: TTS voice model ("en_US-lessac-medium")
- `tts_speed`: TTS speed multiplier (0.5-2.0, default: 1.0)

**Camera Settings:**
- `camera_device`: Camera device index (default: 0)
- `camera_width`: Camera width in pixels (default: 1920)
- `camera_height`: Camera height in pixels (default: 1080)
- `camera_fps`: Camera frames per second (1-60, default: 30)
- `camera_tracking`: Enable camera tracking (True/False)
- `camera_gestures`: Enable gesture recognition (True/False)

**LLM Settings:**
- `llm_model`: Ollama model name (default: "llama2:13b")
- `llm_temperature`: LLM temperature (0.0-2.0, default: 0.7)
- `llm_max_tokens`: Maximum tokens per response (1-4096, default: 512)
- `llm_system_prompt`: System prompt for LLM

**Vision Settings:**
- `vision_detection_model`: Detection model name (default: "yolov8n")
- `vision_confidence_threshold`: Confidence threshold (0.0-1.0, default: 0.5)

**Feature Flags:**
- `feature_voice`: Enable voice features (True/False)
- `feature_vision`: Enable vision features (True/False)
- `feature_tasks`: Enable task management (True/False)
- `feature_ethiopian`: Enable Ethiopian features (True/False)

**API Keys (Optional):**
- `gemini_api_key`: Gemini API key (optional)
- `elevenlabs_api_key`: ElevenLabs API key (optional)

**Database Settings:**
- `database_url`: Database connection URL (default: SQLite)

**Field Validators:**
The Settings class includes validators for:
- `privacy_mode`: Ensures valid privacy mode value
- `log_level`: Ensures valid log level (uppercased)
- `stt_model`: Ensures valid STT model name (lowercased)

**Why Pydantic Settings?**
Pydantic Settings automatically:
- Validates that values are the correct type (e.g., port must be an integer)
- Enforces constraints (e.g., port must be between 1024-65535)
- Provides helpful error messages if validation fails
- Loads from environment variables automatically
- Supports `.env` file loading
- Provides type-safe access to all settings
- Handles type conversion (e.g., "true" → True)

**Example Usage:**
```python
from src.config.settings import settings, PrivacyMode

# Access settings with type safety
print(settings.environment)  # "production"
print(settings.dashboard_port)  # 8000
print(settings.privacy_mode)  # PrivacyMode.LOCAL

# Settings automatically load from .env file if it exists
# Environment variables override defaults
# Type validation happens automatically
```

**Configuration File:**
Settings can be configured via `.env` file (copy from `.env.example`):
```env
ENVIRONMENT=production
LOG_LEVEL=INFO
DASHBOARD_PORT=8000
PRIVACY_MODE=local
LLM_MODEL=llama2:13b
# ... etc
```

---

#### `src/utils/logger.py`
**Purpose:** Structured logging system for the entire application

**What it does:**
- Sets up logging with two outputs:
  - Console output (for development) - uses `rich` library for pretty colors
  - File output (for production) - saves logs as JSON
- Provides a performance logging decorator

**Why it exists:**
Logging helps you:
- Debug problems
- Monitor performance
- Track what the application is doing
- Investigate issues after they happen

**Key Functions:**

```python
def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging with console (rich) and file (JSON) handlers"""
```

**What `setup_logging()` does:**
1. Creates `data/logs/` directory if it doesn't exist
2. Sets up console handler (shows logs in terminal with colors)
3. Sets up file handler (saves logs to `data/logs/zema.log` as JSON)
4. Configures log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)

**Why JSON format for files?**
JSON logs can be easily parsed by log analysis tools, searched, and analyzed. Structured logging makes debugging easier.

**Performance Decorator:**

```python
@log_performance
async def my_function():
    # Your code here
```

**What it does:**
Automatically logs:
- When function starts
- How long it took to execute
- Any errors that occurred

**Example Usage:**
```python
from src.utils.logger import setup_logging, get_logger

setup_logging("INFO")  # Must be called first
logger = get_logger(__name__)

logger.info("Application started")
logger.error("Something went wrong")
```

---

### Core Module (`src/core/`)

#### `src/core/orchestrator.py`
**Purpose:** Main controller that coordinates all components

**What it does:**
- Manages the main conversation loop
- Coordinates voice, vision, AI, and tools
- Handles the flow from wake word → response
- Manages application lifecycle (start/stop)

**Why it exists:**
Without an orchestrator, components wouldn't know how to work together. It's like a conductor directing an orchestra.

**Key Classes:**

```python
class Orchestrator:
    """Main orchestrator for Zema AI"""
```

**Key Methods:**

```python
async def start(self) -> None:
    """Start the main conversation loop"""
```

**What happens in `start()`:**
1. Initializes all components (voice, AI, tools)
2. Enters main loop:
   - Wait for wake word
   - Listen for user input
   - Process with AI
   - Generate response
   - Speak response
   - Repeat

**Example Flow:**
```
1. User says "Hey Zema"
2. Orchestrator detects wake word
3. Orchestrator starts listening
4. User asks question
5. Orchestrator sends to AI
6. AI generates response
7. Orchestrator speaks response
8. Back to waiting for wake word
```

---

#### `src/core/state.py`
**Purpose:** Manages application state and conversation history

**What it does:**
- Tracks conversation history
- Manages system state (listening, processing, etc.)
- Stores user preferences
- Provides state information to other components

**Why it exists:**
Components need to know:
- What was said before (context)
- Whether system is currently listening
- Current user information
- System status

**Key Classes:**

```python
class ConversationTurn:
    """Single conversation turn"""
```

**What it stores:**
- `user_input`: What the user said
- `assistant_response`: What Zema responded
- `timestamp`: When it happened
- `context`: Additional context (vision, tools used, etc.)

```python
class ApplicationState:
    """Global application state"""
```

**What it tracks:**
- `conversation_history`: List of all conversation turns
- `is_listening`: Whether currently listening for input
- `is_processing`: Whether currently processing a request
- `current_user`: Who is currently using the system

**Example Usage:**
```python
from src.core.state import ApplicationState

state = ApplicationState()
state.add_conversation_turn("Hello", "Hi! How can I help?")
recent = state.get_recent_history(limit=5)  # Get last 5 conversations
```

---

### Voice Module (`src/voice/`)

#### `src/voice/audio_io.py`
**Purpose:** Handles microphone input and speaker output

**What it does:**
- Detects available audio devices
- Manages audio streams (input/output)
- Records audio from microphone
- Plays audio to speakers
- Handles errors and recovery

**Why it exists:**
Audio I/O is complex. This module abstracts away the complexity and provides a simple interface for:
- Recording what the user says
- Playing responses

**Key Classes:**

```python
class AudioIO:
    """Audio input/output manager"""
```

**What it manages:**
- `pyaudio`: PyAudio library instance (handles audio hardware)
- `input_stream`: Stream for microphone input
- `output_stream`: Stream for speaker output
- `device_info`: Information about available audio devices

**Why separate input/output?**
- Different devices might be used for input vs output
- Allows more control over each stream
- Better error handling

---

#### `src/voice/wakeword.py`
**Purpose:** Detects wake words like "Hey Zema"

**What it does:**
- Listens continuously for wake words
- Uses Porcupine or openwakeword library
- Detects when user says the wake phrase
- Wakes up the system when detected

**Why it exists:**
To save battery/resources, the system doesn't process everything. It only activates when it hears the wake word.

**Key Classes:**

```python
class WakeWordDetector:
    """Detect wake words using Porcupine or openwakeword"""
```

**Key Methods:**

```python
async def wait_for_wake_word(self) -> Optional[str]:
    """Wait for wake word detection"""
```

**What it does:**
1. Continuously listens to audio stream
2. Analyzes audio for wake word patterns
3. Returns wake word name when detected (e.g., "hey zema")
4. Returns None if timeout

**How it works:**
- Uses machine learning models trained to recognize specific phrases
- Processes audio in real-time
- Low latency (responds quickly)

---

### AI Module (`src/ai/`)

#### `src/ai/llm_client.py`
**Purpose:** Interface to Ollama for AI responses (100% OFFLINE)

**What it does:**
- Connects to local Ollama server
- Sends prompts to LLM
- Receives AI-generated responses
- Manages conversation history
- Handles streaming responses

**Why it exists:**
This is the "brain" of Zema. It understands user input and generates intelligent responses.

**Key Classes:**

```python
class LLMClient:
    """Client for Ollama LLM - OFFLINE ONLY"""
```

**CRITICAL:** All LLM calls go to `localhost:11434` - no internet required!

**Key Methods:**

```python
async def generate(self, user_input: str, context: Optional[Dict] = None) -> str:
    """Generate response from LLM (OFFLINE)"""
```

**What it does:**
1. Builds message list with:
   - System prompt (instructions for the AI)
   - Conversation history (last 10 exchanges)
   - Current user input
   - Context (vision, tools, etc.)
2. Sends to Ollama API (`http://localhost:11434/api/chat`)
3. Receives response
4. Updates conversation history
5. Returns response text

**Why offline?**
- Privacy: Your conversations never leave your device
- Speed: No network latency
- Reliability: Works without internet
- Cost: No API fees

**Example Usage:**
```python
from src.ai.llm_client import LLMClient
from src.config.settings import settings

llm = LLMClient(settings)
response = await llm.generate("What's the weather like?")
print(response)  # AI-generated response
```

---

### API Module (`src/api/`)

#### `src/api/server.py`
**Purpose:** FastAPI web server for dashboard

**What it does:**
- Runs web server (FastAPI)
- Serves dashboard HTML/CSS/JS
- Provides API endpoints
- Handles WebSocket connections for real-time updates

**Why it exists:**
Users need a visual interface to:
- See system status
- Configure settings
- View conversation history
- Monitor system health

**Key Components:**

```python
app = FastAPI(title="Zema Dashboard", version="1.0.0")
```

**Routes:**

```python
@app.get("/")
async def dashboard() -> HTMLResponse:
    """Serve main dashboard page"""
```

**WebSocket:**

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket for real-time updates"""
```

**What WebSocket does:**
- Maintains persistent connection
- Sends real-time status updates
- Updates dashboard without page refresh
- Shows listening status, processing state, etc.

#### `src/api/routes/logs.py`
**Purpose:** API endpoints for viewing application logs

**What it does:**
- Provides REST API endpoints for reading logs
- Supports filtering by log level and search terms
- Provides real-time log streaming via Server-Sent Events (SSE)
- Returns log statistics (file size, line counts, level distribution)
- Allows clearing log file

**Why it exists:**
Enables users to view logs through the web dashboard UI instead of using command line. Makes debugging and monitoring easier.

**Key Endpoints:**

```python
@router.get("/api/logs")
async def get_logs(
    limit: int = 100,
    level: Optional[str] = None,
    search: Optional[str] = None,
    tail: bool = True
) -> Dict[str, Any]
```

**What `get_logs()` does:**
1. Reads log file (`data/logs/zema.log`)
2. Parses JSON log entries
3. Filters by level if specified
4. Filters by search term if specified
5. Returns last N entries (tail) or first N entries
6. Returns log entries with metadata

**Real-time Streaming:**

```python
@router.get("/api/logs/stream")
async def stream_logs()
```

**What it does:**
- Uses Server-Sent Events (SSE) for real-time log streaming
- Sends new log entries as they're written to file
- Allows dashboard to show live logs without polling

**Statistics Endpoint:**

```python
@router.get("/api/logs/stats")
async def get_log_stats() -> Dict[str, Any]
```

**What it does:**
- Returns log file statistics
- Counts logs by level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Shows file size and line count
- Shows last modified timestamp

**Example Usage:**
```python
# Get last 100 logs
GET /api/logs?limit=100&tail=true

# Get only ERROR logs
GET /api/logs?level=ERROR&limit=50

# Search logs
GET /api/logs?search=camera&limit=100

# Get log statistics
GET /api/logs/stats

# Stream logs in real-time
GET /api/logs/stream
```

**Integration:**
- Used by dashboard JavaScript to display logs
- Logs are displayed in real-time when Live Stream is enabled
- Supports filtering and searching from UI
- JSON format makes parsing easy

---

## 🔄 How Components Work Together

### Example: User asks "What time is it?"

```
1. User speaks: "Hey Zema"
   ↓
   WakeWordDetector detects wake word
   ↓
   Orchestrator starts listening
   ↓
2. User says: "What time is it?"
   ↓
   AudioIO records audio
   ↓
   SpeechToText converts audio → text
   ↓
   Orchestrator receives text
   ↓
3. Orchestrator sends to LLMClient
   ↓
   LLMClient calls Ollama API
   ↓
   Ollama generates response: "It's 3:45 PM"
   ↓
   LLMClient returns response
   ↓
4. Orchestrator receives response
   ↓
   TextToSpeech converts text → audio
   ↓
   AudioIO plays audio to speaker
   ↓
   User hears: "It's 3:45 PM"
   ↓
5. State records conversation turn
   ↓
   Orchestrator goes back to waiting for wake word
```

---

## 📝 Function Reference

### Logging Functions

#### `setup_logging(log_level: str = "INFO") -> None`
**Purpose:** Initialize logging system  
**Parameters:**
- `log_level`: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
**Returns:** None  
**Side Effects:** Sets up console and file logging

#### `get_logger(name: str) -> logging.Logger`
**Purpose:** Get logger instance for a module  
**Parameters:**
- `name`: Logger name (usually `__name__`)
**Returns:** Logger instance

#### `@log_performance`
**Purpose:** Decorator to log function execution time  
**Usage:** `@log_performance` before function definition  
**Automatically logs:** Start time, duration, errors

---

## 🎓 Beginner-Friendly Explanations

### What is async/await?
**Think of it like:** Waiting for a pizza delivery. While waiting, you can do other things (like watch TV). When the pizza arrives, you handle it.

**In code:**
```python
# Sync (bad - blocks everything):
result = slow_operation()  # Everything stops here
print(result)

# Async (good - non-blocking):
result = await slow_operation()  # Can do other things while waiting
print(result)
```

### What is Pydantic?
**Think of it like:** A strict form validator. It checks:
- Is this a valid email? ✅
- Is this a number between 0-100? ✅
- Is this text not empty? ✅

**Why it helps:** Catches errors early, before they cause problems.

### What is a decorator?
**Think of it like:** A wrapper around a gift. The decorator adds extra functionality without changing the gift itself.

**Example:**
```python
@log_performance  # This decorator adds logging
def my_function():
    return "Hello"
```

Now `my_function()` automatically logs when it starts and finishes!

---

## 🔄 Auto-Update Instructions

This document is automatically updated after each task completion by `scripts/maintenance/update_docs.py`.

**To manually update:**
```bash
python scripts/maintenance/update_docs.py
```

**What gets updated:**
- New files documented
- New functions explained
- Usage examples added
- Architecture diagrams updated

---

**Last Updated:** 2025-11-03  
**Total Files Documented:** 52  
**Auto-Update Status:** ✅ Enabled

