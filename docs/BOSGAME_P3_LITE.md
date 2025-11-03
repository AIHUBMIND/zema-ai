# BOSGAME P3 Lite Configuration

## Hardware Specifications

- **Model**: BOSGAME P3 Lite Mini PC
- **OS**: Ubuntu 22.04 LTS
- **Architecture**: x86_64
- **Use Case**: Privacy-first voice assistant deployment

## System Requirements

### Minimum Requirements
- Python 3.11+
- 4GB RAM (8GB recommended)
- 32GB storage (64GB recommended)
- USB microphone/speaker or built-in audio
- USB camera (optional, for vision features)

### Recommended Setup
- 8GB+ RAM for smooth LLM inference
- SSD storage for faster model loading
- External USB microphone for better wake word detection
- USB webcam for vision processing

## Ubuntu 22.04 Configuration

### Initial System Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install essential tools
sudo apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    python3.11 \
    python3.11-venv \
    python3.11-dev
```

### Audio Configuration

```bash
# Install audio dependencies
sudo apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    pulseaudio \
    pavucontrol

# Verify audio devices
arecord -l  # List recording devices
aplay -l    # List playback devices
```

### Camera Configuration (Optional)

```bash
# Install camera dependencies
sudo apt-get install -y \
    v4l-utils \
    libv4l-dev

# Test camera
v4l2-ctl --list-devices
```

### Network Configuration

```bash
# Configure static IP (if needed)
sudo nano /etc/netplan/01-netcfg.yaml

# Example configuration:
# network:
#   version: 2
#   ethernets:
#     eth0:
#       dhcp4: false
#       addresses: [192.168.1.100/24]
#       gateway4: 192.168.1.1
#       nameservers:
#         addresses: [8.8.8.8, 8.8.4.4]

# Apply changes
sudo netplan apply
```

## Ollama Setup

### Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull Llama 2 13B model
ollama pull llama2:13b

# Verify installation
ollama list
```

### Ollama Configuration

```bash
# Configure Ollama to run on system startup
sudo systemctl enable ollama

# Set environment variables (optional)
echo 'export OLLAMA_HOST=0.0.0.0:11434' >> ~/.bashrc
source ~/.bashrc
```

## Zema AI Installation

### Clone and Setup

```bash
# Navigate to installation directory
cd ~
git clone <repository-url> zema-ai
cd zema-ai

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Service Configuration

Create a systemd service for auto-start:

```bash
sudo nano /etc/systemd/system/zema-ai.service
```

Add the following content:

```ini
[Unit]
Description=Zema AI Personal Assistant
After=network.target ollama.service

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/zema-ai
Environment="PATH=/home/your-username/zema-ai/venv/bin"
ExecStart=/home/your-username/zema-ai/venv/bin/python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable zema-ai
sudo systemctl start zema-ai

# Check status
sudo systemctl status zema-ai
```

## Performance Optimization

### CPU Governor (for better performance)

```bash
# Install CPU utilities
sudo apt-get install -y cpufrequtils

# Set to performance mode
sudo cpufreq-set -g performance

# Make permanent
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
```

### Memory Management

```bash
# Check available memory
free -h

# Set swap if needed (if RAM < 8GB)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## Monitoring

### Check System Resources

```bash
# CPU usage
htop

# Memory usage
free -h

# Disk usage
df -h

# GPU usage (if applicable)
nvidia-smi
```

### Log Monitoring

```bash
# View Zema AI logs
tail -f data/logs/zema.log

# View system logs
journalctl -u zema-ai -f
```

## Troubleshooting

### Audio Issues

```bash
# Check audio devices
arecord -l
aplay -l

# Test microphone
arecord -d 5 test.wav
aplay test.wav

# Restart audio service
sudo systemctl restart pulseaudio
```

### Network Issues

```bash
# Check network connectivity
ping -c 4 8.8.8.8

# Check Ollama connection
curl http://localhost:11434/api/tags
```

### Service Issues

```bash
# Check service status
sudo systemctl status zema-ai

# View service logs
sudo journalctl -u zema-ai -n 50

# Restart service
sudo systemctl restart zema-ai
```

## Security Considerations

### Firewall Configuration

```bash
# Install UFW
sudo apt-get install -y ufw

# Allow SSH (if remote access)
sudo ufw allow 22/tcp

# Allow Zema AI API (if exposing)
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

### User Permissions

```bash
# Create dedicated user for Zema AI
sudo adduser zema --disabled-password
sudo usermod -aG audio,video zema

# Set ownership
sudo chown -R zema:zema /home/your-username/zema-ai
```

## Maintenance

### Regular Updates

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Python packages
cd ~/zema-ai
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Backup Configuration

```bash
# Backup configuration files
tar -czf zema-backup-$(date +%Y%m%d).tar.gz \
    data/config/ \
    data/db/ \
    .env
```

