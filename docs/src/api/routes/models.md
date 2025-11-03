# models.py Documentation

## File Location
`src/api/routes/models.py`

## Purpose
API routes for managing Ollama models. Provides endpoints to list available models, download models, delete models, and check model status. Supports Qwen, Aya, Llama, and Mistral models for multilingual and translation capabilities.

## Why It Was Created
To provide UI-first model management for Zema AI. Users can download, manage, and switch between different LLM models directly from the Settings Dashboard without using command-line tools.

## How It Works

### Model Metadata
The `AVAILABLE_MODELS` dictionary contains metadata for all supported models:
- Model name and size
- Supported languages
- Strengths and use cases
- Recommendation flags

### Function: `run_ollama_command(command: List[str]) -> Dict[str, Any]`
**Purpose**: Execute Ollama commands asynchronously
**How it works**:
1. Creates subprocess to run `ollama` command
2. Captures stdout and stderr
3. Returns success status and output
**Returns**: Dictionary with success status, exit code, stdout, stderr

### Endpoint: `GET /api/models/available`
**Purpose**: List all available models with metadata
**Returns**: List of models with install status, size, languages, recommendations

### Endpoint: `GET /api/models/list`
**Purpose**: List installed Ollama models
**Returns**: List of installed models parsed from `ollama list` output

### Endpoint: `POST /api/models/download/{model_name}`
**Purpose**: Download an Ollama model
**How it works**:
1. Validates model name exists in AVAILABLE_MODELS
2. Checks if model is already installed
3. Runs `ollama pull {model_name}` command
4. Returns download status
**Returns**: Success status and download output

### Endpoint: `DELETE /api/models/{model_name}`
**Purpose**: Delete an installed Ollama model
**How it works**: Runs `ollama rm {model_name}` command
**Returns**: Success status

### Endpoint: `GET /api/models/{model_name}/status`
**Purpose**: Check if a specific model is installed
**Returns**: Model name, install status, metadata

### Endpoint: `POST /api/models/download-recommended`
**Purpose**: Download recommended models (Qwen 2.5 7B + Aya 8B)
**How it works**:
1. Downloads both recommended models
2. Returns status for each download
**Returns**: Overall status, individual results, download counts

## Supported Models

### Recommended Models (Best for Multilingual)
- **qwen2.5:7b**: Best balance - multilingual & translation (4.7 GB)
- **aya:8b**: Translation specialist (4.7 GB)

### Qwen Models (Multilingual & Translation)
- `qwen2.5:3b`: Fast multilingual (2.0 GB)
- `qwen2.5:7b`: Recommended (4.7 GB)
- `qwen2.5:14b`: High quality (8.5 GB)
- `qwen2.5:72b`: Best quality (40.0 GB)

### Aya Models (Translation Specialist)
- `aya:8b`: Translation expert (4.7 GB)
- `aya:35b`: Best translation (20.0 GB)

### Llama Models (English Focused)
- `llama2:13b`: Good for English (7.3 GB)
- `llama3.2:3b`: Fast, lightweight (2.0 GB)
- `llama3.2:13b`: Better quality (7.3 GB)
- `llama3.1:8b`: Improved multilingual (4.7 GB)

### Mistral Models (Fast Multilingual)
- `mistral:7b`: Fast multilingual (4.1 GB)
- `mixtral:8x7b`: High quality (26.0 GB)

## Dependencies
- `asyncio`: Async subprocess execution
- `subprocess`: Running Ollama commands (via asyncio)
- `fastapi`: API framework
- `httpx`: Optional HTTP client (not used here, but available)

## Usage

### Download a Model
```bash
curl -X POST http://localhost:8000/api/models/download/qwen2.5:7b
```

### List Available Models
```bash
curl http://localhost:8000/api/models/available
```

### List Installed Models
```bash
curl http://localhost:8000/api/models/list
```

### Download Recommended Models
```bash
curl -X POST http://localhost:8000/api/models/download-recommended
```

## Integration

This module is integrated into:
- `src/api/server.py`: Router registered with FastAPI app
- `src/api/static/index.html`: Model Management modal UI
- `src/api/static/js/app.js`: JavaScript handlers for model management

## Error Handling

- **Ollama not found**: Returns error message with installation instructions
- **Invalid model name**: Returns 400 error with list of available models
- **Download failure**: Returns 500 error with error details
- **Already installed**: Returns success status indicating model already exists

## Future Enhancements

- Model download progress streaming (WebSocket)
- Model size verification after download
- Model performance benchmarking
- Automatic model updates
- Model caching and verification

---

**Last Updated**: 2025-11-03  
**Created**: 2025-11-03

