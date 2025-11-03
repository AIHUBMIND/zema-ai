# ZEMA - Mini PC Setup Guide
## Setting Up Zema on Mini PC (Intel/AMD)

**Purpose:** Complete guide for setting up Zema on mini PC hardware  
**Target Hardware:** Intel N95/N100 or AMD Ryzen 5 3550H mini PCs  
**OS:** Ubuntu 22.04 LTS (recommended) or Windows 11 Pro  
**Last Updated:** November 1, 2025

---

## 🎯 Hardware Requirements

### Recommended Mini PC Options:

**Option 1: AMD Ryzen 5 3550H** (Best Performance)
- **Model:** WOWEE Ryzen 5 3550H Mini PC
- **Specs:** 16GB RAM, 512GB SSD, AMD Ryzen 5 3550H (4C/8T)
- **Price:** ~$160-180
- **Buy Links:**
  - [Amazon](https://www.amazon.com/dp/B0C1V3QR2X)
  - [AliExpress](https://www.aliexpress.com/item/1005007012512063.html)
  - [eBay](https://www.ebay.com/itm/336155624071)

**Option 2: Intel N95/N100** (Good Balance)
- **Model:** Firebat AK2 Plus Pro or Beelink Mini S12 Pro
- **Specs:** 16GB RAM, 512GB SSD, Intel N95/N100 (4C)
- **Price:** ~$150-180
- **Buy Links:**
  - [Firebat AK2 Plus Pro](https://www.aliexpress.com/item/1005005967641139.html)
  - [Beelink Mini S12 Pro](https://www.amazon.com/dp/B08XBVXNFP)

### Why Mini PC Over Raspberry Pi?

| Feature | Mini PC (N95/Ryzen) | Raspberry Pi 5 |
|---------|---------------------|----------------|
| CPU Performance | x86, 4-8 cores, faster | ARM, slower |
| RAM | 16GB DDR4/DDR5 | 8GB max |
| Storage | Fast NVMe SSD | Slow microSD |
| LLM Support | 13B models easily | 7B models only |
| OS | Full Ubuntu/Windows | Linux only |
| Price | $150-180 | $80-110 |

**Verdict:** Mini PC is 2-3x faster for LLM inference and can run larger models.

---

## 📋 Step 1: Hardware Setup

### Unboxing & Initial Setup:

1. **Unbox Mini PC**
   - Remove all packaging
   - Check included accessories (power adapter, HDMI cable if any)

2. **Connect Hardware:**
   ```
   - Power adapter → Mini PC
   - HDMI → Monitor/TV
   - USB keyboard → USB port
   - USB mouse → USB port
   - Ethernet cable → Network port (optional, Wi-Fi also works)
   ```

3. **Connect Camera:**
   - Insta360 Link 2 → USB-C or USB-A port
   - Wait for Windows/Linux to detect

4. **Connect Audio:**
   - USB speaker → USB port
   - Or use 3.5mm audio jack if available

5. **Power On:**
   - Press power button
   - Wait for boot (usually comes with Windows 11 Pro pre-installed)

---

## 📋 Step 2: Install Ubuntu 22.04 (Recommended)

### Why Ubuntu Instead of Windows?

- ✅ Better LLM performance (native Linux tools)
- ✅ Easier Python/AI library installation
- ✅ Better for server/background tasks
- ✅ Free and open source

### Installation Steps:

#### Option A: Replace Windows (Clean Install)

1. **Download Ubuntu 22.04 LTS Desktop:**
   - Visit: https://ubuntu.com/download/desktop
   - Download ISO file (~5GB)

2. **Create Bootable USB:**
   - Use **Rufus** (Windows) or **BalenaEtcher** (Mac/Linux)
   - Insert USB drive (8GB+)
   - Flash Ubuntu ISO to USB

3. **Boot from USB:**
   - Power off mini PC
   - Insert USB drive
   - Power on → Press F2/F12/DEL to enter BIOS
   - Change boot order → USB first
   - Save and exit

4. **Install Ubuntu:**
   - Select "Install Ubuntu"
   - Follow installer:
     - Language: English
     - Keyboard: Your layout
     - Installation type: **Erase disk and install Ubuntu** (⚠️ This deletes Windows)
     - Username: `zema` (or your choice)
     - Password: Choose strong password
   - Wait for installation (~15-20 minutes)
   - Reboot when prompted

#### Option B: Dual Boot (Keep Windows)

1. **Shrink Windows Partition:**
   - Boot into Windows
   - Open Disk Management
   - Shrink C: drive (leave ~100GB free)
   - Create unallocated space

2. **Boot from Ubuntu USB:**
   - Follow steps above
   - Choose "Install Ubuntu alongside Windows"
   - Select unallocated space
   - Complete installation

3. **Boot Menu:**
   - On startup, choose Ubuntu or Windows

---

## 📋 Step 3: Initial Ubuntu Setup

### First Boot Tasks:

1. **Update System:**
   ```bash
   sudo apt update
   sudo apt full-upgrade -y
   sudo reboot
   ```

2. **Install Essential Tools:**
   ```bash
   sudo apt install -y \
       git curl wget vim \
       build-essential \
       python3.11 python3-pip python3-venv \
       ffmpeg portaudio19-dev \
       sqlite3 \
       v4l-utils uvcdynctrl
   ```

3. **Verify Hardware:**
   ```bash
   # Check CPU
   lscpu | grep "Model name"
   
   # Check RAM
   free -h
   
   # Check storage
   df -h
   
   # Check camera
   v4l2-ctl --list-devices
   lsusb | grep -i insta360
   
   # Check audio
   arecord -l
   aplay -l
   ```

**Expected Output:**
- CPU: Intel N95/N100 or AMD Ryzen 5 3550H
- RAM: 16GB total
- Storage: ~500GB available
- Camera: Insta360 Link 2 detected
- Audio: Microphone and speaker detected

---

## 📋 Step 4: Install Ollama & Llama 13B

### Install Ollama:

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Verify installation
ollama --version
```

### Download Llama 13B Model (or Larger):

```bash
# Download Llama 3.2 13B (quantized) - Recommended
ollama pull llama3.2:13b

# Or Llama 3.1 13B
ollama pull llama3.1:13b

# For BOSGAME P3 Lite with 24GB RAM, you can also try:
# Llama 3.2 70B (quantized Q4) - Requires ~40GB RAM
# ollama pull llama3.2:70b

# Or other models:
ollama pull qwen2.5:14b
ollama pull gemma2:9b

# Verify model downloaded
ollama list
```

### Test Llama 13B:

```bash
# Test generation
echo "Hello, what is 2+2?" | ollama run llama3.2:13b

# Expected: Response in 2-5 seconds (BOSGAME P3 Lite)
# Expected: Response in 5-15 seconds (Ryzen 5 3550H / Intel N95)
```

**Performance Expectations:**
- **BOSGAME P3 Lite (6800H):** 15-30 tokens/second (very fast!)
- **Mini PC (Intel N95/N100):** 5-15 tokens/second
- **Mini PC (AMD Ryzen 5 3550H):** 8-20 tokens/second
- **Response time:** 2-5 seconds for simple queries (BOSGAME)

---

## 📋 Step 5: Install Python Dependencies

### Create Virtual Environment:

```bash
# Create project directory
mkdir -p ~/zema-ai
cd ~/zema-ai

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Install Python Packages:

```bash
# Install core dependencies
pip install \
    fastapi uvicorn \
    pydantic \
    pyaudio \
    numpy \
    opencv-python-headless \
    faster-whisper \
    httpx \
    sqlalchemy \
    aiofiles \
    python-multipart
```

### Test Python Installation:

```bash
python3 --version  # Should show 3.11+
python3 -c "import cv2; print('OpenCV OK')"
python3 -c "import pyaudio; print('PyAudio OK')"
```

---

## 📋 Step 6: Camera Setup (Insta360 Link 2)

### Verify Camera Detection:

```bash
# List USB devices
lsusb | grep -i insta360

# List video devices
v4l2-ctl --list-devices

# Should show: Insta360 Link 2
```

### Test Camera Capture:

```bash
# Capture test image
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg

# View image
eog test.jpg  # or use any image viewer
```

### Configure Camera Settings:

```bash
# List available controls
v4l2-ctl --list-ctrls

# Set resolution (if needed)
v4l2-ctl --set-fmt-video=width=1920,height=1080

# Test video stream
ffplay /dev/video0  # Press 'q' to quit
```

---

## 📋 Step 7: Audio Setup

### Verify Audio Devices:

```bash
# List audio input devices
arecord -l

# List audio output devices
aplay -l

# Test microphone
arecord -D hw:1,0 -d 5 -f cd test.wav

# Test playback
aplay test.wav
```

### Configure Default Audio:

```bash
# Install PulseAudio GUI (optional)
sudo apt install -y pavucontrol

# Run PulseAudio Volume Control
pavucontrol

# Set default input/output devices
```

---

## 📋 Step 8: Clone & Setup Zema Project

### Clone Repository (When Ready):

```bash
# Navigate to home directory
cd ~

# Clone Zema project (adjust URL when repository is ready)
git clone https://github.com/YOUR_USERNAME/zema-ai.git
cd zema-ai

# Or create from scratch using prompts
mkdir -p ~/zema-ai
cd ~/zema-ai
```

### Create Project Structure:

Use **SETUP-001** prompt from `ZEMA-CURSOR-PROMPTS.md`:

1. Open Cursor IDE (or VS Code)
2. Open folder: `~/zema-ai`
3. Copy SETUP-001 prompt
4. Paste into Cursor chat
5. AI generates project structure

### Install Project Dependencies:

```bash
# Activate virtual environment
source venv/bin/activate

# Install from requirements.txt (when created)
pip install -r requirements.txt
```

---

## 📋 Step 9: Hardware Verification Scripts

### Run Verification:

```bash
# After SETUP-001 creates scripts/
cd ~/zema-ai
python scripts/verify_hardware.py
python scripts/verify_audio.py
python scripts/verify_ollama.py
python scripts/verify_camera.py
```

**Acceptance Criteria:**
- ✅ All verification scripts pass
- ✅ Camera detected and working
- ✅ Audio input/output working
- ✅ Ollama running
- ✅ Llama 13B model loaded
- ✅ System performance acceptable

---

## 📋 Step 10: Configure Zema Service

### Create Systemd Service:

```bash
# Create service file
sudo nano /etc/systemd/system/zema.service
```

**Service File Contents:**

```ini
[Unit]
Description=Zema AI Personal Assistant
After=network.target ollama.service

[Service]
Type=simple
User=zema
WorkingDirectory=/home/zema/zema-ai
Environment="PATH=/home/zema/zema-ai/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/zema/zema-ai/venv/bin/python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable & Start Service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable zema

# Start service
sudo systemctl start zema

# Check status
sudo systemctl status zema

# View logs
journalctl -u zema -f
```

---

## 📋 Step 11: Access Web Dashboard

### Start Zema (if not running as service):

```bash
cd ~/zema-ai
source venv/bin/activate
python -m src.main
```

### Access Dashboard:

- Open browser: `http://localhost:8000`
- Or from another device: `http://MINI_PC_IP:8000`

**Find Mini PC IP:**
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

---

## 🔧 Troubleshooting

### Camera Not Detected:

```bash
# Check USB connection
lsusb | grep -i insta360

# Check video device
ls -l /dev/video*

# Reinstall v4l2 tools
sudo apt install --reinstall v4l-utils

# Try different USB port
```

### Ollama Not Running:

```bash
# Check service status
sudo systemctl status ollama

# Restart service
sudo systemctl restart ollama

# Check logs
journalctl -u ollama -n 50
```

### Audio Issues:

```bash
# Check PulseAudio
pulseaudio --check -v

# Restart PulseAudio
pulseaudio -k
pulseaudio --start

# Test devices
pavucontrol
```

### Performance Issues:

```bash
# Check CPU usage
htop

# Check memory
free -h

# Check disk space
df -h

# Monitor temperature (if sensors available)
sensors
```

---

## ✅ Acceptance Criteria

### System Ready When:

- [ ] Ubuntu 22.04 installed and updated
- [ ] Python 3.11+ installed
- [ ] Ollama installed and running
- [ ] Llama 13B model downloaded
- [ ] Camera detected (`/dev/video0`)
- [ ] Audio input/output working
- [ ] Project structure created
- [ ] Virtual environment set up
- [ ] Dependencies installed
- [ ] Verification scripts pass
- [ ] Zema service running (optional)
- [ ] Web dashboard accessible

---

## 📚 Next Steps

### After Hardware Setup:

1. **Start Building:**
   - Follow `ZEMA-CURSOR-PROMPTS.md`
   - Start with SETUP-001
   - Build features sequentially

2. **Development Workflow:**
   ```bash
   # Activate environment
   cd ~/zema-ai
   source venv/bin/activate
   
   # Make changes
   # Test locally
   python -m src.main
   
   # When ready, enable service
   sudo systemctl restart zema
   ```

3. **Monitor Logs:**
   ```bash
   # Application logs
   tail -f data/logs/zema.log
   
   # Service logs
   journalctl -u zema -f
   ```

---

## 🎯 Quick Reference

### Essential Commands:

```bash
# System info
lscpu                    # CPU info
free -h                  # Memory
df -h                    # Disk space

# Ollama
ollama list              # List models
ollama run llama3.2:13b  # Test model
sudo systemctl status ollama

# Zema
cd ~/zema-ai
source venv/bin/activate
python -m src.main

# Service
sudo systemctl status zema
sudo systemctl restart zema
journalctl -u zema -f
```

### File Locations:

```
~/zema-ai/              # Project directory
~/zema-ai/venv/          # Virtual environment
~/zema-ai/data/          # Data directory
~/zema-ai/data/logs/     # Log files
/etc/systemd/system/zema.service  # Service file
```

---

## 🚀 You're Ready!

Your mini PC is now configured for Zema! The system is:
- ✅ More powerful than Raspberry Pi
- ✅ Can run Llama 13B models
- ✅ Ready for development
- ✅ Optimized for AI workloads

**Next:** Start building features using `ZEMA-CURSOR-PROMPTS.md`!

