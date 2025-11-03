# download_models.py Documentation

## File Location
`scripts/download_models.py`

## Purpose
Model download and verification script. Downloads and verifies all required AI models for Zema AI, including YOLO, Whisper, and Piper models.

## Why It Was Created
AI models must be downloaded before use. This script:
- Downloads YOLOv8 model for object detection
- Verifies model integrity
- Creates necessary model directories
- Provides progress indication
- Handles download errors gracefully

## How It Works

### Function: `download_file(url: str, dest_path: Path, description: str) -> bool`
**Purpose**: Download a file with progress indication
**How it works**:
1. Creates destination directory if needed
2. Downloads file from URL using `urllib.request.urlretrieve`
3. Shows progress indication
4. Verifies file size
5. Returns success status

**Returns**: True if download successful

### Function: `verify_file_integrity(file_path: Path, expected_size_mb: Optional[int] = None) -> bool`
**Purpose**: Verify downloaded file integrity
**How it works**:
1. Checks if file exists
2. Verifies file size matches expected size
3. Calculates SHA256 checksum (if provided)
4. Returns verification status

**Returns**: True if file is valid

### Model Definitions
Currently downloads:
- **YOLOv8 Nano**: Object detection model
  - URL: GitHub releases
  - Path: `data/models/yolo/yolov8n.pt`
  - Size: ~6MB

**Note**: Whisper and Piper models are downloaded via their respective tools:
- Whisper: Via `whisper.cpp` or `faster-whisper`
- Piper: Via `piper-tts` command-line tool
- Ollama: Via `ollama pull` command

### Main Execution Flow
1. **Create directories**: Creates `data/models/` structure
2. **Download YOLO model**: Downloads YOLOv8 Nano
3. **Verify integrity**: Checks file size and integrity
4. **Report status**: Shows download results

## Dependencies
- `urllib.request`: File downloading
- `pathlib`: File path handling
- `hashlib`: File integrity verification (optional)
- `httpx`: HTTP client (optional, for future enhancements)

## Usage

### Basic Usage
```bash
python scripts/download_models.py
```

### Expected Output
```
============================================================
ZEMA AI - Model Download and Verification
============================================================

Creating model directories...
[OK] Directory created: data/models/yolo

Downloading YOLOv8 Nano...
[OK] Downloading: 100% (6.2 MB)
[OK] File saved: data/models/yolo/yolov8n.pt

Verifying file integrity...
[OK] File size verified: 6.2 MB
[OK] File integrity check passed

VERIFICATION SUMMARY
[OK] All models downloaded successfully
```

### Exit Codes
- `0`: All models downloaded successfully
- `1`: Download failed

## Error Handling

### Network Errors
- Connection timeout: Retries with clear error message
- Download interrupted: Shows partial download status
- Invalid URL: Reports URL error

### File System Errors
- Permission denied: Suggests running with appropriate permissions
- Disk full: Reports disk space issue
- Path errors: Creates directories if needed

## Integration
- **Phase 0.5**: Hardware Verification (HARDWARE-004)
- **Setup Scripts**: Can be called from setup automation
- **CI/CD**: Can be integrated into build pipeline
- **Manual Download**: Can be run independently

## Output Files
- `data/models/yolo/yolov8n.pt`: YOLOv8 Nano model file
  - Used for object detection
  - ~6MB in size

## Directory Structure
```
data/
  models/
    yolo/
      yolov8n.pt
    whisper/
      (downloaded by whisper.cpp)
    piper/
      (downloaded by piper-tts)
```

## Configuration
Script uses settings from `src/config/settings.py`:
- `models_base_path`: Base path for models (default: `data/models`)
- `yolo_model_path`: YOLO model path (default: `data/models/yolo`)

## Benefits
1. **Automated Download**: Downloads models automatically
2. **Integrity Verification**: Verifies downloaded files
3. **Progress Indication**: Shows download progress
4. **Error Handling**: Handles download errors gracefully
5. **Clear Output**: ASCII-compatible output (no emojis)

## Testing
```bash
# Run download
python scripts/download_models.py

# Check exit code
echo $?  # Should be 0 if successful

# Verify model file
ls -lh data/models/yolo/yolov8n.pt

# Check file size
du -h data/models/yolo/yolov8n.pt
```

## Troubleshooting

### Download Failed
1. Check internet connection
2. Verify URL is accessible: `curl -I <url>`
3. Check disk space: `df -h`
4. Try manual download: `wget <url> -O <dest>`

### File Integrity Failed
1. Re-download model
2. Check disk space
3. Verify file permissions
4. Check for disk errors

### Permission Denied
1. Check directory permissions: `ls -l data/models/`
2. Create directory manually: `mkdir -p data/models/yolo`
3. Run with appropriate permissions

## Future Enhancements
- Support for Whisper model download
- Support for Piper voice download
- Parallel downloads for multiple models
- Resume interrupted downloads
- Checksum verification

## Phase 0.5 Context
This script is part of **HARDWARE-004: Model Download Verification** in Phase 0.5 Hardware Verification. Models must be downloaded before proceeding to Phase 1 Voice Interaction.

