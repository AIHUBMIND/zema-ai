#!/bin/bash
# Download all required models for Zema

set -e

echo "=========================================="
echo "Zema AI - Model Download Script"
echo "=========================================="
echo ""

# Create models directory
mkdir -p data/models/{whisper,piper,yolo}

# Download Whisper model (base)
echo "📥 Downloading Whisper base model..."
echo "Note: Whisper models are downloaded automatically by faster-whisper on first use"
echo "Model will be cached in: ~/.cache/huggingface/"

# Download Piper TTS voices
echo "📥 Downloading Piper TTS voices..."
echo "Note: Download Piper voices from: https://github.com/rhasspy/piper/releases"
echo "Place ONNX models in: data/models/piper/"

# Download YOLO model
echo "📥 Downloading YOLO model..."
wget -O data/models/yolo/yolov8n.pt \
  https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt || \
  echo "⚠️  YOLO model download failed. Will be downloaded automatically by ultralytics on first use."

# Verify Ollama models
echo "📥 Verifying Ollama models..."
echo "Run: ollama pull llama2:13b"
echo "Or your preferred model: ollama pull llama3.2:3b"

echo ""
echo "=========================================="
echo "Model download complete!"
echo "=========================================="
echo ""
echo "Manual steps:"
echo "1. Pull Ollama model: ollama pull llama2:13b"
echo "2. Download Piper voices from: https://github.com/rhasspy/piper/releases"
echo "3. Whisper models download automatically on first use"
echo ""

