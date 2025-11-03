# ZEMA - Windows 11 Setup & Ubuntu Migration Guide
## Complete Development Environment Setup

**Purpose:** Set up Zema development on Windows 11, then migrate to Ubuntu on mini PC  
**Target:** BOSGAME P3 Lite Mini PC (AMD Ryzen 7 6800H, 24GB DDR5)  
**OS:** Windows 11 (development) → Ubuntu 22.04 LTS (production)  
**Last Updated:** November 1, 2025

---

## 🎯 Overview

**Development Flow:**
1. **Develop on Windows 11** (your main computer)
   - Install Python, Git, Cursor IDE
   - Build and test locally
   - Use Windows for development

2. **Deploy to Ubuntu** (BOSGAME P3 Lite Mini PC)
   - Migrate project to Ubuntu
   - Install production dependencies
   - Run Zema on mini PC

**Why This Approach:**
- ✅ Develop comfortably on Windows
- ✅ Test before deploying
- ✅ Easy migration path
- ✅ Best of both worlds

---

## 📋 PART 1: Windows 11 Development Setup

### Step 1: Install Python 3.12 (Latest Stable)

**Python Version Info:**
- **Current Latest:** Python 3.12.x (as of Nov 2025)
- **Minimum Required:** Python 3.11+
- **Recommended:** Python 3.12.x (best performance, latest features)

#### Installation Steps:

1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Click "Download Python 3.12.x" (latest version)
   - File: `python-3.12.x-amd64.exe`

2. **Install Python:**
   - Run installer
   - ✅ **CHECK:** "Add Python to PATH" (IMPORTANT!)
   - ✅ **CHECK:** "Install for all users" (optional)
   - Click "Install Now"
   - Wait for installation (2-3 minutes)

3. **Verify Installation:**
   ```powershell
   # Open PowerShell (Windows key + X, then "Windows PowerShell")
   python --version
   # Should show: Python 3.12.x
   
   pip --version
   # Should show: pip 24.x.x
   ```

4. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

**Troubleshooting:**
- If `python --version` doesn't work:
  - Restart PowerShell/Command Prompt
  - Check PATH: `$env:PATH` (should include Python)
  - Reinstall Python with "Add to PATH" checked

---

### Step 2: Install Git for Windows

1. **Download Git:**
   - Visit: https://git-scm.com/download/win
   - Download installer (64-bit)

2. **Install Git:**
   - Run installer
   - Use default settings (recommended)
   - Choose "Git from command line and also from 3rd-party software"
   - Click "Next" through all steps
   - Click "Install"

3. **Verify Installation:**
   ```powershell
   git --version
   # Should show: git version 2.x.x
   ```

4. **Configure Git (First Time):**
   ```powershell
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

---

### Step 3: Install Cursor IDE

1. **Download Cursor:**
   - Visit: https://cursor.sh/
   - Click "Download for Windows"
   - Run installer

2. **Install Cursor:**
   - Use default settings
   - Launch Cursor

3. **Configure Python in Cursor:**
   - Open Cursor
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose Python 3.12 from list

---

### Step 4: Install Windows Build Tools (For Audio Libraries)

**Why:** Some Python packages (like `pyaudio`) need C++ compiler

1. **Install Visual Studio Build Tools:**
   - Download: https://visualstudio.microsoft.com/downloads/
   - Choose "Build Tools for Visual Studio 2022"
   - Install "C++ build tools" workload
   - Or use simpler method below

2. **Alternative (Easier):**
   ```powershell
   # Install pre-built wheels for Windows
   pip install pipwin
   pipwin install pyaudio
   ```

---

### Step 5: Set Up Development Environment

**Follow:** `ZEMA-GETTING-STARTED.md` Steps 1-3

1. **Create Project Folder:**
   ```powershell
   cd C:\Users\YourName\Projects
   mkdir zema-ai
   cd zema-ai
   ```

2. **Open in Cursor:**
   - File → Open Folder → Select `zema-ai`

3. **Let Cursor AI Set Up Everything:**
   - Copy setup prompt from `ZEMA-GETTING-STARTED.md`
   - Paste in Cursor chat
   - Cursor creates everything

---

## 📋 PART 2: Migrating to Ubuntu on Mini PC

### Overview

**Migration Strategy:**
1. Develop on Windows (local)
2. Commit to Git
3. Push to GitHub
4. Clone on Ubuntu mini PC
5. Set up production environment

---

### Step 1: Push to GitHub (From Windows)

1. **Create GitHub Repository:**
   - Visit: https://github.com/new
   - Name: `zema-ai`
   - Don't initialize with README (we have one)
   - Click "Create repository"

2. **Push from Windows:**
   ```powershell
   cd C:\Users\YourName\Projects\zema-ai
   
   # Initialize Git (if not done)
   git init
   
   # Add remote
   git remote add origin https://github.com/YOUR_USERNAME/zema-ai.git
   
   # Commit all files
   git add .
   git commit -m "Initial commit - Windows development setup"
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Set Up Ubuntu on Mini PC

**Follow:** `ZEMA-BOSGAME-P3-LITE-CONFIG.md` for detailed Ubuntu setup

**Quick Steps:**

1. **Install Ubuntu 22.04 LTS:**
   - Download ISO: https://ubuntu.com/download/desktop
   - Create bootable USB (Rufus/BalenaEtcher)
   - Boot mini PC from USB
   - Install Ubuntu (replace Windows or dual boot)

2. **Update System:**
   ```bash
   sudo apt update
   sudo apt full-upgrade -y
   sudo reboot
   ```

3. **Install Python 3.12:**
   ```bash
   # Ubuntu 22.04 comes with Python 3.10
   # We need Python 3.12
   
   # Add deadsnakes PPA
   sudo apt install software-properties-common -y
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt update
   
   # Install Python 3.12
   sudo apt install python3.12 python3.12-venv python3.12-dev -y
   
   # Verify
   python3.12 --version
   # Should show: Python 3.12.x
   
   # Install pip
   curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
   
   # Verify pip
   python3.12 -m pip --version
   ```

4. **Install Git:**
   ```bash
   sudo apt install git -y
   git --version
   ```

5. **Install Build Tools (For Audio Libraries):**
   ```bash
   sudo apt install build-essential portaudio19-dev python3.12-dev -y
   ```

---

### Step 3: Clone Project on Ubuntu

```bash
# Clone repository
cd ~
git clone https://github.com/YOUR_USERNAME/zema-ai.git
cd zema-ai

# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version
# Should show: Python 3.12.x

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
pip list
```

---

### Step 4: Install Ollama on Ubuntu

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Download Llama 13B model
ollama pull llama3.2:13b

# Test Ollama
ollama run llama3.2:13b "Say hello"
```

---

### Step 5: Set Up Camera & Audio

**Follow:** `ZEMA-BOSGAME-P3-LITE-CONFIG.md` sections 6-7

**Quick Verification:**
```bash
# Check camera detected
lsusb | grep Insta360
v4l2-ctl --list-devices

# Check audio devices
arecord -l
aplay -l

# Test camera capture
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg
```

---

### Step 6: Run Hardware Verification

```bash
cd ~/zema-ai
source venv/bin/activate

# Run verification scripts
python scripts/verify_hardware.py
python scripts/verify_audio.py
python scripts/verify_ollama.py
python scripts/verify_camera.py
```

**All should pass!** ✅

---

## 🔄 Continuous Development Workflow

### Daily Development Pattern:

**On Windows (Development):**
```powershell
# 1. Make changes
# 2. Test locally
# 3. Commit changes
git add .
git commit -m "feat: Feature description"

# 4. Push to GitHub
git push origin main
```

**On Ubuntu (Production):**
```bash
# 1. Pull latest changes
cd ~/zema-ai
git pull origin main

# 2. Update dependencies if needed
source venv/bin/activate
pip install -r requirements.txt

# 3. Restart Zema service
sudo systemctl restart zema
```

---

## 🔧 Differences: Windows vs Ubuntu

### File Paths:

| Windows | Ubuntu |
|---------|--------|
| `C:\Users\Name\Projects\zema-ai` | `~/zema-ai` |
| `venv\Scripts\activate` | `source venv/bin/activate` |
| `python` | `python3.12` |

### Audio Libraries:

- **Windows:** Use `pipwin` for `pyaudio`
- **Ubuntu:** Install `portaudio19-dev` first, then `pip install pyaudio`

### Camera Access:

- **Windows:** Uses DirectShow (may need different drivers)
- **Ubuntu:** Uses V4L2 (standard Linux video)

---

## 🚨 Common Migration Issues

### Issue: Python Version Mismatch

**Problem:** Windows has Python 3.12, Ubuntu has 3.10

**Solution:**
```bash
# On Ubuntu, install Python 3.12 (see Step 2 above)
# Always use python3.12 explicitly
python3.12 -m venv venv
```

### Issue: Audio Not Working on Ubuntu

**Solution:**
```bash
# Install audio dependencies
sudo apt install portaudio19-dev alsa-utils -y
pip install pyaudio
```

### Issue: Camera Not Detected on Ubuntu

**Solution:**
```bash
# Check USB permissions
lsusb | grep Insta360

# Add user to video group
sudo usermod -a -G video $USER
# Log out and back in

# Test camera
v4l2-ctl --list-devices
```

---

## ✅ Migration Checklist

### Before Migrating:

- [ ] Code committed to Git
- [ ] Pushed to GitHub
- [ ] Ubuntu installed on mini PC
- [ ] Python 3.12 installed on Ubuntu
- [ ] Git installed on Ubuntu
- [ ] Build tools installed

### After Migration:

- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Ollama installed and running
- [ ] Camera detected
- [ ] Audio working
- [ ] Hardware verification passed
- [ ] Zema runs successfully

---

## 🎯 Summary

**Windows 11 Setup:**
1. Install Python 3.12
2. Install Git
3. Install Cursor IDE
4. Set up project

**Ubuntu Migration:**
1. Push to GitHub
2. Install Ubuntu on mini PC
3. Install Python 3.12
4. Clone repository
5. Install dependencies
6. Verify hardware

**Daily Workflow:**
- Develop on Windows
- Push to GitHub
- Pull on Ubuntu
- Deploy and test

**You're ready!** Start with Windows setup, then migrate when ready. 🚀

