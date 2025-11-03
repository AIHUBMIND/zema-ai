#!/usr/bin/env python3
"""Reorganize documentation into proper categories."""
import shutil
from pathlib import Path

# Create organized folder structure
folders = {
    "docs/getting-started": [],
    "docs/setup": [],
    "docs/development": [],
    "docs/configuration": [],
}

# Map files to categories
file_mapping = {
    "docs/guides/QUICK_START.md": "docs/getting-started/",
    "docs/guides/ACTIVATION.md": "docs/getting-started/",
    "docs/guides/SETUP.md": "docs/setup/",
    "docs/guides/WSL_INFO.md": "docs/setup/",
    "docs/guides/WHY_ACTIVATION.md": "docs/development/",
    "docs/guides/ADDING_PIP_TO_PATH.md": "docs/development/",
    "docs/guides/PIP_FIXED.md": "docs/development/",
}

# Create folders
for folder in folders.keys():
    Path(folder).mkdir(parents=True, exist_ok=True)

# Move files
moved = []
for source, dest in file_mapping.items():
    source_path = Path(source)
    dest_path = Path(dest) / source_path.name
    if source_path.exists():
        shutil.move(str(source_path), str(dest_path))
        moved.append((source, str(dest_path)))
        print(f"✓ Moved: {source_path.name} → {dest}")
    else:
        print(f"⚠ Skipped (not found): {source}")

print(f"\n✅ Moved {len(moved)} files")
print("\nNew structure:")
for folder in folders.keys():
    files = list(Path(folder).glob("*.md"))
    if files:
        print(f"\n{folder}/")
        for f in files:
            print(f"  - {f.name}")

