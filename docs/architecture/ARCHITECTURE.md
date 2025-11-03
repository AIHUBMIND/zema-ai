# ZEMA AI - Architecture Documentation

**Purpose:** High-level system architecture and design decisions  
**Last Updated:** 2025-11-02  
**Auto-Updated:** Yes

---

## 🏗️ System Architecture

### Overview

Zema AI follows a **modular, event-driven architecture** designed for:
- **Smart Hybrid Mode:** Automatically detects Internet connectivity and switches between online services (preferred) and local LLM (fallback)
- **Privacy:** All processing happens locally when offline; online data usage is configurable
- **Offline-first:** Core features work without internet using local LLM as fallback
- **Modularity:** Components can be tested and replaced independently
- **Scalability:** Easy to add new features

---

## 📐 Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                     │
│              (Web Dashboard, Voice I/O)                  │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                    Orchestration Layer                    │
│              (Core Orchestrator, State)                 │
└─────────────────────────────────────────────────────────┘
         ↕              ↕              ↕
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Voice Layer │ │  Vision Layer│ │   AI Layer    │
└──────────────┘ └──────────────┘ └──────────────┘
         ↕              ↕              ↕
┌─────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                   │
│        (Config, Logging, Database, Tools)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Voice Interaction Flow

```
User Voice
    ↓
[AudioIO] → Capture audio
    ↓
[WakeWordDetector] → Detect "Hey Zema"
    ↓
[AudioIO] → Continue recording
    ↓
[VAD] → Detect end of speech
    ↓
[STT] → Convert audio to text
    ↓
[Orchestrator] → Route to appropriate handler
    ↓
[LLMClient] → Generate response
    ↓
[ResponseParser] → Parse response, extract tool calls
    ↓
[Tools] → Execute tools if needed
    ↓
[LLMClient] → Generate final response
    ↓
[TTS] → Convert text to speech
    ↓
[AudioIO] → Play audio
    ↓
[State] → Record conversation turn
```

---

## 🧩 Component Responsibilities

### Core Orchestrator
**Responsibility:** Coordinates all components, manages main loop
**Dependencies:** All modules
**Provides:** Main entry point, component coordination

### Voice Module
**Responsibility:** Audio I/O, wake word, STT, TTS, VAD
**Dependencies:** AudioIO, Settings
**Provides:** Voice interaction capabilities

### Vision Module
**Responsibility:** Camera control, object detection, gesture recognition
**Dependencies:** Camera, Settings
**Provides:** Computer vision capabilities

### AI Module
**Responsibility:** LLM interaction, context management
**Dependencies:** Ollama (local), Settings
**Provides:** Natural language understanding and generation

### Tools Module
**Responsibility:** Personal assistant tools (tasks, notes, knowledge)
**Dependencies:** Database, Settings
**Provides:** Actionable capabilities

### API Module
**Responsibility:** Web dashboard, REST API, WebSocket
**Dependencies:** FastAPI, Settings
**Provides:** Visual interface and API access

---

## 🔐 Privacy & Security Design

### Data Storage
- **All data stored locally:** `data/` directory
- **No cloud sync:** Everything stays on device
- **Encrypted database:** SQLite with encryption (optional)

### Network & Connectivity Strategy
- **Smart Connectivity Detection:** Automatically detects Internet availability
- **Hybrid Mode:** Uses online services when available, falls back to local LLM when offline
- **Ollama local fallback:** `localhost:11434` (always available as fallback)
- **Online preference:** When Internet is available, uses online services for better accuracy
- **Seamless switching:** Automatically adapts to connectivity changes
- **No telemetry:** Zero data collection
- **Optional web access:** Dashboard only accessible locally by default

### User Control
- **Privacy mode:** Disable recording when needed
- **Data deletion:** Easy to clear all data
- **Transparency:** All processing visible in logs

---

## ⚡ Performance Considerations

### Async Architecture
- **Non-blocking I/O:** All I/O operations use async/await
- **Concurrent processing:** Can handle multiple requests
- **Resource efficient:** Doesn't block on slow operations

### Caching Strategy
- **Conversation history:** Kept in memory (last 100 turns)
- **Model caching:** Ollama caches models in memory
- **Config caching:** Settings loaded once, cached

### Resource Management
- **Audio streams:** Properly closed when not in use
- **Camera:** Released when not needed
- **Memory limits:** Conversation history limited to prevent memory issues

---

## 🧪 Testing Strategy

### Unit Tests
- **Individual components:** Each module tested independently
- **Mock external dependencies:** Audio, camera, LLM mocked
- **Fast execution:** Tests run quickly

### Integration Tests
- **Component interaction:** Test how components work together
- **Real hardware:** Test with actual devices when possible
- **End-to-end:** Full conversation flow tests

### Hardware Tests
- **Device detection:** Verify audio/video devices work
- **Performance:** Benchmark on target hardware
- **Reliability:** Stress testing

---

## 🔄 Update & Maintenance

### Version Control
- **Git:** All code in Git repository
- **Auto-commit:** Changes automatically committed
- **Version tracking:** Semantic versioning

### Configuration Management
- **Environment variables:** `.env` file for settings
- **Live updates:** Settings can change without restart
- **Validation:** Pydantic validates all settings

### Logging & Monitoring
- **Structured logs:** JSON format for analysis
- **Performance metrics:** Automatic performance logging
- **Error tracking:** Comprehensive error logging

---

**Last Updated:** 2025-11-02  
**Architecture Version:** 1.0

