# verify_ollama.py Documentation

## File Location
`scripts/verify_ollama.py`

## Purpose
Ollama health check script. Verifies Ollama service is running, checks model availability, tests inference performance, and measures response latency for Zema AI requirements.

## Why It Was Created
Ollama is critical for local LLM inference. This script:
- Checks if Ollama service is running
- Verifies Llama 3.2 model is downloaded
- Tests inference speed (tokens/second)
- Measures response latency
- Checks GPU/CPU usage
- Verifies model loads without errors

## How It Works

### Function: `check_ollama_service() -> bool`
**Purpose**: Check if Ollama service is running
**How it works**:
1. Makes HTTP GET request to `http://localhost:11434/api/tags`
2. Verifies response is successful
3. Checks service is accessible

**Returns**: True if Ollama is accessible

### Function: `list_available_models() -> List[str]`
**Purpose**: List all available Ollama models
**How it works**:
1. Calls Ollama API: `GET /api/tags`
2. Extracts model names from response
3. Returns list of available models

**Returns**: List of model names

### Function: `verify_model(model_name: str) -> Tuple[bool, Optional[str]]`
**Purpose**: Verify specific model is available
**How it works**:
1. Checks if model is in available models list
2. Verifies model can be loaded
3. Returns success status

**Returns**: Tuple of (success, error_message)

### Function: `test_inference_performance(model_name: str, prompt: str) -> Dict[str, Any]`
**Purpose**: Test inference performance
**How it works**:
1. Sends prompt to Ollama API: `POST /api/generate`
2. Measures time to first token
3. Measures tokens per second
4. Monitors memory usage (if psutil available)
5. Calculates performance metrics

**Returns**: Dictionary with performance metrics

### Performance Targets
For Raspberry Pi 5 / BOSGAME P3 Lite:
- **Time to first token**: < 1000ms
- **Tokens per second**: > 10
- **Memory usage**: < 6GB
- **No model loading errors**

### Main Execution Flow
1. **Step 1**: Check Ollama service
   - Verifies service is running
   - Checks API accessibility
2. **Step 2**: List available models
   - Shows all downloaded models
   - Displays model information
3. **Step 3**: Verify model
   - Checks if specified model exists
   - Verifies model can be loaded
4. **Step 4**: Test inference performance
   - Sends test prompt
   - Measures latency
   - Calculates tokens/second
   - Monitors memory usage

## Dependencies
- `httpx`: HTTP client for Ollama API
- `psutil`: Resource monitoring (optional)
- `time`: Time measurement
- `json`: JSON parsing

## Usage

### Basic Usage
```bash
python scripts/verify_ollama.py
```

### Expected Output
```
============================================================
Step 1: Checking Ollama service...
[OK] Ollama service is running

Step 2: Listing available models...
[OK] Found 2 models:
  - llama2:13b
  - llama3.2:3b

Step 3: Verifying model: llama2:13b
[OK] Model is available

Step 4: Testing inference performance...
[OK] Time to first token: 850ms
[OK] Tokens per second: 12.5
[OK] Memory usage: 4.2GB
[OK] Performance targets met

VERIFICATION SUMMARY
[OK] All Ollama tests passed
```

### Exit Codes
- `0`: All tests passed
- `1`: Ollama service not running
- `2`: Model not found
- `3`: Inference failed
- `4`: Performance below target

## Configuration
Script uses settings from `src/config/settings.py`:
- `ollama_url`: Ollama server URL (default: `http://localhost:11434`)
- `ollama_model_name`: Model to verify (default: `llama2:13b`)
- `ollama_timeout`: Request timeout (default: 60 seconds)
- `ollama_time_to_first_token_max_ms`: Max TTF threshold (default: 1000ms)
- `ollama_tokens_per_second_min`: Min tokens/sec threshold (default: 10)
- `ollama_memory_usage_max_gb`: Max memory threshold (default: 6GB)

## Error Handling

### Docker/Windows Environments
Script gracefully handles:
- Missing httpx (warns but continues)
- Missing psutil (skips memory monitoring)
- Ollama not running (provides troubleshooting)
- Model not found (suggests downloading)

### Error Messages
- Clear warnings for missing dependencies
- Troubleshooting suggestions
- Performance threshold violations

## Integration
- **Phase 0.5**: Hardware Verification (HARDWARE-003)
- **Before Development**: Run before starting Phase 1
- **Setup Scripts**: Can be called from setup automation
- **CI/CD**: Can be integrated into build pipeline

## Benefits
1. **Service Verification**: Ensures Ollama is running
2. **Model Verification**: Confirms model is available
3. **Performance Testing**: Measures inference speed
4. **Latency Measurement**: Checks time to first token
5. **Memory Monitoring**: Tracks resource usage
6. **Clear Output**: ASCII-compatible output (no emojis)

## Testing
```bash
# Run verification
python scripts/verify_ollama.py

# Check exit code
echo $?  # Should be 0 if successful

# Test Ollama manually
curl http://localhost:11434/api/tags
```

## Troubleshooting

### Ollama Service Not Running
1. Start Ollama: `ollama serve` (or start as service)
2. Check service status: `systemctl status ollama` (Linux)
3. Verify port 11434 is accessible: `curl http://localhost:11434/api/tags`
4. Check firewall settings

### Model Not Found
1. Download model: `ollama pull llama2:13b`
2. List models: `ollama list`
3. Verify model name is correct
4. Check model availability: `curl http://localhost:11434/api/tags`

### Performance Below Target
1. Check system resources: `htop` or `top`
2. Verify model size matches hardware
3. Consider using smaller model (e.g., llama3.2:3b)
4. Check for background processes consuming resources

### Inference Failed
1. Check Ollama logs: `journalctl -u ollama` (Linux)
2. Verify model is fully downloaded
3. Check system memory availability
4. Test with simple prompt manually

## Phase 0.5 Context
This script is part of **HARDWARE-003: Ollama Health Check** in Phase 0.5 Hardware Verification. It must pass before proceeding to Phase 1 Voice Interaction.

