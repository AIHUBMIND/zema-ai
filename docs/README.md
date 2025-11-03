# Documentation Structure

This directory contains all project documentation organized by category.

**Last Updated:** 2025-11-02  
**Note:** This file is updated/appended - do not create new structure documentation files.

---

## 📁 Directory Structure

```
docs/
├── progress/          # Progress tracking and checkpoints
│   ├── CHECKPOINT.md           # Quick resume point for new chats
│   └── PROJECT_PROGRESS.md     # Detailed progress tracker
│
├── architecture/      # System architecture and code documentation
│   ├── ARCHITECTURE.md         # High-level system architecture
│   ├── CODE_DOCUMENTATION.md  # Detailed file-by-file documentation
│   └── PROMPT_ANALYSIS_REPORT.md
│
├── setup/            # Setup and installation guides
│   ├── SETUP.md                # Platform-specific setup
│   ├── ACTIVATION.md           # Virtual environment activation
│   ├── WHY_ACTIVATION.md      # Understanding venv
│   ├── ADDING_PIP_TO_PATH.md  # Windows PATH setup
│   ├── PIP_FIXED.md           # Pip troubleshooting
│   ├── WSL_INFO.md            # WSL information
│   └── QUICK_START.md         # Quick start guide
│
├── git/              # Git and GitHub documentation
│   ├── GITHUB_SETUP.md        # GitHub repository setup
│   └── AUTO_COMMIT.md         # Auto-commit workflow
│
├── hardware/         # Hardware configuration
│   └── BOSGAME_P3_LITE.md     # BOSGAME P3 Lite setup
│
├── development/     # Development progress
│   └── ENHANCEMENT_PROGRESS.md
│
└── guides/          # Main project guides (unchanged)
    ├── ZEMA-CURSOR-PROMPTS.md    # ⭐ MOST IMPORTANT - 100+ prompts
    ├── ZEMA-GETTING-STARTED.md   # Getting started guide
    ├── ZEMA-IMPLEMENTATION.md    # Implementation guide
    └── ... (other guides)
```

## 📚 Quick Reference

### For New Chat Sessions
- **Checkpoint:** `docs/progress/CHECKPOINT.md` - Quick resume point
- **Progress:** `docs/progress/PROJECT_PROGRESS.md` - Detailed status

### For Understanding Code
- **Architecture:** `docs/architecture/ARCHITECTURE.md` - System design
- **Code Docs:** `docs/architecture/CODE_DOCUMENTATION.md` - File-by-file explanations

### For Setup
- **Quick Start:** `docs/setup/QUICK_START.md`
- **Detailed Setup:** `docs/setup/SETUP.md`

### For Development
- **Prompts:** `docs/guides/ZEMA-CURSOR-PROMPTS.md` - ⭐ Main development guide
- **Getting Started:** `docs/guides/ZEMA-GETTING-STARTED.md`

## 🔄 Auto-Update

Documentation files are automatically updated after each task completion:
- Progress tracking updates
- Code documentation updates
- Checkpoint updates

See `.cursorrules` for documentation update workflow.

---

## 📂 Project Structure Summary

**Status:** ✅ Fully Organized

### Root Files (Essential Only)
- `README.md` - Project overview
- `requirements.txt` - Dependencies
- `pyproject.toml` - Project config
- `.gitignore` - Git ignore rules
- `.cursorrules` - Cursor AI rules
- `.env.example` - Environment template
- `setup.py` - Setup script
- `setup.sh` - Linux setup

### Source Code (`src/`)
- `main.py` - Entry point
- `core/` - Core orchestrator
- `config/` - Configuration
- `voice/` - Voice I/O
- `vision/` - Computer vision
- `ai/` - LLM client
- `tools/` - Assistant tools
- `api/` - FastAPI server
- `utils/` - Utilities

### Scripts (`scripts/`)
- `setup/` - Setup scripts
- `maintenance/` - Maintenance scripts (auto_commit.py, update_docs.py)
- `development/` - Dev scripts
- `legacy/` - Old scripts (can be removed)

### Data (`data/`)
- `config/` - Configuration files
- `logs/` - Log files
- `db/` - Database files
- `models/` - AI models
- `audio/`, `images/`, `knowledge/`, `exports/`, `backups/`

### Tests (`tests/`)
- `unit/` - Unit tests
- `integration/` - Integration tests
- `hardware/` - Hardware tests

---

## ✅ Organization Benefits

1. **Easy Navigation** - Everything is categorized logically
2. **Clear Separation** - Setup, docs, scripts are separate
3. **Better Organization** - No more scattered files
4. **Easier Maintenance** - Know where everything is
5. **Cleaner Root** - Only essential files in root

---

## ⚠️ Important: Documentation Update Policy

**CRITICAL RULE:** When adding documentation:
- ✅ **APPEND/UPDATE** existing files instead of creating new ones
- ✅ Check if similar information exists in existing files
- ✅ Use appropriate existing file (progress, architecture, setup, etc.)
- ❌ **DO NOT** create new markdown files for similar content
- ❌ **DO NOT** duplicate information across multiple files

**Append to existing files:**
- Progress updates → `docs/progress/PROJECT_PROGRESS.md`
- Code documentation → `docs/architecture/CODE_DOCUMENTATION.md`
- Architecture changes → `docs/architecture/ARCHITECTURE.md`
- Setup notes → `docs/setup/` (appropriate file)
- Git workflow → `docs/git/` (appropriate file)

See `.cursorrules` for detailed documentation workflow.
