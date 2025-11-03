# Zema AI Personal Assistant

A privacy-first voice assistant designed for mini PC (BOSGAME P3 Lite) running Ubuntu 22.04.

## Features

- **Privacy-First**: All data stored locally, no cloud dependencies
- **Offline-First**: Core features work without internet connection
- **Voice Assistant**: Wake word detection, speech-to-text, text-to-speech
- **Vision Processing**: Camera integration for visual context
- **Local LLM**: Uses Ollama with Llama 13B for 100% offline inference
- **FastAPI Backend**: Modern async API for interactions

## Requirements

- Python 3.11+
- Ubuntu 22.04 (tested on BOSGAME P3 Lite mini PC)
- Ollama with Llama 13B model installed locally

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ZEMA-AI
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration:
```bash
cp data/config/config.example.yaml data/config/config.yaml
# Edit config.yaml with your settings
```

5. Run the application:
```bash
python -m src.main
```

## Project Structure

```
zema-ai/
├── src/
│   ├── core/          # Core orchestrator, state management
│   ├── config/        # Configuration management (Pydantic)
│   ├── voice/         # Voice I/O, wake word, STT, TTS
│   ├── vision/        # Camera, vision processing
│   ├── ai/            # LLM client, context management
│   ├── tools/         # Personal assistant tools
│   ├── api/           # FastAPI server, routes
│   └── utils/         # Utilities, logging, helpers
├── scripts/           # Setup, verification, utility scripts
├── tests/             # Unit tests, integration tests
├── data/              # Data directory
│   ├── config/        # Configuration files
│   ├── logs/          # Log files
│   ├── db/            # Database files
│   ├── models/        # AI model files
│   └── backups/       # Backup files
└── docs/              # Documentation
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
Follow PEP 8 and use type hints. All code should be async-first.

## License

[Specify your license here]

## Contributing

[Add contributing guidelines]

