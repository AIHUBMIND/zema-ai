# Documentation Structure Guide

## Overview
This documentation structure mirrors the project's folder hierarchy. Each Python file has a corresponding markdown documentation file in the `docs/` folder, following the same directory structure.

## Structure Pattern

### File Documentation
For each Python file `path/to/file.py`, there is a corresponding documentation file:
```
path/to/file.py  →  docs/path/to/file.md
```

### Folder Documentation
For each folder, there is a `README.md` file explaining:
- What the folder contains
- Purpose of the folder
- How files work together
- Key concepts

## Documentation Locations

### Root Level
- `docs/setup.md` - Documentation for `setup.py`

### Scripts Folder
- `docs/scripts/README.md` - Scripts folder overview
- `docs/scripts/maintenance/README.md` - Maintenance scripts overview
- `docs/scripts/maintenance/benchmark.md` - `benchmark.py` documentation
- `docs/scripts/maintenance/auto_commit.md` - `auto_commit.py` documentation
- `docs/scripts/maintenance/check_rules_compliance.md` - `check_rules_compliance.py` documentation
- `docs/scripts/maintenance/update_docs.md` - `update_docs.py` documentation
- `docs/scripts/maintenance/check_docs.md` - `check_docs.py` documentation
- `docs/scripts/maintenance/check_git_status.md` - `check_git_status.py` documentation
- `docs/scripts/setup/README.md` - Setup scripts overview
- `docs/scripts/organize_project.md` - `organize_project.py` documentation

### Source Code Folder
- `docs/src/README.md` - Source code overview
- `docs/src/main.md` - `main.py` documentation
- `docs/src/core/README.md` - Core module overview
- `docs/src/core/orchestrator.md` - `orchestrator.py` documentation
- `docs/src/config/README.md` - Config module overview
- `docs/src/config/settings.md` - `settings.py` documentation
- `docs/src/voice/README.md` - Voice module overview
- `docs/src/vision/README.md` - Vision module overview
- `docs/src/ai/README.md` - AI module overview
- `docs/src/tools/README.md` - Tools module overview
- `docs/src/api/README.md` - API module overview
- `docs/src/utils/README.md` - Utils module overview
- `docs/src/utils/logger.md` - `logger.py` documentation

### Tests Folder
- `docs/tests/README.md` - Tests folder overview

## How to Use This Documentation

### Finding File Documentation
1. Locate the Python file in the project
2. Find the corresponding `.md` file in `docs/` following the same path
3. Example: `scripts/maintenance/benchmark.py` → `docs/scripts/maintenance/benchmark.md`

### Understanding a Folder
1. Read the folder's `README.md` file
2. This explains the folder's purpose and contents
3. Example: `docs/src/core/README.md` explains the core module

### Understanding a File
1. Read the file's `.md` documentation
2. Each documentation includes:
   - File location
   - Purpose
   - Why it was created
   - How it works (detailed explanation)
   - Dependencies
   - Usage examples
   - Integration points

## Documentation Format

Each file documentation follows this structure:
1. **File Location** - Where the file is
2. **Purpose** - What the file does
3. **Why It Was Created** - Context and reasoning
4. **How It Works** - Detailed explanation of functionality
5. **Dependencies** - Required libraries/modules
6. **Usage** - How to use it
7. **Integration** - How it fits into the project

## Benefits of This Structure

1. **Easy to Find**: Mirror structure makes finding docs intuitive
2. **Comprehensive**: Every file has documentation
3. **Organized**: Folder READMEs provide context
4. **Beginner-Friendly**: Detailed explanations for each component
5. **Maintainable**: Easy to update when files change

## Adding New Documentation

When adding a new Python file:
1. Create corresponding `.md` file in `docs/` following the same path
2. Use the standard format (see examples above)
3. Update the folder's `README.md` if needed

## Related Documentation

- `docs/architecture/CODE_DOCUMENTATION.md` - Comprehensive code documentation (single file)
- `docs/architecture/ARCHITECTURE.md` - System architecture overview
- `docs/progress/PROJECT_PROGRESS.md` - Development progress tracking

