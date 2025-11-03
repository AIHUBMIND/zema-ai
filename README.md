# Zema AI - Privacy-First Voice Assistant

Zema is a smart hybrid voice assistant designed for mini PCs. It automatically uses online services when Internet is available for better accuracy, and seamlessly falls back to local LLM (Ollama) when offline. Built with Python 3.11+, FastAPI, and intelligent connectivity detection.

## Features

- **Smart Hybrid Mode**: Automatically detects Internet connectivity and switches between online services (preferred) and local LLM (fallback)
  - **Internet Available**: Uses online services for real-time data and better accuracy
  - **Internet Unavailable**: Falls back to local Ollama LLM for 100% offline operation
  - **Seamless Switching**: Automatically adapts to connectivity changes without user intervention
- **Privacy-First**: All data stays local when offline; online data usage is configurable
- **Offline-Capable**: Core features work without internet using local LLM
- **Voice Interaction**: Wake word detection, speech-to-text, text-to-speech
- **Computer Vision**: Object detection, scene analysis, gesture recognition
- **Local LLM**: Uses Ollama with Llama models for offline AI fallback
- **Web Dashboard**: Configuration and monitoring interface with logs viewer (v0.1.1)
- **Multi-Language**: Support for English and Amharic

## Quick Start

### Prerequisites

- Python 3.11+
- Ubuntu 22.04 (for production on BOSGAME P3 Lite)
- Ollama installed locally
- Insta360 Link 2 camera (optional, for vision features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AIHUBMIND/zema-ai.git
cd zema-ai
```

2. Run setup script (Linux):
```bash
bash setup.sh
```

3. Activate virtual environment:
```bash
source venv/bin/activate
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Download models:
```bash
bash scripts/download_models.sh
```

6. Verify hardware:
```bash
python scripts/verify_hardware.py
```

7. Start Zema:
```bash
python src/main.py
```

## Project Structure

```
zema-ai/
├── src/                  # Source code
│   ├── core/            # Core orchestrator and state
│   ├── config/          # Configuration management
│   ├── voice/           # Voice I/O, STT, TTS
│   ├── vision/          # Camera and vision processing
│   ├── ai/              # LLM client and context
│   ├── tools/            # Personal assistant tools
│   ├── api/             # FastAPI server and routes
│   └── utils/            # Utilities and helpers
├── data/                 # Data directory
│   ├── db/              # Database files
│   ├── logs/            # Log files
│   ├── models/          # AI models
│   └── ...
├── tests/                # Tests
├── scripts/              # Utility scripts
└── docs/                 # Documentation
```

## Configuration

Configuration is managed through `.env` file and Pydantic Settings. See `.env.example` for all available options.

Key settings:
- `LLM_MODEL`: Ollama model name (e.g., `llama2:13b`) - used when offline
- `CONNECTION_MODE`: Connection mode (`auto`, `local`, `online`) - `auto` enables smart hybrid mode
- `INTERNET_CHECK_URL`: URL to check Internet connectivity (default: `https://www.google.com`)
- `CAMERA_DEVICE`: Camera device index
- `WAKEWORD_KEYWORDS`: Wake word phrases

**Connection Modes:**
- `auto`: Automatically detects Internet and switches between online/local (default)
- `local`: Always use local LLM (offline-only mode)
- `online`: Always use online services (requires Internet)

## Usage

### Voice Interaction

1. Wake word: Say "Hey Zema" or configured wake words
2. Speak your request
3. Zema processes and responds

### Web Dashboard

Access dashboard at `http://localhost:8000` (default)

### Configuration via Voice

- "Enable privacy mode"
- "Disable camera tracking"
- "Switch to Amharic"
- "Set voice speed to 1.5"

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

- Follow PEP 8
- Use type hints
- Async/await for I/O operations
- Pydantic for validation

## License

[Add your license here]

## Contributing

[Add contributing guidelines]

## Support

[Add support information]
