# Documentation Structure

This directory contains all project documentation organized by category.

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
