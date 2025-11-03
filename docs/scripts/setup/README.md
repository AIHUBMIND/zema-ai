# Setup Scripts Folder

## Purpose
The `scripts/setup/` folder contains scripts for initial project setup, verification, and GitHub configuration. These scripts help ensure the project is properly configured before development begins.

## Files in This Folder

### `verify_setup.py`
Comprehensive setup verification script. Checks all requirements from `ZEMA-GETTING-STARTED.md` including virtual environment, dependencies, Git, project structure, and configuration files.

### `verify_step4.py`
Specific verification for STEP 4 from the getting started guide. Runs detailed checks for virtual environment, Python packages, Git status, project structure, and code imports.

### `test_setup.py`
Simple test script to verify basic imports work. Tests that `Settings` can be imported and displays key configuration values.

### `connect_github.py`
Interactive script to connect local Git repository to GitHub. Handles remote configuration, branch naming, and initial push.

### `setup_github_remote.py`
Interactive GitHub setup script with step-by-step instructions. Helps users create GitHub repository and configure remote.

## Usage Pattern
These scripts are typically run during initial setup:
```bash
# Verify everything is set up correctly
python scripts/setup/verify_setup.py

# Test that imports work
python scripts/setup/test_setup.py

# Connect to GitHub
python scripts/setup/connect_github.py
```

## Integration
These scripts are referenced in:
- `ZEMA-GETTING-STARTED.md` - Setup guide
- `docs/setup/` - Setup documentation
- Initial project setup workflow

