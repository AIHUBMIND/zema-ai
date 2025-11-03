# ZEMA - Local Development Guide
## Building Zema on Your Computer Before Hardware Arrives

**Purpose:** Start building Zema structure on your computer now  
**Platform:** Windows/Mac/Linux (your current computer)  
**When:** Before mini PC arrives  
**Last Updated:** November 1, 2025

---

## 🎯 Why Build Locally First?

**Benefits:**
- ✅ Start immediately (don't wait for hardware)
- ✅ Test project structure and configuration
- ✅ Build non-hardware features (dashboard, API, database)
- ✅ Learn the codebase before deployment
- ✅ Easy to transfer to mini PC later

**What Works Locally:**
- ✅ Project structure
- ✅ Configuration system
- ✅ Logging system
- ✅ Database schema
- ✅ API endpoints
- ✅ Web dashboard
- ✅ Unit tests

**What Needs Hardware:**
- ⚠️ Voice input/output (microphone/speaker)
- ⚠️ Camera (Insta360 Link 2)
- ⚠️ Ollama/Llama (can install locally though!)

---

## 📋 Step 1: Install Development Tools

### Required Software:

1. **Python 3.11+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version` (should show 3.11+)

2. **Git**
   - Download: https://git-scm.com/downloads
   - Verify: `git --version`

3. **Cursor IDE** (or VS Code)
   - Download: https://cursor.sh/
   - Install Python extension

4. **Terminal/Command Line**
   - Windows: PowerShell or Git Bash
   - Mac: Terminal (built-in)
   - Linux: Terminal (built-in)

---

## 📋 Step 2: Create Project Structure

### Initialize Project:

```bash
# Create project directory
mkdir zema-ai
cd zema-ai

# Initialize Git repository
git init
git branch -M main

# Create .gitignore
echo "venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
data/logs/*.log
.env
*.db
*.sqlite" > .gitignore
```

### Use SETUP-001 Prompt:

1. **Open Cursor IDE**
   - File → Open Folder → Select `zema-ai`

2. **Open Prompt Document**
   - Open `ZEMA-CURSOR-PROMPTS.md`
   - Find "SETUP-001: Create Project Structure"

3. **Copy Prompt**
   - Select entire markdown code block
   - Copy to clipboard

4. **Paste in Cursor**
   - Press `Ctrl+L` (or `Cmd+L` on Mac) to open chat
   - Paste prompt
   - Press Enter

5. **AI Generates Structure**
   - Review generated files
   - Accept changes

**Expected Result:**
```
zema-ai/
├── src/
│   ├── core/
│   ├── config/
│   ├── voice/
│   ├── vision/
│   └── ...
├── scripts/
├── tests/
├── data/
├── requirements.txt
└── README.md
```

---

## 📋 Step 3: Set Up Python Environment

### Create Virtual Environment:

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Verify activation
which python  # Should show venv path
```

### Install Basic Dependencies:

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install core packages
pip install \
    fastapi \
    uvicorn \
    pydantic \
    httpx \
    sqlalchemy \
    aiofiles \
    python-multipart
```

---

## 📋 Step 4: Build Configuration System

### Use SETUP-002 Prompt:

1. **Open ZEMA-CURSOR-PROMPTS.md**
2. **Find SETUP-002: Configuration System**
3. **Copy prompt → Paste in Cursor**
4. **AI generates configuration code**

### Test Configuration:

```bash
# Test configuration loading
python -c "from src.config.settings import Settings; s = Settings(); print(s)"
```

**Expected Output:**
- Configuration loads successfully
- Settings file created (`data/config/settings.yaml`)

---

## 📋 Step 5: Build Logging System

### Use SETUP-003 Prompt:

1. **Find SETUP-003: Logging System**
2. **Copy prompt → Paste in Cursor**
3. **AI generates logging code**

### Test Logging:

```bash
# Test logging
python -c "import logging; from src.utils.logger import setup_logger; logger = setup_logger(); logger.info('Test log')"
```

**Expected Output:**
- Log file created (`data/logs/zema.log`)
- Log message written

---

## 📋 Step 6: Build Non-Hardware Features

### Features You Can Build Now:

**Phase 2: Web Dashboard** (No hardware needed)
- DASHBOARD-001: FastAPI server
- DASHBOARD-002: HTML/CSS interface
- DASHBOARD-003: JavaScript application
- DASHBOARD-004: API endpoints
- DASHBOARD-005: WebSocket updates

**Phase 3: Configuration** (No hardware needed)
- CONFIG-001: System config tool
- CONFIG-002: Configuration manager
- CONFIG-003: Voice command integration

**Database & Storage** (No hardware needed)
- SETUP-001: Database schema
- SETUP-002: Data models

**Testing** (No hardware needed)
- TEST-001: Unit tests
- TEST-002: Integration tests
- TEST-003: Hardware mocks

---

## 📋 Step 7: Install Ollama Locally (Optional)

### Why Install Locally?

- ✅ Test LLM integration before mini PC arrives
- ✅ Use smaller models (7B) for testing
- ✅ Verify API calls work

### Install Ollama:

**Windows:**
```powershell
# Download from https://ollama.com/download
# Install Ollama
# Run: ollama pull llama3.2:7b
```

**Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:7b
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:7b
```

### Test Ollama:

```bash
# Test generation
echo "Hello" | ollama run llama3.2:7b
```

**Note:** For production, use Llama 13B on mini PC. Use 7B locally for testing.

---

## 📋 Step 8: Build Mock Hardware (Optional)

### Create Hardware Mocks:

You can build hardware mock modules to test without physical hardware:

```python
# src/voice/mock_audio_io.py
class MockAudioIO:
    """Mock audio I/O for testing"""
    def record_audio(self, duration):
        # Return fake audio data
        return np.zeros(16000 * duration)
    
    def play_audio(self, audio_data):
        # Fake playback
        pass
```

This lets you:
- ✅ Test voice flow logic
- ✅ Test conversation loop
- ✅ Develop features without hardware

---

## 📋 Step 9: Commit & Push to Git

### Version Control:

```bash
# Stage all files
git add .

# Commit
git commit -m "feat: Initial project structure

- Created project structure (SETUP-001)
- Added configuration system (SETUP-002)
- Added logging system (SETUP-003)
- Ready for hardware deployment"

# Push to GitHub (if you have remote)
git remote add origin https://github.com/YOUR_USERNAME/zema-ai.git
git push -u origin main
```

---

## 📋 Step 10: Prepare for Mini PC Transfer

### When Hardware Arrives:

1. **Transfer Project:**
   ```bash
   # On mini PC
   git clone https://github.com/YOUR_USERNAME/zema-ai.git
   cd zema-ai
   ```

2. **Install Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Hardware:**
   - Follow `ZEMA-MINI-PC-SETUP-GUIDE.md`
   - Connect camera
   - Configure audio
   - Install Ollama 13B

4. **Test Everything:**
   ```bash
   python scripts/verify_hardware.py
   python scripts/verify_audio.py
   python scripts/verify_ollama.py
   ```

---

## 🚀 Development Workflow

### Daily Workflow:

```bash
# 1. Activate environment
cd zema-ai
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Make changes
# Edit files, use Cursor prompts, etc.

# 3. Test locally
python -m pytest tests/  # Run tests
python -m src.main      # Run application (if possible)

# 4. Commit changes
git add .
git commit -m "feat: Added feature X"

# 5. Push to GitHub
git push origin main
```

### When Mini PC Arrives:

```bash
# 1. SSH to mini PC
ssh zema@MINI_PC_IP

# 2. Pull latest code
cd zema-ai
git pull origin main

# 3. Install new dependencies
source venv/bin/activate
pip install -r requirements.txt

# 4. Test on hardware
python scripts/verify_hardware.py

# 5. Run Zema
python -m src.main
```

---

## ✅ What You Can Build Now

### ✅ Ready to Build (No Hardware):

- [x] Project structure (SETUP-001)
- [x] Configuration system (SETUP-002)
- [x] Logging system (SETUP-003)
- [x] Database schema
- [x] API endpoints
- [x] Web dashboard UI
- [x] Configuration manager
- [x] User management
- [x] Conversation history storage
- [x] Unit tests
- [x] Integration tests

### ⏳ Need Hardware:

- [ ] Voice input/output
- [ ] Camera integration
- [ ] Ollama 13B setup
- [ ] Hardware verification
- [ ] End-to-end voice flow
- [ ] Vision features

---

## 📊 Progress Tracking

### Track What You've Built:

Create `PROGRESS.md`:

```markdown
# Zema Development Progress

## Completed (Local Development)
- [x] Project structure
- [x] Configuration system
- [x] Logging system
- [x] Database schema
- [x] API endpoints
- [ ] Web dashboard UI
- [ ] User management

## Pending (Need Hardware)
- [ ] Hardware verification
- [ ] Voice input/output
- [ ] Camera integration
- [ ] Ollama 13B setup
- [ ] End-to-end testing
```

---

## 🎯 Next Steps

### Right Now:

1. **Set up local development environment**
2. **Create project structure** (SETUP-001)
3. **Build configuration** (SETUP-002)
4. **Build logging** (SETUP-003)
5. **Start building dashboard** (Phase 2)

### When Mini PC Arrives:

1. **Transfer project** (git clone)
2. **Install hardware** (camera, audio)
3. **Configure Ollama** (Llama 13B)
4. **Run verification** (hardware tests)
5. **Deploy and test** (full system)

---

## 💡 Pro Tips

### For Local Development:

1. **Use Mock Hardware**
   - Create mock modules for audio/camera
   - Test logic without physical hardware

2. **Test API Endpoints**
   - Use Postman or curl
   - Test dashboard endpoints
   - Verify database operations

3. **Commit Frequently**
   - Commit after each working feature
   - Push to GitHub regularly
   - Easy to transfer to mini PC

4. **Read Documentation**
   - Understand architecture before coding
   - Reference implementation guide
   - Follow prompts sequentially

---

## 🎉 You're Ready!

**You can start building NOW!**

- ✅ No hardware needed for project structure
- ✅ Build dashboard, API, database
- ✅ Test locally with mocks
- ✅ Transfer to mini PC when ready

**Start with SETUP-001 prompt and begin building!**

