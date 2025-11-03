# Auto-Commit Workflow Guide

## Overview

After completing every task, automatically commit and push changes to GitHub.

## Quick Usage

```bash
# After completing a task
python scripts/auto_commit.py "task description"

# Examples:
python scripts/auto_commit.py "Added configuration system"
python scripts/auto_commit.py "Implemented voice module"
python scripts/auto_commit.py "Fixed bug in API endpoint"
```

## What It Does

1. **Checks for changes** - Verifies there are uncommitted changes
2. **Stages all files** - Runs `git add .`
3. **Creates commit** - With formatted message: `feat: task description - timestamp`
4. **Pushes to GitHub** - Automatically pushes to `origin/main`

## Commit Message Format

The script automatically formats commit messages:
- `feat: task description - YYYY-MM-DD HH:MM:SS`

Examples:
- `feat: Added configuration system - 2025-01-15 14:30:00`
- `feat: Implemented voice module - 2025-01-15 14:45:00`
- `fix: Fixed bug in API endpoint - 2025-01-15 15:00:00`

## Integration with Cursor AI

The `.cursorrules` file includes instructions for Cursor AI to:
1. Run the auto-commit script after completing tasks
2. Use descriptive commit messages
3. Ensure all changes are pushed to GitHub

## Manual Alternative

If auto-commit script doesn't work, use manual commands:

```bash
git add .
git commit -m "feat: task description"
git push origin main
```

## Troubleshooting

### Git Not Found
- Install Git: https://git-scm.com/downloads
- Or add to PATH: `$env:Path += ';C:\Program Files\Git\cmd'`

### Authentication Failed
- Use GitHub CLI: `gh auth login`
- Or create Personal Access Token: https://github.com/settings/tokens

### Push Failed
- Check internet connection
- Verify GitHub credentials
- Check if repository exists: https://github.com/AIHUBMIND/zema-ai

