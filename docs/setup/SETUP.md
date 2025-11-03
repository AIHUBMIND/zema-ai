# Platform-Specific Installation Notes

## Windows Development Setup

Some packages require compilation tools that may not be available on Windows. The following packages have been installed:

✅ **Installed (pure Python packages):**
- fastapi, uvicorn, pydantic, pydantic-settings
- httpx, sqlalchemy, aiosqlite, aiofiles
- python-multipart, pyyaml, python-dotenv, structlog
- pytest, pytest-asyncio

⚠️ **Install on Linux Target (Ubuntu 22.04):**
These packages require compilation and should be installed on the target Linux system:

```bash
# On Ubuntu 22.04, install system dependencies first:
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    portaudio19-dev \
    libasound2-dev \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev

# Then install Python packages:
pip install pyaudio>=0.2.14
pip install opencv-python-headless>=4.8.0
pip install faster-whisper>=0.10.0
pip install numpy>=1.24.0,<2.3.0
```

## Linux Target Setup (Ubuntu 22.04)

For the BOSGAME P3 Lite mini PC running Ubuntu 22.04:

```bash
# 1. Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3.11 python3.11-venv python3.11-dev \
    portaudio19-dev libasound2-dev \
    ffmpeg libavcodec-dev libavformat-dev \
    libavutil-dev libswscale-dev libswresample-dev \
    libavfilter-dev

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install all requirements
pip install --upgrade pip
pip install -r requirements.txt
```

## Verification

Run the test script to verify setup:
```bash
python scripts/test_setup.py
```

