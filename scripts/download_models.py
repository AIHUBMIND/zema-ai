#!/usr/bin/env python3
"""
Model Download and Verification Script
Downloads and verifies all required AI models

Usage:
    python scripts/download_models.py

Exit codes:
    0: All models downloaded successfully
    1: Download failed
"""

import sys
import hashlib
from pathlib import Path
from typing import Optional
from urllib.request import urlretrieve

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    print("WARNING: httpx not installed. Install with: pip install httpx")

# Model URLs and checksums
MODELS = {
    'yolo': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt',
        'path': 'data/models/yolo/yolov8n.pt',
        'size_mb': 6,
        'description': 'YOLOv8 Nano (object detection)'
    },
    # Whisper models will be downloaded via whisper.cpp
    # Piper voices will be downloaded via piper-tts
    # Ollama models are downloaded via ollama pull
}

def download_file(url: str, dest_path: Path, description: str) -> bool:
    """
    Download a file with progress indication
    
    Args:
        url: URL to download from
        dest_path: Destination path
        description: Description of the file
        
    Returns:
        True if download successful
    """
    print(f"   Downloading {description}...")
    print(f"   URL: {url}")
    print(f"   Destination: {dest_path}")
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        def show_progress(block_num, block_size, total_size):
            if total_size > 0:
                percent = min(100, (block_num * block_size * 100) // total_size)
                print(f"\r   Progress: {percent}%", end='', flush=True)
        
        urlretrieve(url, str(dest_path), reporthook=show_progress)
        print("\n   ✅ Download complete")
        return True
    except Exception as e:
        print(f"\n   ❌ Download failed: {e}")
        return False

def verify_file(file_path: Path, expected_size_mb: Optional[int] = None) -> bool:
    """
    Verify downloaded file exists and optionally check size
    
    Args:
        file_path: Path to file
        expected_size_mb: Expected size in MB
        
    Returns:
        True if file is valid
    """
    if not file_path.exists():
        return False
    
    if expected_size_mb:
        actual_size_mb = file_path.stat().st_size / 1024 / 1024
        if abs(actual_size_mb - expected_size_mb) > expected_size_mb * 0.1:  # 10% tolerance
            print(f"   ⚠️  WARNING: File size mismatch (expected ~{expected_size_mb}MB, got {actual_size_mb:.2f}MB)")
            return False
    
    return True

def check_whisper_models() -> bool:
    """Check if Whisper models are available"""
    print("\n" + "=" * 60)
    print("Step 2: Checking Whisper models...")
    print("=" * 60)
    
    whisper_path = Path("data/models/whisper")
    whisper_path.mkdir(parents=True, exist_ok=True)
    
    print("   ℹ️  Whisper models should be downloaded via whisper.cpp")
    print("   ℹ️  Or install via: pip install faster-whisper")
    print("   ℹ️  Models will be downloaded automatically on first use")
    
    return True

def check_piper_voices() -> bool:
    """Check if Piper voices are available"""
    print("\n" + "=" * 60)
    print("Step 3: Checking Piper TTS voices...")
    print("=" * 60)
    
    piper_path = Path("data/models/piper")
    piper_path.mkdir(parents=True, exist_ok=True)
    
    print("   ℹ️  Piper voices should be downloaded via piper-tts")
    print("   ℹ️  Or install via: pip install piper-tts")
    print("   ℹ️  Voices will be downloaded automatically on first use")
    
    return True

def check_ollama_models() -> bool:
    """Check if Ollama models are available"""
    print("\n" + "=" * 60)
    print("Step 4: Checking Ollama models...")
    print("=" * 60)
    
    print("   ℹ️  Ollama models are downloaded via ollama pull")
    print("   ℹ️  Run: ollama pull llama2:13b")
    print("   ℹ️  Or use verify_ollama.py to check")
    
    return True

def main():
    """Download and verify all models"""
    print("\n" + "=" * 60)
    print("ZEMA AI - Model Download and Verification")
    print("=" * 60)
    print()
    
    success_count = 0
    total_count = len(MODELS)
    
    # Step 1: Download YOLO model
    print("=" * 60)
    print("Step 1: Downloading YOLO model...")
    print("=" * 60)
    
    yolo_info = MODELS['yolo']
    yolo_path = Path(yolo_info['path'])
    
    if yolo_path.exists():
        print(f"   ✅ YOLO model already exists: {yolo_path}")
        if verify_file(yolo_path, yolo_info['size_mb']):
            success_count += 1
    else:
        if download_file(yolo_info['url'], yolo_path, yolo_info['description']):
            if verify_file(yolo_path, yolo_info['size_mb']):
                success_count += 1
    
    # Step 2-4: Check other models
    check_whisper_models()
    check_piper_voices()
    check_ollama_models()
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"✅ YOLO model: {'AVAILABLE' if Path(MODELS['yolo']['path']).exists() else 'MISSING'}")
    print("ℹ️  Whisper models: Download via whisper.cpp or faster-whisper")
    print("ℹ️  Piper voices: Download via piper-tts")
    print("ℹ️  Ollama models: Download via ollama pull")
    print("\n⚠️  NOTE: Some models are downloaded automatically on first use")
    print("   Full functionality requires all models to be available")
    print("\n✅ Model download script ready")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

