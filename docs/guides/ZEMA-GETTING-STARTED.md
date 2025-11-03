# ZEMA - Getting Started Guide
## AI-Agent First Approach - Let Cursor Do Everything

**Purpose:** Complete setup using Cursor AI agent - minimal manual steps  
**Approach:** Tell Cursor what to do, AI handles all setup  
**Time:** 15 minutes (mostly waiting for AI)  
**Last Updated:** November 1, 2025

---

## 🎯 Quick Overview

**What You'll Do:**
1. Create folder `zema-ai`
2. Open folder in Cursor IDE
3. Give Cursor one comprehensive setup prompt
4. Cursor AI sets up everything automatically
5. Start building with prompts

**That's it!** Cursor AI handles Python, Git, dependencies, structure - everything!

---

## 📋 Prerequisites (Check These First)

### Before Starting:

- [ ] **Cursor IDE installed** ([download here](https://cursor.sh/))
- [ ] **Python 3.12+ installed** ([download here](https://www.python.org/downloads/))
   - **Note:** Python 3.12.x is latest stable (Nov 2025)
   - Minimum: Python 3.11+
   - Recommended: Python 3.12.x for best performance
   - **Windows 11 Installation:** See `ZEMA-WINDOWS-UBUNTU-MIGRATION.md` Part 1
- [ ] **Git installed** ([download here](https://git-scm.com/downloads))
- [ ] **ZEMA-CURSOR-PROMPTS.md** accessible (your coding guide)

**That's all you need!** Everything else Cursor AI will set up.

---

## 🚀 STEP 1: Create Project Folder

### On Your Computer:

**Windows:**
```powershell
# Open PowerShell or Command Prompt
cd C:\Users\YourName\Projects  # or wherever you want
mkdir zema-ai
cd zema-ai
```

**Mac/Linux:**
```bash
# Open Terminal
cd ~/Projects  # or wherever you want
mkdir zema-ai
cd zema-ai
```

**Verify:**
```bash
pwd  # Should show .../zema-ai
```

**Time:** 1 minute

---

## 🚀 STEP 2: Open Folder in Cursor IDE

### Launch Cursor:

1. **Open Cursor IDE**
2. **File → Open Folder**
3. **Select `zema-ai` folder** (the one you just created)
4. **Click "Open"**

**Verify:** Cursor IDE shows `zema-ai` folder in sidebar

**Time:** 1 minute

---

## 🚀 STEP 3: Tell Cursor AI to Set Up Everything

### This is the Magic Step! 🪄

**Open Cursor Chat:**
- Press `Ctrl+L` (Windows/Linux) or `Cmd+L` (Mac)
- Or click the chat icon in sidebar

**Copy and Paste This Complete Setup Prompt:**

```markdown
I'm building Zema AI Personal Assistant - a privacy-first voice assistant for mini PC.

Please set up the complete project structure and development environment from scratch:

REQUIREMENTS:
1. Create complete Python project structure for Zema AI
2. Initialize Git repository with proper .gitignore
3. Create Python virtual environment (venv)
4. Install all required dependencies
5. Create .cursorrules file with project-specific rules
6. Create requirements.txt with all dependencies
7. Set up proper project structure as specified below

PROJECT STRUCTURE NEEDED:
```
zema-ai/
├── src/
│   ├── core/           # Core orchestrator, state management
│   ├── config/         # Configuration management (Pydantic)
│   ├── voice/          # Voice I/O, wake word, STT, TTS
│   ├── vision/         # Camera, vision processing
│   ├── ai/             # LLM client, context management
│   ├── tools/          # Personal assistant tools
│   ├── api/            # FastAPI server, routes
│   └── utils/          # Utilities, logging, helpers
├── scripts/            # Setup, verification, utility scripts
├── tests/              # Unit tests, integration tests
├── data/               # Data directory
│   ├── config/         # Configuration files
│   ├── logs/           # Log files
│   ├── db/             # Database files
│   ├── models/         # AI model files
│   └── backups/        # Backup files
├── docs/               # Documentation
├── .gitignore          # Git ignore rules
├── .cursorrules        # Cursor AI rules
├── requirements.txt    # Python dependencies
├── README.md           # Project README
└── setup.py            # Optional setup script
```

DEPENDENCIES TO INSTALL:
- fastapi>=0.104.0
- uvicorn[standard]>=0.24.0
- pydantic>=2.5.0
- pydantic-settings>=2.1.0
- httpx>=0.25.0
- sqlalchemy>=2.0.0
- aiosqlite>=0.19.0
- aiofiles>=23.2.0
- python-multipart>=0.0.6
- pyyaml>=6.0.1
- python-dotenv>=1.0.0
- structlog>=23.2.0
- pyaudio>=0.2.14
- numpy>=1.24.0
- opencv-python-headless>=4.8.0
- faster-whisper>=0.10.0
- pytest>=7.4.0
- pytest-asyncio>=0.21.0

CURSOR RULES (.cursorrules):
- This is Zema AI Personal Assistant - privacy-first voice assistant
- Runs on mini PC (BOSGAME P3 Lite) with Ubuntu 22.04
- Uses Ollama for local LLM inference (Llama 13B) - 100% offline
- Built with Python 3.11+, FastAPI, async/await
- Follow PEP 8 Python style guide
- Use type hints for all functions
- Prefer async/await over sync code
- Use Pydantic for data validation
- Offline-first: All core features work without internet
- Privacy-first: All data stored locally
- Modular: Each module has single responsibility

GIT SETUP:
- Initialize Git repository
- Create comprehensive .gitignore for Python projects
- Include ignores for: __pycache__, venv/, .env, *.log, data/db/, etc.

After setup, create a simple test to verify everything works:
- Create src/config/settings.py with basic Settings class
- Create a simple test script that imports and prints settings

Please do all of this automatically - create all files, install dependencies, set up Git, everything.
```

**Paste this prompt into Cursor chat and press Enter**

**What Cursor AI Will Do:**
- ✅ Create all folder structure
- ✅ Initialize Git repository
- ✅ Create .gitignore
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .cursorrules file
- ✅ Create requirements.txt
- ✅ Create initial project files
- ✅ Set up basic configuration

**Time:** 5-10 minutes (AI working)

---

## 🚀 STEP 4: Verify Setup

### Check What Cursor Created:

**In Cursor Terminal:**
```bash
# Check virtual environment created
ls venv/  # Should show venv folder

# Check Python works
python --version  # Should show Python 3.12.x (or 3.11+)

# Check dependencies installed
pip list  # Should show FastAPI, Pydantic, etc.

# Check Git initialized
git status  # Should show Git repository

# Check structure created
ls src/  # Should show core/, config/, voice/, etc.
```

**If Everything Looks Good:**
- ✅ Project structure created
- ✅ Dependencies installed
- ✅ Git initialized
- ✅ Virtual environment active

**Time:** 2 minutes

---

## 🚀 STEP 5: Start Building with Prompts

### Now Use Your Prompts!

1. **Open `ZEMA-CURSOR-PROMPTS.md`**
   - Keep this file open in Cursor
   - This is your coding guide

2. **Find SETUP-002 Prompt:**
   - Navigate to "SETUP-002: Configuration System"
   - Copy the entire prompt block

3. **Use Cursor Chat:**
   - Press `Ctrl+L` (or `Cmd+L`)
   - Paste SETUP-002 prompt
   - Generate code

4. **Test It Works:**
   ```bash
   python -c "from src.config.settings import Settings; print(Settings())"
   ```

5. **Commit Changes:**
   ```bash
   git add .
   git commit -m "feat: SETUP-002 - Configuration system"
   ```

**Time:** 15 minutes per prompt

---

## 🎯 Complete Workflow

### Daily Development Pattern:

```
1. Open Cursor IDE → Open zema-ai folder
2. Open ZEMA-CURSOR-PROMPTS.md
3. Find next prompt (e.g., SETUP-003)
4. Copy prompt → Paste in Cursor chat
5. Review generated code → Test
6. Commit → git commit -m "feat: PROMPT-ID - Description"
7. Move to next prompt → Repeat
```

---

## 📋 What Cursor AI Should Create

### Expected Structure After Setup:

```
zema-ai/
├── src/
│   ├── core/
│   ├── config/
│   │   └── settings.py  (basic)
│   ├── voice/
│   ├── vision/
│   ├── ai/
│   ├── tools/
│   ├── api/
│   └── utils/
├── scripts/
├── tests/
├── data/
│   ├── config/
│   ├── logs/
│   └── db/
├── venv/              ✅ Created by Cursor
├── .git/              ✅ Created by Cursor
├── .gitignore         ✅ Created by Cursor
├── .cursorrules       ✅ Created by Cursor
├── requirements.txt    ✅ Created by Cursor
└── README.md          ✅ Created by Cursor
```

---

## ✅ Verification Checklist

### After Cursor AI Setup:

- [ ] `venv/` folder exists
- [ ] `.git/` folder exists
- [ ] `.gitignore` file exists
- [ ] `.cursorrules` file exists
- [ ] `requirements.txt` exists
- [ ] `src/` folder structure created
- [ ] `scripts/` folder exists
- [ ] `tests/` folder exists
- [ ] `data/` folder structure created
- [ ] Python dependencies installed (`pip list` shows packages)
- [ ] Git initialized (`git status` works)

**If all checked:** ✅ Ready to build!

---

## 🚨 Troubleshooting

### Issue: Cursor AI Didn't Create Everything

**Solution:**
- Ask Cursor: "Please create the missing folders/files"
- Or copy specific parts of the prompt separately

### Issue: Dependencies Not Installed

**Solution:**
```bash
# Check if venv is active
which python  # Should show venv path

# If not active, activate:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install manually if needed
pip install -r requirements.txt
```

### Issue: Python Not Found

**Solution:**
- Install Python 3.11+ from python.org
- Restart Cursor IDE
- Tell Cursor: "Python is installed at [path]"

---

## 🎯 Next Steps After Setup

### Start Building:

1. **SETUP-002:** Configuration System
   - Copy prompt from `ZEMA-CURSOR-PROMPTS.md`
   - Generate in Cursor
   - Test and commit

2. **SETUP-003:** Logging System
   - Copy prompt
   - Generate
   - Test and commit

3. **Continue Sequentially:**
   - Follow prompts in order
   - Test each before moving on
   - Commit after each working feature

---

## 💡 Pro Tips

### For Cursor AI Setup:

1. **Be Specific:**
   - Tell Cursor exactly what you need
   - Include all requirements in prompt

2. **Review Generated Code:**
   - Always check what Cursor created
   - Test before moving on

3. **Iterate if Needed:**
   - If something missing, ask Cursor to add it
   - Cursor can fix issues

4. **Use Context:**
   - Reference `ZEMA-CURSOR-PROMPTS.md` when asking Cursor
   - Say "@ZEMA-CURSOR-PROMPTS.md" to give context

---

## 🎉 Summary

**Your Simple Process:**

1. ✅ Create folder `zema-ai`
2. ✅ Open folder in Cursor IDE
3. ✅ Paste comprehensive setup prompt
4. ✅ Cursor AI sets up everything
5. ✅ Verify setup works
6. ✅ Start building with prompts

**That's it!** No manual Git, no manual Python setup, no manual dependency installation - Cursor AI does it all!

**Time:** 15 minutes total (mostly waiting for AI)

**You're ready!** Start with Step 1 above. 🚀

---

## 📚 Additional Resources

### For Windows 11 Setup:
- **See:** `ZEMA-WINDOWS-UBUNTU-MIGRATION.md` Part 1
- **Covers:** Python 3.12 installation, Git setup, Cursor configuration

### For Ubuntu Migration:
- **See:** `ZEMA-WINDOWS-UBUNTU-MIGRATION.md` Part 2
- **Covers:** Migrating project from Windows to Ubuntu mini PC

### For Senior Dev/DevOps:
- **See:** `ZEMA-SENIOR-DEV-DEVOPS.md`
- **Covers:** CI/CD, Docker, monitoring, security best practices
