#!/usr/bin/env python3
"""Reverse all document reorganization - restore original structure."""
import shutil
from pathlib import Path

# Files to move back to original locations
reversals = [
    # From getting-started/ back to root or docs/
    ("docs/getting-started/QUICK_START.md", "QUICK_START.md"),
    ("docs/getting-started/ACTIVATION.md", "docs/ACTIVATION.md"),
    
    # From setup/ back to docs/
    ("docs/setup/SETUP.md", "docs/SETUP.md"),
    ("docs/setup/WSL_INFO.md", "docs/WSL_INFO.md"),
    
    # From development/ back to docs/
    ("docs/development/WHY_ACTIVATION.md", "docs/WHY_ACTIVATION.md"),
    ("docs/development/ADDING_PIP_TO_PATH.md", "docs/ADDING_PIP_TO_PATH.md"),
    ("docs/development/PIP_FIXED.md", "docs/PIP_FIXED.md"),
    
    # From configuration/ back to docs/ (if I created it)
    ("docs/configuration/BOSGAME_P3_LITE.md", "docs/BOSGAME_P3_LITE.md"),
]

# Files to delete (from Downloads folder copies)
files_to_delete = [
    "docs/getting-started/GETTING_STARTED.md",
    "docs/getting-started/QUICK_REFERENCE.md",
    "docs/setup/WINDOWS_UBUNTU_MIGRATION.md",
    "docs/setup/TROUBLESHOOTING.md",
    "docs/development/LOCAL_DEVELOPMENT.md",
    "docs/development/LOCAL_DEVELOPMENT_DETAILED.md",
    "docs/development/SENIOR_DEV_DEVOPS.md",
    "docs/development/CURSOR_PROMPTS.md",
    "docs/development/IMPLEMENTATION.md",
    "docs/development/GESTURE_INTEGRATION.md",
    "docs/development/INFRASTRUCTURE.md",
    "docs/development/FILE_ORGANIZATION.md",
    "docs/development/CLEANUP_AND_CLARIFICATIONS.md",
    "docs/development/DOCUMENTATION_STATUS.md",
    "docs/configuration/BOSGAME_P3_LITE_CONFIG.md",
    "docs/configuration/MINI_PC_SETUP_GUIDE.md",
    "docs/configuration/RASPBERRY_PI_SETUP.md",
]

print("Reversing document reorganization...\n")

# Move files back
moved = []
for source, dest in reversals:
    source_path = Path(source)
    dest_path = Path(dest)
    if source_path.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(dest_path))
        moved.append((source, dest))
        print(f"✓ Moved back: {source_path.name} → {dest}")
    else:
        print(f"⚠ Not found: {source}")

# Delete files copied from Downloads
deleted = []
for file_path in files_to_delete:
    path = Path(file_path)
    if path.exists():
        path.unlink()
        deleted.append(file_path)
        print(f"✓ Deleted: {file_path}")

# Remove empty subfolders
folders_to_remove = [
    "docs/getting-started",
    "docs/setup",
    "docs/development",
    "docs/configuration",
]

for folder in folders_to_remove:
    folder_path = Path(folder)
    if folder_path.exists():
        try:
            folder_path.rmdir()
            print(f"✓ Removed empty folder: {folder}")
        except OSError:
            print(f"⚠ Folder not empty: {folder}")

# Restore original docs/README.md (simple version)
original_readme = """# Documentation

## Setup & Installation
- [SETUP.md](SETUP.md) - Platform-specific installation notes

## Development Environment
- [ACTIVATION.md](ACTIVATION.md) - How to activate virtual environment
- [WHY_ACTIVATION.md](WHY_ACTIVATION.md) - Understanding virtual environments
- [ADDING_PIP_TO_PATH.md](ADDING_PIP_TO_PATH.md) - Adding pip to Windows PATH
- [PIP_FIXED.md](PIP_FIXED.md) - Troubleshooting pip installation
- [WSL_INFO.md](WSL_INFO.md) - WSL information and setup

## Configuration
- [BOSGAME_P3_LITE.md](BOSGAME_P3_LITE.md) - BOSGAME P3 Lite configuration
"""

with open("docs/README.md", "w", encoding="utf-8") as f:
    f.write(original_readme)

print(f"\n✅ Reversal complete!")
print(f"  Moved back: {len(moved)} files")
print(f"  Deleted: {len(deleted)} files")
print(f"\n📁 Current structure:")
print("  docs/")
for f in sorted(Path("docs").glob("*.md")):
    print(f"    - {f.name}")

