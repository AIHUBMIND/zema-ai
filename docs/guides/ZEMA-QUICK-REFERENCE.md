# ZEMA Quick Reference Card
## Essential Commands & Settings

**Version:** 1.0 | **Platform:** Raspberry Pi 5 + Insta360 Link 2 | **Date:** Nov 2025

---

## 🚀 System Control

```bash
# Start Zema
sudo systemctl start zema

# Stop Zema
sudo systemctl stop zema

# Restart Zema
sudo systemctl restart zema

# Check status
sudo systemctl status zema

# Enable auto-start on boot
sudo systemctl enable zema

# Disable auto-start
sudo systemctl disable zema

# Run manually (foreground, see all output)
cd ~/zema-ai
source venv/bin/activate
python src/main.py
```

---

## 📋 Monitoring & Logs

```bash
# View live logs
tail -f data/logs/zema.log

# View errors only
tail -f data/logs/zema.log | grep ERROR

# View last 100 lines
tail -100 data/logs/zema.log

# View systemd logs
journalctl -u zema -f

# View logs since last boot
journalctl -u zema -b

# Search logs
grep "camera" data/logs/zema.log
```

---

## 🎛️ Configuration

```bash
# Edit settings
nano .env

# Common settings to change:
PRIVACY_MODE=local           # local, hybrid, cloud
WAKEWORD_KEYWORDS=hey zema   # Change wake word
WAKEWORD_SENSITIVITY=0.5     # 0.0-1.0
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
CAMERA_TRACKING=true        # Enable/disable AI tracking
CAMERA_GESTURES=true        # Enable/disable gestures
LLM_MODEL=llama3.2:3b       # AI model
STT_MODEL=base              # Whisper model

# After editing, restart:
sudo systemctl restart zema

# View current settings (while Zema running):
http://zema.local:8000      # Open dashboard
```

---

## 🔧 Hardware Testing

```bash
# Full hardware check
python scripts/verify_hardware.py

# Test camera only
v4l2-ctl --list-devices
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg

# Test audio
arecord -l                  # List devices
arecord -D hw:1,0 -d 5 test.wav  # Record 5 seconds
aplay test.wav              # Play back

# Test Ollama
ollama list                 # List models
echo "Hello" | ollama run llama3.2:3b

# Full system benchmark
python scripts/benchmark.py

# Check temperature
vcgencmd measure_temp

# Check CPU/memory
htop
```

---

## 🎥 Camera Control

```bash
# Check camera detected
v4l2-ctl --list-devices

# View camera settings
v4l2-ctl -d /dev/video0 --all

# Set to 1080p @ 30fps
v4l2-ctl -d /dev/video0 \
  --set-fmt-video=width=1920,height=1080,pixelformat=MJPG
v4l2-ctl -d /dev/video0 --set-parm=30

# Enable autofocus
v4l2-ctl -d /dev/video0 --set-ctrl=focus_automatic_continuous=1

# PTZ controls (pan/tilt)
v4l2-ctl -d /dev/video0 --set-ctrl=pan_absolute=0    # Center
v4l2-ctl -d /dev/video0 --set-ctrl=tilt_absolute=0   # Center

# Capture test frame
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg
```

---

## 🔊 Audio Control

```bash
# List audio devices
arecord -l                  # Input devices
aplay -l                    # Output devices

# Set camera mic as default
cat > ~/.asoundrc << 'EOF'
pcm.!default {
    type hw
    card 1
    device 0
}
EOF

# Volume control
alsamixer                   # Press F6 to select device

# Test microphone
arecord -D hw:1,0 -f cd -d 5 test.wav
aplay test.wav
```

---

## 🤖 AI Models

```bash
# Ollama
ollama list                 # List models
ollama pull llama3.2:3b     # Download model
ollama rm llama3.2:3b       # Remove model
systemctl status ollama     # Check Ollama service

# Download all models
bash scripts/download_models.sh

# Check models exist
ls -lh data/models/

# Model sizes:
# - Llama 3.2-3B: ~2GB
# - Whisper base: ~150MB
# - Piper voices: ~30MB each
# - YOLOv8n: ~6MB
```

---

## 🌐 Web Dashboard

```bash
# Access dashboard
http://zema.local:8000      # By hostname
http://192.168.1.XXX:8000   # By IP address

# Change port (if 8000 in use)
# Edit .env:
DASHBOARD_PORT=8080

# Disable dashboard
ENABLE_DASHBOARD=false

# Dashboard features:
# - System status (CPU, memory, temperature)
# - Settings (all configuration)
# - Users (family members)
# - History (conversations)
# - Privacy (data management)
```

---

## 🗣️ Voice Commands

```bash
# Wake Zema
"Hey Zema"

# Configuration commands
"Enable privacy mode"
"Disable camera tracking"
"Switch to Amharic"
"Change voice to female"
"Show my settings"

# Voice interaction
"What time is it?"
"What do you see?"
"Remind me to..."
"Take a note..."
"What's on my calendar?"
```

---

## 🐛 Troubleshooting

```bash
# Quick diagnostics
python scripts/verify_hardware.py
python scripts/verify_audio.py
python scripts/verify_ollama.py

# Check what's wrong
sudo systemctl status zema  # Service status
tail -100 data/logs/zema.log | grep ERROR
dmesg | tail -20           # Kernel messages

# Common fixes
sudo systemctl restart zema      # Restart service
sudo systemctl restart ollama    # Restart Ollama
sudo reboot                      # Reboot Pi

# Camera not detected
lsusb | grep Insta360
# Replug camera, try different USB port

# Ollama not responding
sudo systemctl restart ollama

# Slow performance
vcgencmd measure_temp       # Check temperature
htop                        # Check CPU/memory

# Disk full
df -h                       # Check space
bash scripts/cleanup.sh     # Clean old files
```

---

## 💾 Backup & Maintenance

```bash
# Backup
bash scripts/backup.sh

# Restore
# (Copy backup to data/ directory)

# Clean old files
bash scripts/cleanup.sh

# Update system
sudo apt update && sudo apt upgrade -y

# Update Zema code
cd ~/zema-ai
git pull
source venv/bin/activate
pip install --upgrade -r requirements.txt
sudo systemctl restart zema

# Check disk usage
du -sh data/*
df -h
```

---

## 📊 Performance Monitoring

```bash
# Real-time monitoring
watch -n 2 '
echo "CPU:"; top -bn1 | grep "Cpu(s)"
echo "Memory:"; free -h | grep Mem
echo "Temp:"; vcgencmd measure_temp
echo "Zema:"; ps aux | grep python | grep -v grep
'

# Performance targets (Pi 5)
# - Wake word detection: <500ms
# - Gesture detection: <300ms
# - STT: <2s
# - LLM response: 3-6s
# - TTS: <1s
# - Total: 5-10s end-to-end

# Check Ollama speed
time echo "Count to 5" | ollama run llama3.2:3b
# Should be 10-15 tokens/second on Pi 5
```

---

## 🔐 Privacy & Data

```bash
# View stored data
ls -lh data/db/              # Databases
ls -lh data/audio/           # Audio files
ls -lh data/images/          # Images

# Data locations
data/db/zema.db             # Main database
data/logs/                  # Logs
data/audio/                 # Voice recordings (if enabled)
data/images/                # Camera captures
data/models/                # AI models

# Clear data (CAREFUL!)
rm -rf data/db/*.db         # Clear all databases
rm -rf data/audio/*         # Clear audio
rm -rf data/images/*        # Clear images
# Restart Zema to recreate databases

# Privacy modes
PRIVACY_MODE=local          # All local, no cloud
PRIVACY_MODE=hybrid         # Simple local, complex cloud
PRIVACY_MODE=cloud          # Use cloud APIs

# Data retention
DATA_RETENTION_DAYS=30      # Auto-delete after 30 days
```

---

## 🚨 Emergency Procedures

```bash
# Zema won't start
sudo systemctl status zema
journalctl -u zema -n 50
# Fix errors, then restart

# System frozen
# Hard reboot (power cycle)

# Camera not working
lsusb | grep Insta360
# If not found: replug camera
# If found: check logs

# No audio
arecord -l
alsamixer
# Check mic not muted, volume >70%

# Ollama crash
sudo systemctl restart ollama
ollama list

# Out of disk space
df -h
bash scripts/cleanup.sh
# Or move data to USB drive

# Overheating
vcgencmd measure_temp
# If >80°C: Add cooling, reduce workload
```

---

## 📁 File Locations

```bash
# Configuration
~/zema-ai/.env                     # Main config
~/zema-ai/config/logging.yaml     # Logging config

# Code
~/zema-ai/src/                    # Source code

# Data
~/zema-ai/data/db/                # Databases
~/zema-ai/data/logs/              # Logs
~/zema-ai/data/models/            # AI models

# Scripts
~/zema-ai/scripts/                # Utility scripts

# Service
/etc/systemd/system/zema.service  # Systemd service
```

---

## 🔢 Default Ports

```
8000 - Web dashboard
11434 - Ollama API
```

---

## 📞 Support Checklist

Before asking for help, collect:
```bash
# System info
uname -a
python --version
df -h

# Zema status
sudo systemctl status zema
tail -50 data/logs/zema.log

# Hardware status
python scripts/verify_hardware.py

# Save debug package
tar -czf zema-debug.tar.gz \
    data/logs/ \
    .env \
    /var/log/syslog
```

---

## ⚡ Quick Tips

- **Reboot fixes 90% of issues** - try it first
- **Check logs** - most errors are logged clearly  
- **Temperature matters** - keep Pi <75°C
- **Camera needs USB 3.0** - use blue port for 4K
- **Use official power supply** - 27W for stability
- **Speak clearly** - voice detection needs good audio
- **Dashboard is your friend** - easier than command line
- **Backup before experiments** - save your data
- **Update regularly** - keep system current
- **Monitor disk space** - models take space

---

**Need more help?** See `ZEMA-TROUBLESHOOTING.md` for detailed problem-solving.

**Print this card** and keep near your Raspberry Pi! 📄🖨️