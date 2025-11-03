# ZEMA - Implementation Guide
## Complete Code Structure and Module Details

**For:** Personal AI Assistant Development  
**Platform:** Raspberry Pi 5 + Python 3.11+  
**Approach:** Vibe Coding with Cursor AI  
**Last Updated:** November 1, 2025

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Module Details](#module-details)
3. [Web Dashboard UI](#web-dashboard)
4. [Voice-Based Configuration](#voice-config)
5. [Core Application Flow](#application-flow)
6. [Data Models](#data-models)
7. [Configuration System](#configuration)
8. [Testing Strategy](#testing)

---

## 1. Project Structure

```plaintext
zema-ai/
│
├── README.md                      # Project overview and quick start
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Poetry configuration
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── setup.sh                      # Raspberry Pi setup script
├── Dockerfile                    # Optional containerization
│
├── src/                          # Main source code
│   ├── __init__.py
│   ├── main.py                   # Application entry point
│   │
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py           # Settings class (Pydantic)
│   │   └── config_manager.py     # Voice/API config updates
│   │
│   ├── core/                     # Core system functionality
│   │   ├── __init__.py
│   │   ├── orchestrator.py       # Main control loop
│   │   └── state.py              # Application state management
│   │
│   ├── ai/                       # AI/NLP components
│   │   ├── __init__.py
│   │   ├── llm_client.py         # Ollama/Llama interface
│   │   ├── context_manager.py    # Conversation context
│   │   ├── system_prompts.py     # AI personality/instructions
│   │   └── response_parser.py    # Parse AI outputs
│   │
│   ├── voice/                    # Voice processing
│   │   ├── __init__.py
│   │   ├── audio_io.py           # Microphone/speaker interface
│   │   ├── vad.py                # Voice Activity Detection
│   │   ├── wakeword.py           # Wake word detection
│   │   ├── stt.py                # Speech-to-Text (Whisper)
│   │   └── tts.py                # Text-to-Speech (Piper)
│   │
│   ├── vision/                   # Computer vision
│   │   ├── __init__.py
│   │   ├── camera.py             # Insta360 Link 2 interface
│   │   ├── detector.py           # Object detection (YOLO)
│   │   ├── analyzer.py           # Scene analysis
│   │   ├── gestures.py           # Gesture recognition
│   │   ├── measurement.py        # Object measurement
│   │   └── model3d.py            # 3D model generation
│   │
│   ├── tools/                    # Assistant tools/skills
│   │   ├── __init__.py
│   │   ├── base.py               # Base tool interface
│   │   ├── tasks.py              # Tasks/reminders/calendar
│   │   ├── notes.py              # Note-taking
│   │   ├── knowledge.py          # Knowledge base queries
│   │   ├── recipes.py            # Ethiopian recipes
│   │   ├── web_search.py         # Web search (optional)
│   │   ├── smart_home.py         # Smart home control (optional)
│   │   └── system_config.py      # Voice-based system config
│   │
│   ├── users/                    # User management
│   │   ├── __init__.py
│   │   ├── profile.py            # User profiles
│   │   └── preferences.py        # User preferences
│   │
│   ├── data/                     # Data layer
│   │   ├── __init__.py
│   │   ├── database.py           # SQLite interface
│   │   ├── models.py             # Data models
│   │   └── migrations/           # Database migrations
│   │
│   ├── api/                      # Web API & Dashboard
│   │   ├── __init__.py
│   │   ├── server.py             # FastAPI app
│   │   ├── routes/               # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Configuration endpoints
│   │   │   ├── conversations.py  # Conversation history
│   │   │   ├── users.py          # User management
│   │   │   └── system.py         # System status/control
│   │   └── static/               # Web dashboard UI
│   │       ├── index.html        # Main dashboard
│   │       ├── css/
│   │       │   └── style.css     # Dashboard styles
│   │       └── js/
│   │           └── app.js        # Dashboard functionality
│   │
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── logger.py             # Logging configuration
│       ├── helpers.py            # Helper functions
│       └── constants.py          # Constants
│
├── data/                         # Data storage
│   ├── db/                       # SQLite databases
│   ├── models/                   # ML models
│   ├── audio/                    # Saved audio files
│   ├── images/                   # Saved images
│   ├── knowledge/                # Knowledge base files
│   └── exports/                  # Exported files (3D models, etc.)
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                 # Test fixtures
│
├── scripts/                      # Utility scripts
│   ├── download_models.sh        # Download AI models
│   ├── backup.sh                 # Backup data
│   └── cleanup.sh                # Clean up temp files
│
├── docs/                         # Documentation
│   ├── setup.md                  # Setup instructions
│   ├── usage.md                  # Usage guide
│   └── development.md            # Development guide
│
└── config/                       # Configuration files
    ├── systemd/                  # Systemd service files
    └── logging.yaml              # Logging configuration
```

---

## 2. Module Details

### src/main.py
**Purpose:** Application entry point

```python
"""
Zema AI Personal Assistant - Main Entry Point

This is the starting point for the Zema application.
It initializes all components and starts the main conversation loop.
"""

import asyncio
import signal
from src.core.orchestrator import Orchestrator
from src.api.server import start_dashboard
from src.config.settings import Settings
from src.utils.logger import setup_logging

async def main():
    """Main application entry point"""
    # Load configuration
    settings = Settings()
    
    # Setup logging
    setup_logging(settings.log_level)
    
    # Initialize orchestrator
    orchestrator = Orchestrator(settings)
    
    # Setup graceful shutdown
    def signal_handler(sig, frame):
        orchestrator.shutdown()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start web dashboard (in background)
    if settings.enable_dashboard:
        asyncio.create_task(start_dashboard(settings.dashboard_port))
        logger.info(f"Dashboard available at http://{settings.hostname}:{settings.dashboard_port}")
    
    # Start Zema voice assistant
    await orchestrator.start()

if __name__ == "__main__":
    asyncio.run(main())
```

**What it does:**
1. Loads configuration from environment/files
2. Sets up logging
3. Creates main orchestrator
4. **Starts web dashboard** (optional, configurable)
5. Handles shutdown signals gracefully
6. Starts the main event loop

---

### src/core/orchestrator.py
**Purpose:** Main control loop - coordinates all modules

```python
"""
Core Orchestrator

Manages the main event loop and coordinates all components:
- Voice input/output
- Vision processing
- AI processing
- Tool execution
- Voice-based configuration
"""

class Orchestrator:
    """Main controller for Zema"""
    
    def __init__(self, settings):
        """Initialize all components"""
        self.settings = settings
        self.state = ApplicationState()
        
        # Initialize modules
        self.wakeword = WakeWordDetector(settings.wakeword)
        self.vad = VoiceActivityDetector(settings.audio)
        self.stt = SpeechToText(settings.stt)
        self.llm = LLMClient(settings.llm)
        self.tts = TextToSpeech(settings.tts)
        self.camera = Camera(settings.camera)
        self.tools = ToolRegistry(settings.tools)
        self.config_manager = ConfigManager(settings)
        
    async def start(self):
        """Start the main loop"""
        logger.info("Zema starting...")
        
        # Start background tasks
        asyncio.create_task(self.wakeword.listen())
        asyncio.create_task(self.camera.monitor())
        
        # Main conversation loop
        while self.state.running:
            await self._conversation_loop()
            
    async def _conversation_loop(self):
        """Single conversation turn"""
        # 1. Wait for wake word or gesture
        await self.wakeword.wait_for_activation()
        
        # 2. Play activation sound
        await self.play_chime()
        
        # 3. Listen for voice input
        audio = await self.vad.listen()
        
        # 4. Convert speech to text
        text = await self.stt.transcribe(audio)
        
        # 5. Check if it's a configuration command
        if self._is_config_command(text):
            response = await self.config_manager.handle_voice_config(text)
            await self.tts.speak(response)
            return
        
        # 6. Get camera context if needed
        vision_context = None
        if self._needs_vision(text):
            vision_context = await self.camera.analyze()
        
        # 7. Get AI response
        response = await self.llm.generate(
            user_input=text,
            vision_context=vision_context,
            conversation_history=self.state.history
        )
        
        # 8. Execute any tool calls
        if response.tool_calls:
            tool_results = await self.tools.execute(response.tool_calls)
            response = await self.llm.generate(
                tool_results=tool_results,
                conversation_history=self.state.history
            )
        
        # 9. Speak response
        await self.tts.speak(response.text)
        
        # 10. Update conversation history
        self.state.add_turn(text, response.text)
        
    def _is_config_command(self, text: str) -> bool:
        """Check if user is trying to configure settings"""
        config_keywords = [
            "enable", "disable", "turn on", "turn off",
            "change", "switch", "settings", "configure"
        ]
        return any(keyword in text.lower() for keyword in config_keywords)
```

**What it does:**
1. Coordinates all modules (voice, vision, AI, tools)
2. Manages conversation flow
3. Handles wake word → listen → process → respond cycle
4. **Detects and handles voice configuration commands**
5. Maintains conversation state
6. Executes tool calls when needed

---

## 3. Web Dashboard UI

### Overview

The web dashboard provides a **user-friendly interface** for configuring and monitoring Zema without using command line.

**Access:** `http://zema.local:8000` (or Pi's IP address)

### src/api/server.py
**Purpose:** FastAPI web server for dashboard and API

```python
"""
Web Dashboard Server

Provides REST API and web interface for Zema configuration.
"""

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Zema Dashboard")

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

# Dashboard home
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve main dashboard page"""
    with open("src/api/static/index.html") as f:
        return f.read()

# System status
@app.get("/api/status")
async def get_status():
    """Get current system status"""
    return {
        "running": True,
        "uptime": "2h 34m",
        "cpu_usage": "35%",
        "memory_usage": "3.2 GB",
        "camera_connected": True,
        "microphone_connected": True
    }

# Configuration endpoints
@app.get("/api/config")
async def get_config():
    """Get current configuration"""
    return {
        "privacy_mode": "local",
        "wake_word": "hey zema",
        "language": "en",
        "voice": "en_US-lessac-medium",
        "camera_tracking": True,
        "gesture_control": True,
        "features": {
            "voice": True,
            "vision": True,
            "tasks": True,
            "ethiopian": True
        }
    }

@app.post("/api/config")
async def update_config(config: dict):
    """Update configuration"""
    # Save to settings
    # Reload Zema components if needed
    return {"success": True, "message": "Configuration updated"}

# User management
@app.get("/api/users")
async def get_users():
    """Get all user profiles"""
    return [
        {"id": 1, "name": "You", "role": "owner"},
        {"id": 2, "name": "Wife", "role": "member"},
        {"id": 3, "name": "Kid 1", "role": "limited"}
    ]

@app.post("/api/users")
async def create_user(user: dict):
    """Create new user profile"""
    return {"success": True, "user_id": 4}

# Conversation history
@app.get("/api/conversations")
async def get_conversations(limit: int = 50):
    """Get recent conversations"""
    return [
        {
            "id": 1,
            "timestamp": "2025-11-01T20:30:00",
            "user": "You",
            "query": "What time is it?",
            "response": "It's 8:30 PM",
            "language": "en"
        }
    ]

@app.delete("/api/conversations")
async def clear_conversations():
    """Clear all conversation history"""
    return {"success": True, "message": "History cleared"}

# Real-time updates via WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    while True:
        # Send status updates
        data = {"type": "status", "data": {"listening": True}}
        await websocket.send_json(data)
        await asyncio.sleep(1)

async def start_dashboard(port: int = 8000):
    """Start the dashboard server"""
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
```

### src/api/static/index.html
**Purpose:** Main dashboard interface

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zema Dashboard</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <h1>ዜማ Zema AI Assistant</h1>
            <div class="status">
                <span id="status-indicator" class="status-indicator active"></span>
                <span id="status-text">Active</span>
            </div>
        </header>

        <!-- Navigation -->
        <nav>
            <button class="nav-btn active" data-section="dashboard">Dashboard</button>
            <button class="nav-btn" data-section="settings">Settings</button>
            <button class="nav-btn" data-section="users">Users</button>
            <button class="nav-btn" data-section="conversations">History</button>
            <button class="nav-btn" data-section="privacy">Privacy</button>
        </nav>

        <!-- Dashboard Section -->
        <section id="dashboard" class="section active">
            <h2>System Status</h2>
            <div class="cards">
                <div class="card">
                    <h3>Voice</h3>
                    <p class="status-value">✓ Active</p>
                    <small>Listening for "Hey Zema"</small>
                </div>
                <div class="card">
                    <h3>Vision</h3>
                    <p class="status-value">✓ Active</p>
                    <small>Insta360 Link 2 connected</small>
                </div>
                <div class="card">
                    <h3>CPU</h3>
                    <p class="status-value" id="cpu-usage">35%</p>
                    <small>Raspberry Pi 5</small>
                </div>
                <div class="card">
                    <h3>Memory</h3>
                    <p class="status-value" id="memory-usage">3.2 GB</p>
                    <small>of 8 GB</small>
                </div>
            </div>

            <h3>Recent Activity</h3>
            <div id="recent-activity">
                <!-- Populated by JavaScript -->
            </div>
        </section>

        <!-- Settings Section -->
        <section id="settings" class="section">
            <h2>Configuration</h2>
            
            <div class="setting-group">
                <h3>Privacy Mode</h3>
                <select id="privacy-mode">
                    <option value="local">Local (Offline)</option>
                    <option value="hybrid">Hybrid (Smart)</option>
                    <option value="cloud">Cloud (Full Features)</option>
                </select>
                <p class="help-text">Controls whether Zema uses external APIs</p>
            </div>

            <div class="setting-group">
                <h3>Wake Word</h3>
                <input type="text" id="wake-word" value="hey zema">
                <p class="help-text">Say this to activate Zema</p>
            </div>

            <div class="setting-group">
                <h3>Language</h3>
                <select id="language">
                    <option value="en">English</option>
                    <option value="am">Amharic (አማርኛ)</option>
                    <option value="both">Both (Code-switching)</option>
                </select>
            </div>

            <div class="setting-group">
                <h3>Voice</h3>
                <select id="voice">
                    <option value="en_US-lessac-medium">Lessac (Male)</option>
                    <option value="en_US-amy-medium">Amy (Female)</option>
                    <option value="en_GB-alan-medium">Alan (British Male)</option>
                </select>
                <button id="test-voice">Test Voice</button>
            </div>

            <div class="setting-group">
                <h3>Camera Features</h3>
                <label>
                    <input type="checkbox" id="camera-tracking" checked>
                    AI Tracking (follows you)
                </label>
                <label>
                    <input type="checkbox" id="gesture-control" checked>
                    Gesture Control (wave to activate)
                </label>
            </div>

            <div class="setting-group">
                <h3>Features</h3>
                <label>
                    <input type="checkbox" id="feature-voice" checked disabled>
                    Voice Assistant (always on)
                </label>
                <label>
                    <input type="checkbox" id="feature-vision" checked>
                    Computer Vision
                </label>
                <label>
                    <input type="checkbox" id="feature-tasks" checked>
                    Tasks & Reminders
                </label>
                <label>
                    <input type="checkbox" id="feature-ethiopian" checked>
                    Ethiopian Cultural Features
                </label>
            </div>

            <button id="save-settings" class="btn-primary">Save Settings</button>
        </section>

        <!-- Users Section -->
        <section id="users" class="section">
            <h2>Family Members</h2>
            <button id="add-user" class="btn-primary">+ Add Family Member</button>
            
            <div id="user-list">
                <!-- Populated by JavaScript -->
            </div>
        </section>

        <!-- Conversations Section -->
        <section id="conversations" class="section">
            <h2>Conversation History</h2>
            <div class="actions">
                <button id="export-conversations">Export</button>
                <button id="clear-conversations" class="btn-danger">Clear All</button>
            </div>
            
            <div id="conversation-list">
                <!-- Populated by JavaScript -->
            </div>
        </section>

        <!-- Privacy Section -->
        <section id="privacy" class="section">
            <h2>Privacy & Data</h2>
            
            <div class="info-box">
                <h3>Your Data</h3>
                <p>All data is stored locally on your Raspberry Pi.</p>
                <p>Zema never sends data to external servers unless you enable cloud features.</p>
            </div>

            <div class="data-stats">
                <p>Conversations stored: <strong id="conversation-count">127</strong></p>
                <p>Images captured: <strong id="image-count">45</strong></p>
                <p>Audio recordings: <strong id="audio-count">0</strong></p>
                <p>Storage used: <strong id="storage-used">234 MB</strong></p>
            </div>

            <button id="export-data" class="btn-primary">Export All Data</button>
            <button id="delete-data" class="btn-danger">Delete All Data</button>
        </section>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
```

### Dashboard Features

**Dashboard Tab:**
- Real-time system status
- CPU/memory usage
- Camera/microphone status
- Recent activity feed
- Quick toggles (mute, privacy mode)

**Settings Tab:**
- Privacy mode selector
- Wake word customization
- Language selection
- Voice selection with preview
- Camera features (tracking, gestures)
- Enable/disable feature modules

**Users Tab:**
- Add family members
- Set permissions per user
- Voice profile training
- View user activity

**History Tab:**
- View all conversations
- Search conversations
- Export to file
- Clear history (with confirmation)

**Privacy Tab:**
- Data usage statistics
- Export all data
- Delete all data
- Review what's stored

---

## 4. Voice-Based Configuration

### src/tools/system_config.py
**Purpose:** Allow voice commands to change settings

```python
"""
Voice-Based System Configuration

Allows user to configure Zema settings using voice commands.
"""

class SystemConfigTool:
    """Handle voice-based configuration changes"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
    async def handle_command(self, command: str) -> str:
        """
        Process voice configuration command
        
        Examples:
        - "Enable privacy mode"
        - "Disable camera tracking"
        - "Change voice to female"
        - "Switch to Amharic"
        - "Turn off gesture control"
        """
        command = command.lower()
        
        # Privacy mode
        if "privacy mode" in command:
            if "enable" in command or "turn on" in command:
                await self.config_manager.set("privacy_mode", "local")
                return "Privacy mode enabled. All processing is now local."
            elif "disable" in command or "turn off" in command:
                return "Privacy mode is always on. I can switch to hybrid mode if you'd like."
                
        # Camera tracking
        elif "camera tracking" in command or "ai tracking" in command:
            if "enable" in command or "turn on" in command:
                await self.config_manager.set("camera.tracking", True)
                return "Camera tracking enabled. I'll follow you as you move."
            elif "disable" in command or "turn off" in command:
                await self.config_manager.set("camera.tracking", False)
                return "Camera tracking disabled."
                
        # Gesture control
        elif "gesture" in command:
            if "enable" in command or "turn on" in command:
                await self.config_manager.set("camera.gestures", True)
                return "Gesture control enabled. You can wave to activate me."
            elif "disable" in command or "turn off" in command:
                await self.config_manager.set("camera.gestures", False)
                return "Gesture control disabled."
                
        # Language
        elif "language" in command or "switch to" in command:
            if "amharic" in command:
                await self.config_manager.set("language", "am")
                return "[translate:ጤና ይስጥልኝ! አሁን በአማርኛ እናገራለሁ።]"  # Hello! I now speak in Amharic
            elif "english" in command:
                await self.config_manager.set("language", "en")
                return "Switched to English."
            elif "both" in command:
                await self.config_manager.set("language", "both")
                return "I'll now respond in both English and Amharic as appropriate."
                
        # Voice
        elif "voice" in command and "change" in command:
            if "female" in command:
                await self.config_manager.set("tts.voice", "en_US-amy-medium")
                return "Voice changed to female."
            elif "male" in command:
                await self.config_manager.set("tts.voice", "en_US-lessac-medium")
                return "Voice changed to male."
                
        # Show settings
        elif "show" in command and "settings" in command:
            settings = await self.config_manager.get_all()
            return f"Current settings: Privacy mode is {settings['privacy_mode']}, " \
                   f"language is {settings['language']}, " \
                   f"camera tracking is {'on' if settings['camera']['tracking'] else 'off'}."
                   
        else:
            return "I'm not sure how to change that setting. " \
                   "You can use the dashboard at http://zema.local:8000 for more options."
```

### Supported Voice Commands

**Privacy & Security:**
- "Enable privacy mode"
- "Switch to hybrid mode"
- "Show me my data"

**Camera:**
- "Enable/disable camera tracking"
- "Turn on/off gesture control"
- "Disable camera" (privacy mode)

**Language & Voice:**
- "Switch to Amharic"
- "Speak in both languages"
- "Change voice to female/male"

**Features:**
- "Disable vision features"
- "Turn off reminders"
- "Enable Ethiopian features"

**System:**
- "Show my settings"
- "Restart yourself"
- "What's my storage usage?"

---

## 5. Core Application Flow

### Startup Sequence

```
1. main.py executes
   ↓
2. Load settings from .env and config files
   ↓
3. Initialize logging
   ↓
4. Create Orchestrator with all modules
   ↓
5. Start web dashboard (background thread)
   ↓
6. Start background tasks:
   - Wake word listener
   - Camera monitor
   - Reminder checker
   ↓
7. Enter main conversation loop
```

### Conversation Flow with Config Detection

```
1. Wake word detected ("Hey Zema") or gesture
   ↓
2. Play activation chime
   ↓
3. VAD listens for speech
   ↓
4. Speech ends (silence detected)
   ↓
5. STT transcribes audio → text
   ↓
6. Check if configuration command
   ├─ Yes → SystemConfigTool handles it
   │         ↓
   │         Return response via TTS
   │         ↓
   │         Back to step 1
   └─ No → Continue normal flow
   ↓
7. Check if vision needed
   ├─ Yes → Capture frame, run detection
   └─ No → Continue
   ↓
8. Send to LLM with context
   ↓
9. LLM generates response
   ├─ Tool calls needed?
   │  ├─ Yes → Execute tools
   │  └─ Get final response
   └─ No → Continue
   ↓
10. TTS speaks response
   ↓
11. Update conversation history
   ↓
12. Update dashboard (WebSocket)
   ↓
13. Return to step 1
```

### Dashboard Update Flow

```
User changes setting in dashboard
   ↓
POST /api/config with new values
   ↓
Server validates settings
   ↓
Save to database
   ↓
Broadcast to Zema via event bus
   ↓
Zema reloads affected modules
   ↓
Confirm to user (voice if active)
   ↓
Dashboard shows success
```

---

## 6. Configuration System

### src/config/settings.py
**Purpose:** Centralized configuration with live updates

```python
"""
Settings Management

Pydantic-based configuration with environment variables
and live reload capability.
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Main configuration"""
    
    # General
    environment: str = "production"
    log_level: str = "INFO"
    hostname: str = "zema"
    
    # Dashboard
    enable_dashboard: bool = True
    dashboard_port: int = 8000
    
    # Wake Word
    wakeword_keywords: list[str] = ["hey zema", "zema"]
    wakeword_sensitivity: float = 0.5
    
    # Privacy
    privacy_mode: str = "local"  # local, hybrid, cloud
    data_retention_days: int = 30
    
    # Voice
    stt_model: str = "base"
    stt_language: str = "en"
    tts_engine: str = "piper"
    tts_voice: str = "en_US-lessac-medium"
    tts_speed: float = 1.0
    
    # Camera
    camera_device: int = 0
    camera_width: int = 1920
    camera_height: int = 1080
    camera_fps: int = 30
    camera_tracking: bool = True
    camera_gestures: bool = True
    
    # LLM
    llm_model: str = "llama3.2:3b"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 512
    
    # Features
    feature_voice: bool = True  # Always on
    feature_vision: bool = True
    feature_tasks: bool = True
    feature_ethiopian: bool = True
    
    # API Keys (optional)
    gemini_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

### src/config/config_manager.py
**Purpose:** Handle live configuration updates

```python
"""
Configuration Manager

Handles live updates to configuration without restarting Zema.
"""

class ConfigManager:
    """Manage configuration with live updates"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db = Database()
        self.event_bus = EventBus()
        
    async def set(self, key: str, value: any):
        """
        Set configuration value
        
        Args:
            key: Dot-notation key (e.g., "camera.tracking")
            value: New value
        """
        # Update in-memory settings
        self._set_nested(self.settings, key, value)
        
        # Save to database
        await self.db.execute(
            "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
            (key, json.dumps(value))
        )
        
        # Broadcast change event
        await self.event_bus.publish("config_changed", {
            "key": key,
            "value": value
        })
        
        logger.info(f"Configuration updated: {key} = {value}")
        
    async def get(self, key: str) -> any:
        """Get configuration value"""
        return self._get_nested(self.settings, key)
        
    async def get_all(self) -> dict:
        """Get all configuration as dictionary"""
        return self.settings.dict()
        
    def _set_nested(self, obj, key: str, value):
        """Set nested attribute using dot notation"""
        keys = key.split(".")
        for k in keys[:-1]:
            obj = getattr(obj, k)
        setattr(obj, keys[-1], value)
        
    def _get_nested(self, obj, key: str):
        """Get nested attribute using dot notation"""
        keys = key.split(".")
        for k in keys:
            obj = getattr(obj, k)
        return obj
```

---

## 7. User Interface Options Summary

### Three Ways to Configure Zema

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| **Web Dashboard** | Primary configuration | • Visual interface<br>• All settings accessible<br>• Works from any device<br>• No command line needed | • Requires browser<br>• Must be on same network |
| **Voice Commands** | Quick changes during use | • Hands-free<br>• Natural<br>• Fast for simple changes | • Limited settings<br>• Must remember commands |
| **SSH/Command Line** | Advanced configuration | • Full system access<br>• Can edit .env directly<br>• Scriptable | • Technical knowledge needed<br>• Not user-friendly |

### Recommended Workflow

1. **Initial Setup:** Use command line (follow Infrastructure Guide)
2. **Daily Use:** Voice commands for quick toggles
3. **Detailed Config:** Web dashboard for everything else
4. **Advanced:** SSH for system-level changes

---

*Continue to Part 2 for Data Models, Testing Strategy, and complete Cursor prompts...*