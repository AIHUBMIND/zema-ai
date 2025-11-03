#!/usr/bin/env python3
"""Organize all ZEMA markdown files from Downloads into docs structure."""
import shutil
from pathlib import Path
from typing import Dict, Tuple

# Define file mappings: (source_filename, target_folder, target_filename)
file_mappings: Dict[str, Tuple[str, str]] = {
    # Getting Started
    "ZEMA-GETTING-STARTED.md": ("getting-started", "GETTING_STARTED.md"),
    "ZEMA-QUICK-REFERENCE.md": ("getting-started", "QUICK_REFERENCE.md"),
    
    # Configuration
    "ZEMA-BOSGAME-P3-LITE-CONFIG.md": ("configuration", "BOSGAME_P3_LITE_CONFIG.md"),
    "ZEMA-MINI-PC-SETUP-GUIDE.md": ("configuration", "MINI_PC_SETUP_GUIDE.md"),
    "ZEMA-RASPBERRY-PI-SETUP-GUIDE.md": ("configuration", "RASPBERRY_PI_SETUP.md"),
    
    # Development
    "ZEMA-LOCAL-DEVELOPMENT.md": ("development", "LOCAL_DEVELOPMENT_DETAILED.md"),
    "ZEMA-SENIOR-DEV-DEVOPS.md": ("development", "SENIOR_DEV_DEVOPS.md"),
    "ZEMA-CURSOR-PROMPTS.md": ("development", "CURSOR_PROMPTS.md"),
    "ZEMA-IMPLEMENTATION.md": ("development", "IMPLEMENTATION.md"),
    "ZEMA-GESTURE-INTEGRATION.md": ("development", "GESTURE_INTEGRATION.md"),
    "ZEMA-INFRASTRUCTURE.md": ("development", "INFRASTRUCTURE.md"),
    "ZEMA-FILE-ORGANIZATION.md": ("development", "FILE_ORGANIZATION.md"),
    "ZEMA-CLEANUP-AND-CLARIFICATIONS.md": ("development", "CLEANUP_AND_CLARIFICATIONS.md"),
    "ZEMA-DOCUMENTATION-STATUS.md": ("development", "DOCUMENTATION_STATUS.md"),
    
    # Setup
    "ZEMA-WINDOWS-UBUNTU-MIGRATION.md": ("setup", "WINDOWS_UBUNTU_MIGRATION.md"),
    "ZEMA-TROUBLESHOOTING.md": ("setup", "TROUBLESHOOTING.md"),
}

downloads_dir = Path("C:/Users/abrah/Downloads")
docs_dir = Path("docs")

# Create all necessary folders
for folder in set(folder for folder, _ in file_mappings.values()):
    (docs_dir / folder).mkdir(parents=True, exist_ok=True)

# Move files
moved = []
skipped = []
errors = []

for source_name, (target_folder, target_name) in file_mappings.items():
    source_path = downloads_dir / source_name
    target_path = docs_dir / target_folder / target_name
    
    if source_path.exists():
        try:
            shutil.copy2(str(source_path), str(target_path))
            moved.append((source_name, str(target_path)))
            print(f"✓ Copied: {source_name} → {target_path.relative_to('docs')}")
        except Exception as e:
            errors.append((source_name, str(e)))
            print(f"✗ Error copying {source_name}: {e}")
    else:
        skipped.append(source_name)
        print(f"⚠ Skipped (not found): {source_name}")

print(f"\n✅ Summary:")
print(f"  Copied: {len(moved)} files")
print(f"  Skipped: {len(skipped)} files")
print(f"  Errors: {len(errors)} files")

if skipped:
    print(f"\n⚠ Files not found in Downloads:")
    for f in skipped:
        print(f"  - {f}")

if errors:
    print(f"\n✗ Errors:")
    for f, e in errors:
        print(f"  - {f}: {e}")

# Show final structure
print(f"\n📁 Final structure:")
for folder in sorted(set(folder for folder, _ in file_mappings.values())):
    files = list((docs_dir / folder).glob("*.md"))
    if files:
        print(f"\n  docs/{folder}/")
        for f in sorted(files):
            print(f"    - {f.name}")

