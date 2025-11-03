# settings.py Documentation

## File Location
`src/config/settings.py`

## Purpose
Application configuration settings using Pydantic. Provides type-safe access to all configuration values with validation and environment variable support.

## Why It Was Created
Pydantic provides:
- Type validation (ensures correct types)
- Environment variable support (12-factor app pattern)
- Default values (sensible defaults)
- Documentation (field descriptions)
- Validation (validates values before use)

## How It Works

### Class: `Settings(BaseSettings)`
**Purpose**: Main settings class
**Inherits from**: `pydantic_settings.BaseSettings`

**Configuration Sources** (priority order):
1. Environment variables (highest priority)
2. `.env` file
3. Default values (lowest priority)

### Configuration Sections

#### Application Settings
```python
app_name: str = "Zema AI Personal Assistant"
app_version: str = "0.1.0"
debug: bool = False
```

#### API Settings
```python
api_host: str = "127.0.0.1"
api_port: int = 8000
```

#### LLM Settings (Ollama)
```python
ollama_base_url: str = "http://localhost:11434"
ollama_model: str = "llama2:13b"
```

#### Voice Settings
```python
wake_word_enabled: bool = True
sample_rate: int = 16000
channels: int = 1
chunk_size: int = 1024
```

#### Vision Settings
```python
camera_enabled: bool = False
camera_index: int = 0
```

#### Database Settings
```python
database_url: str = "sqlite+aiosqlite:///./data/db/zema.db"
```

#### Logging Settings
```python
log_level: str = "INFO"
log_file: str = "./data/logs/zema.log"
```

#### Path Settings
```python
data_dir: str = "./data"
models_dir: str = "./data/models"
```

### Configuration Model
```python
model_config = SettingsConfigDict(
    env_file=".env",              # Load from .env file
    env_file_encoding="utf-8",    # UTF-8 encoding
    case_sensitive=False,          # Environment vars case-insensitive
    extra="ignore",                # Ignore extra fields
)
```

### Global Instance
```python
settings = Settings()
```
**Purpose**: Single global instance used throughout the application

## Usage

### Accessing Settings
```python
from src.config.settings import settings

# Access values
print(settings.app_name)
print(settings.api_port)
print(settings.ollama_model)
```

### Environment Variables
Set environment variables to override defaults:
```bash
# Linux/Mac
export OLLAMA_MODEL=llama3:8b
export API_PORT=9000

# Windows
set OLLAMA_MODEL=llama3:8b
set API_PORT=9000
```

### .env File
Create `.env` file in project root:
```env
OLLAMA_MODEL=llama3:8b
API_PORT=9000
DEBUG=true
```

### Type Safety
Pydantic validates types:
```python
# ✅ Valid
settings.api_port = 8000

# ❌ Invalid - raises ValidationError
settings.api_port = "8000"  # String instead of int
```

## Field Descriptions
Each field has a description:
```python
app_name: str = Field(
    default="Zema AI Personal Assistant",
    description="Application name"
)
```

These descriptions:
- Appear in generated documentation
- Help with IDE autocomplete
- Provide context for developers

## Validation
Pydantic automatically validates:
- **Type validation**: Ensures correct types
- **Required fields**: Fields with defaults are optional
- **Custom validators**: Can add custom validation logic

## Dependencies
- `pydantic_settings`: Settings management
- `pydantic`: Data validation

## Integration
Used throughout the application:
- `src/main.py`: Gets log level
- `src/core/orchestrator.py`: Gets all settings
- `src/voice/audio_io.py`: Gets audio settings
- `src/api/server.py`: Gets API settings
- And more...

## Benefits
1. **Type safety**: Catches type errors early
2. **Environment-aware**: Easy configuration for different environments
3. **Documentation**: Field descriptions provide context
4. **Validation**: Ensures valid configuration values
5. **Single source of truth**: All config in one place

## Related Files
- `.env.example`: Example environment variables
- `.env`: Actual environment variables (not in Git)
- `src/config/config_manager.py`: Runtime configuration updates

