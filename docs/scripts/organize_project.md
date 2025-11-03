# organize_project.py Documentation

## File Location
`scripts/organize_project.py`

## Purpose
Reorganizes project files and documentation into proper subdirectories. Moves files from root and flat structures into organized folders.

## Why It Was Created
Initially, documentation and scripts were scattered. This script:
- Organizes documentation into logical folders
- Organizes scripts into categories
- Updates file references after reorganization
- Maintains clean project structure

## How It Works

### Main Class: `ProjectOrganizer`

#### `organize_all()`
**Purpose**: Main orchestration method
**How it works**:
1. Calls `organize_documentation()` - Moves docs to subfolders
2. Calls `organize_scripts()` - Moves scripts to subfolders
3. Calls `cleanup_root()` - Cleans root directory
4. Prints completion message

#### `organize_documentation()`
**Purpose**: Organizes documentation files
**How it works**:
1. Defines structure mapping:
   - `progress/` → Progress tracking files
   - `architecture/` → Architecture docs
   - `setup/` → Setup guides
   - `git/` → Git/GitHub docs
   - `hardware/` → Hardware config
   - `development/` → Dev progress
2. For each folder:
   - Creates folder if it doesn't exist
   - Moves files from source to target location
   - Skips if file already in place
   - Reports moved files and missing files
3. Prints summary of moved files

**File Mappings**:
- `PROJECT_PROGRESS.md` → `docs/progress/PROJECT_PROGRESS.md`
- `CHECKPOINT.md` → `docs/progress/CHECKPOINT.md`
- `ARCHITECTURE.md` → `docs/architecture/ARCHITECTURE.md`
- `SETUP.md` → `docs/setup/SETUP.md`
- And more...

#### `organize_scripts()`
**Purpose**: Organizes scripts into categories
**How it works**:
1. Defines script categories:
   - `setup/` → Setup scripts
   - `maintenance/` → Maintenance scripts
   - `development/` → Dev scripts
   - `legacy/` → Old/organizational scripts
2. For each category:
   - Creates folder if needed
   - Moves scripts from root `scripts/` to category folder
   - Reports moved and missing files
3. Prints summary

**Script Categories**:
- **setup**: `setup_github_remote.py`, `connect_github.py`, `test_setup.py`, `verify_setup.py`, `verify_step4.py`
- **maintenance**: `auto_commit.py`, `update_docs.py`, `check_rules_compliance.py`, `check_git_status.py`, `benchmark.py`
- **development**: `download_models.sh`
- **legacy**: Old reorganization scripts

#### `cleanup_root()`
**Purpose**: Cleans up root directory
**How it works**:
1. Defines files that should stay in root:
   - `README.md`, `requirements.txt`, `pyproject.toml`
   - `.gitignore`, `.cursorrules`, `.env.example`
   - `setup.py`, `setup.sh`
2. Checks for files that should be moved
3. Reports cleanup status

**Note**: Currently mostly a placeholder - files should already be moved by previous steps.

#### `update_references()`
**Purpose**: Updates file references in key files
**How it works**:
1. Updates `CHECKPOINT.md` references:
   - `docs/PROJECT_PROGRESS.md` → `docs/progress/PROJECT_PROGRESS.md`
   - `docs/CODE_DOCUMENTATION.md` → `docs/architecture/CODE_DOCUMENTATION.md`
2. Updates `PROJECT_PROGRESS.md` references
3. Updates `.cursorrules` references
4. Updates `scripts/update_docs.py` paths
5. Uses string replacement with `encoding='utf-8'`

**Why this matters**: After moving files, references break. This fixes them.

## Dependencies
- `shutil`: File moving operations
- `pathlib.Path`: Path handling
- `typing`: Type hints

## Usage
```bash
# From project root
python scripts/organize_project.py
```

## Output Example
```
============================================================
ORGANIZING PROJECT STRUCTURE
============================================================

📚 Organizing Documentation...

  📁 progress/ (Progress tracking and checkpoints)
    ✓ docs/PROJECT_PROGRESS.md → docs/progress/PROJECT_PROGRESS.md
    ✓ CHECKPOINT.md → docs/progress/CHECKPOINT.md

  📁 architecture/ (System architecture and code documentation)
    ✓ docs/ARCHITECTURE.md → docs/architecture/ARCHITECTURE.md
    ...

  📊 Moved 15 files

🔧 Organizing Scripts...
  📁 scripts/setup/ (Setup and installation scripts)
    ✓ setup_github_remote.py → scripts/setup/setup_github_remote.py
    ...

  📊 Moved 12 scripts

✅ PROJECT ORGANIZATION COMPLETE
```

## When to Use
- After initial project setup
- When restructuring project
- When cleaning up scattered files
- One-time reorganization task

## Important Notes
- **Backup first**: This script moves files, so backup before running
- **One-time use**: Designed for initial reorganization, not regular use
- **Updates references**: Automatically fixes broken file references
- **Safe**: Checks if files exist before moving, skips if already in place

## Related Scripts
- `scripts/legacy/reorganize_docs.py`: Old version (now in legacy)
- `scripts/legacy/organize_docs.py`: Older version
- `scripts/legacy/reverse_reorganization.py`: Undoes reorganization

## Future Enhancements
- Dry-run mode (show what would happen without doing it)
- Backup before moving
- More sophisticated reference updating
- Integration with Git for tracking moves

