# Scripts Folder Documentation

## Purpose
The `scripts/` folder contains utility scripts, setup scripts, maintenance tools, and development helpers. These scripts are not part of the main application code but support development, deployment, and maintenance tasks.

## Folder Structure

### `maintenance/`
Contains scripts for ongoing maintenance tasks:
- **Auto-commit**: Automated Git commits and pushes
- **Benchmark**: System performance benchmarking
- **Check compliance**: Code quality and rules compliance checking
- **Update docs**: Automated documentation updates
- **Check docs**: Prevent duplicate documentation files

### `setup/`
Contains scripts for initial project setup:
- **GitHub setup**: Configure GitHub remote repository
- **Verify setup**: Verify project setup is complete
- **Test setup**: Test that imports and basic functionality work

### `legacy/`
Contains old/organizational scripts that are no longer actively used but kept for reference:
- Documentation reorganization scripts
- Path configuration helpers
- Cleanup scripts

## Usage
These scripts are typically run from the project root directory:
```bash
python scripts/maintenance/benchmark.py
python scripts/setup/verify_setup.py
```

## Important Notes
- Scripts use Python 3.11+ features
- Some scripts require specific dependencies (e.g., `psutil` for benchmarking)
- Scripts should follow PEP 8 style guidelines
- All scripts should have proper error handling and logging

