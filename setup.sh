#!/bin/bash
# Zema AI Setup Script for Ubuntu 22.04
# BOSGAME P3 Lite Mini PC Setup

set -e

echo "=========================================="
echo "Zema AI Setup Script"
echo "=========================================="
echo ""

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11+
echo "Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    v4l-utils \
    v4l2loopback-utils \
    build-essential \
    git

# Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Create virtual environment
echo "Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "Creating data directories..."
mkdir -p data/{db,logs,models,backups,audio,images,knowledge,exports,config}

# Create .gitkeep files
touch data/models/.gitkeep

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Copy .env.example to .env and configure"
echo "3. Download models: bash scripts/download_models.sh"
echo "4. Run hardware verification: python scripts/verify_hardware.py"
echo "5. Start Zema: python src/main.py"
echo ""

