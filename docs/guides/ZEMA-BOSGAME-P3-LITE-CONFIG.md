# ZEMA - BOSGAME P3 Lite Configuration Guide
## Optimizing Your High-End Mini PC for Zema

**Purpose:** Complete configuration guide for BOSGAME P3 Lite Mini PC  
**Hardware:** AMD Ryzen 7 6800H, 24GB DDR5, 1TB PCIe 4.0 NVMe  
**Target:** Maximum performance for Llama 13B+ and advanced AI workloads  
**Last Updated:** November 1, 2025

---

## 🎉 Excellent Choice!

**Congratulations!** You've selected one of the **best mini PCs available** for local AI/LLM work. The BOSGAME P3 Lite with Ryzen 7 6800H is a **flagship system** that will easily handle:

- ✅ Llama 13B models (real-time, fast responses)
- ✅ Multiple concurrent AI tasks
- ✅ Future expansion (64GB RAM possible)
- ✅ Advanced vision processing
- ✅ Multi-monitor development
- ✅ Professional-grade performance

---

## 📋 System Specifications

### Your Hardware:

| Component | Specification |
|-----------|---------------|
| **CPU** | AMD Ryzen 7 6800H (8 cores/16 threads) |
| **Base Clock** | Up to 4.7GHz turbo |
| **RAM** | 24GB DDR5 (expandable to 64GB) |
| **Storage** | 1TB PCIe 4.0x4 NVMe SSD |
| **GPU** | Radeon 680M integrated |
| **Display** | Triple output (HDMI, DP, USB4 up to 8K60Hz) |
| **Network** | Dual 2.5GbE LAN, WiFi 6E, Bluetooth 5.2 |
| **USB** | Multiple USB 3, USB4/Type-C |

---

## 🚀 Step 1: Initial Setup

### Unboxing & First Boot:

1. **Unbox and Connect:**
   ```
   - Connect power adapter
   - Connect monitor via HDMI/DP/USB4
   - Connect keyboard and mouse
   - Connect Insta360 Link 2 camera
   - Connect USB speaker
   ```

2. **Boot System:**
   - Usually comes with Windows 11 Pro pre-installed
   - First boot: Complete Windows setup
   - Update Windows completely

3. **Verify Hardware:**
   - Check Device Manager for all components
   - Verify RAM shows 24GB
   - Verify SSD shows ~1TB

---

## 🚀 Step 2: Install Ubuntu 22.04 LTS (Recommended)

### Why Ubuntu for AI?

- ✅ Better LLM performance
- ✅ Native Linux tools (llama.cpp, Ollama)
- ✅ Easier Python/AI library installation
- ✅ Better for server/background tasks
- ✅ Professional development environment

### Installation Options:

#### Option A: Replace Windows (Clean Install)

1. **Download Ubuntu 22.04 Desktop:**
   - Visit: https://ubuntu.com/download/desktop
   - Download ISO (~5GB)

2. **Create Bootable USB:**
   - Use **Rufus** (Windows) or **BalenaEtcher**
   - Flash Ubuntu ISO to USB drive (8GB+)

3. **Boot from USB:**
   - Power off mini PC
   - Insert USB drive
   - Power on → Press **F2/F12/DEL** to enter BIOS
   - Change boot order → USB first
   - Save and exit

4. **Install Ubuntu:**
   - Select "Install Ubuntu"
   - Choose "Erase disk and install Ubuntu"
   - Set username: `zema`
   - Set password: Strong password
   - Wait for installation (~15-20 minutes)

#### Option B: Dual Boot (Keep Windows)

1. **Shrink Windows Partition:**
   - Boot into Windows
   - Open Disk Management
   - Shrink C: drive (leave ~200GB free)
   - Create unallocated space

2. **Install Ubuntu:**
   - Boot from USB
   - Choose "Install Ubuntu alongside Windows"
   - Select unallocated space
   - Complete installation

---

## 🚀 Step 3: Optimize Ubuntu for BOSGAME P3 Lite

### Update System:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

### Install Essential Tools:

```bash
sudo apt install -y \
    git curl wget vim \
    build-essential \
    python3.11 python3-pip python3-venv \
    ffmpeg portaudio19-dev \
    sqlite3 \
    v4l-utils uvcdynctrl \
    htop neofetch \
    docker.io docker-compose
```

### Enable Docker (Optional but Recommended):

```bash
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
# Log out and back in for group changes
```

### Install Graphics Drivers:

```bash
# For AMD Radeon 680M
sudo apt install -y \
    mesa-utils \
    xserver-xorg-video-amdgpu \
    libgl1-mesa-dri
```

### Verify GPU:

```bash
# Check GPU info
lspci | grep -i vga
glxinfo | grep "OpenGL renderer"
```

---

## 🚀 Step 4: Install Ollama & Optimize for Ryzen 7 6800H

### Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl start ollama
sudo systemctl enable ollama
ollama --version
```

### Configure Ollama for Maximum Performance:

```bash
# Edit Ollama configuration
sudo nano /etc/systemd/system/ollama.service
```

**Add to [Service] section:**
```ini
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_MAX_LOADED_MODELS=2"
Environment="OLLAMA_NUM_GPU=0"
Environment="OLLAMA_NUM_THREAD=16"
```

**Reload service:**
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### Download Models (Optimized for 24GB RAM):

```bash
# Recommended: Llama 3.2 13B (fits perfectly in 24GB)
ollama pull llama3.2:13b

# Alternative models (all work great):
ollama pull llama3.1:13b
ollama pull qwen2.5:14b
ollama pull gemma2:9b

# For testing (smaller, faster):
ollama pull llama3.2:7b

# Advanced: With 24GB RAM, you can try quantized 70B (requires swap)
# ollama pull llama3.2:70b
```

### Test Performance:

```bash
# Benchmark Llama 13B
time echo "Write a short story about AI" | ollama run llama3.2:13b

# Expected performance:
# - First token: < 1 second
# - Tokens/second: 15-30 tokens/sec
# - Response time: 2-5 seconds for short queries
```

---

## 🚀 Step 5: Python Environment Setup

### Create Virtual Environment:

```bash
cd ~
mkdir -p zema-ai
cd zema-ai

# Create venv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Install Core Dependencies:

```bash
pip install \
    fastapi uvicorn[standard] \
    pydantic \
    pyaudio \
    numpy \
    opencv-python-headless \
    faster-whisper \
    httpx \
    sqlalchemy \
    aiofiles \
    python-multipart \
    pyyaml \
    python-dotenv
```

### Install AI/ML Libraries:

```bash
pip install \
    torch torchvision torchaudio \
    transformers \
    accelerate \
    sentencepiece \
    onnxruntime
```

---

## 🚀 Step 6: Camera Setup (Insta360 Link 2)

### Verify Camera Detection:

```bash
# List USB devices
lsusb | grep -i insta360

# Should show: Insta360 Technologies, Inc. Link 2

# List video devices
v4l2-ctl --list-devices

# Should show: Insta360 Link 2 (/dev/video0)
```

### Test Camera Capture:

```bash
# Capture test image (4K)
ffmpeg -f v4l2 -i /dev/video0 -frames 1 -vf scale=3840:2160 test.jpg

# Test video stream
ffplay /dev/video0

# Check camera capabilities
v4l2-ctl --list-formats-ext
```

### Configure Camera Settings:

```bash
# Set resolution to 4K
v4l2-ctl --set-fmt-video=width=3840,height=2160,pixelformat=YUYV

# Enable autofocus
v4l2-ctl --set-ctrl=focus_auto=1

# Test PTZ controls (if supported)
v4l2-ctl --set-ctrl=pan_absolute=0
v4l2-ctl --set-ctrl=tilt_absolute=0
```

---

## 🚀 Step 7: Audio Setup

### Verify Audio Devices:

```bash
# List input devices
arecord -l

# List output devices
aplay -l

# Test microphone
arecord -D hw:1,0 -d 5 -f cd -r 44100 test.wav

# Test playback
aplay test.wav
```

### Configure PulseAudio:

```bash
# Install PulseAudio GUI
sudo apt install -y pavucontrol

# Run PulseAudio Volume Control
pavucontrol

# Set default input/output devices
# Configure Insta360 Link 2 microphone as default input
```

---

## 🚀 Step 8: System Optimization

### CPU Governor (Performance Mode):

```bash
# Install cpufrequtils
sudo apt install -y cpufrequtils

# Set to performance mode
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl restart cpufrequtils

# Verify
cpufreq-info
```

### Memory Optimization:

```bash
# Configure swap (if needed for larger models)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### SSD Optimization:

```bash
# Enable TRIM (keeps SSD fast)
sudo systemctl enable fstrim.timer
sudo systemctl start fstrim.timer

# Check SSD health
sudo smartctl -a /dev/nvme0n1
```

---

## 🚀 Step 9: Clone & Setup Zema Project

### Clone Repository:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/zema-ai.git
cd zema-ai

# Or create from scratch
mkdir -p ~/zema-ai
cd ~/zema-ai
```

### Use SETUP-001 Prompt:

1. Open Cursor IDE
2. Open folder: `~/zema-ai`
3. Copy SETUP-001 prompt from `ZEMA-CURSOR-PROMPTS.md`
4. Paste into Cursor chat
5. AI generates project structure

### Install Project Dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Step 10: Hardware Verification

### Run Verification Scripts:

```bash
cd ~/zema-ai
python scripts/verify_hardware.py
python scripts/verify_audio.py
python scripts/verify_ollama.py
python scripts/verify_camera.py
```

### Expected Results:

- ✅ CPU: AMD Ryzen 7 6800H detected
- ✅ RAM: 24GB DDR5 detected
- ✅ Storage: 1TB NVMe detected
- ✅ GPU: Radeon 680M detected
- ✅ Camera: Insta360 Link 2 detected
- ✅ Audio: Input/output working
- ✅ Ollama: Running with Llama 13B

---

## 🚀 Step 11: Performance Benchmarking

### CPU Benchmark:

```bash
# Install benchmarking tools
sudo apt install -y sysbench

# CPU benchmark
sysbench cpu --cpu-max-prime=20000 --threads=16 run
```

### LLM Performance Test:

```bash
# Create test script
cat > ~/test_llm.sh << 'EOF'
#!/bin/bash
echo "Testing Llama 13B performance..."
time echo "Write a 200-word essay about artificial intelligence" | ollama run llama3.2:13b > /dev/null
EOF

chmod +x ~/test_llm.sh
~/test_llm.sh
```

**Expected Performance:**
- **First token latency:** < 1 second
- **Tokens per second:** 15-30 tokens/sec
- **Total response time:** 5-15 seconds for 200 words

---

## 🚀 Step 12: Configure Zema Service

### Create Systemd Service:

```bash
sudo nano /etc/systemd/system/zema.service
```

**Service File:**

```ini
[Unit]
Description=Zema AI Personal Assistant
After=network.target ollama.service

[Service]
Type=simple
User=zema
WorkingDirectory=/home/zema/zema-ai
Environment="PATH=/home/zema/zema-ai/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/home/zema/zema-ai/venv/bin/python -m src.main
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Enable & Start Service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable zema
sudo systemctl start zema
sudo systemctl status zema
```

---

## 🎯 Optimization Tips for BOSGAME P3 Lite

### Maximum Performance:

1. **CPU Affinity:**
   ```bash
   # Pin Ollama to specific cores
   taskset -c 0-7 ollama serve
   ```

2. **Memory Allocation:**
   - With 24GB RAM, you can run multiple models simultaneously
   - Configure Ollama to use 12-16GB for models

3. **SSD Cache:**
   - Keep model files on NVMe SSD (already there!)
   - Models load instantly

4. **GPU Acceleration:**
   - Radeon 680M can handle some ONNX/DirectML workloads
   - Test GPU-accelerated vision processing

### Multi-Monitor Setup:

```bash
# Connect up to 3 displays:
# - HDMI: 4K@60Hz
# - DisplayPort: 4K@60Hz
# - USB4: 8K@60Hz

# Configure displays
xrandr --output HDMI-1 --mode 3840x2160 --rate 60
xrandr --output DP-1 --mode 3840x2160 --rate 60
```

---

## ✅ Acceptance Criteria

### System Ready When:

- [ ] Ubuntu 22.04 installed and updated
- [ ] Python 3.11+ installed
- [ ] Ollama installed and optimized
- [ ] Llama 13B model downloaded
- [ ] Camera detected and tested
- [ ] Audio input/output working
- [ ] Project structure created
- [ ] Virtual environment set up
- [ ] Dependencies installed
- [ ] Verification scripts pass
- [ ] Performance benchmarks acceptable
- [ ] Zema service running

---

## 📊 Performance Expectations

### With BOSGAME P3 Lite:

| Task | Performance |
|------|-------------|
| **Llama 13B Inference** | 15-30 tokens/sec |
| **Wake Word Detection** | < 100ms latency |
| **Speech-to-Text** | Real-time |
| **Text-to-Speech** | Real-time |
| **Vision Processing** | 30-60 FPS |
| **Multiple Models** | Can run 2-3 simultaneously |

---

## 🎉 You're Ready!

Your BOSGAME P3 Lite is **one of the best systems** for running Zema:

- ✅ **8-core CPU** → Fast LLM inference
- ✅ **24GB RAM** → Large models + multitasking
- ✅ **1TB NVMe** → Instant model loading
- ✅ **Radeon 680M** → GPU acceleration possible
- ✅ **Triple display** → Perfect for development

**This system will handle Zema beautifully!** 🚀

**Next:** Start building features using `ZEMA-CURSOR-PROMPTS.md`!

