#!/usr/bin/env python3
"""Script to organize markdown documentation files."""
import os
import shutil
from pathlib import Path

# Create guides directory
guides_dir = Path("docs/guides")
guides_dir.mkdir(exist_ok=True)

# Files to move
files_to_move = [
    ("QUICK_START.md", "docs/guides/QUICK_START.md"),
    ("docs/ACTIVATION.md", "docs/guides/ACTIVATION.md"),
    ("docs/ADDING_PIP_TO_PATH.md", "docs/guides/ADDING_PIP_TO_PATH.md"),
    ("docs/PIP_FIXED.md", "docs/guides/PIP_FIXED.md"),
    ("docs/WHY_ACTIVATION.md", "docs/guides/WHY_ACTIVATION.md"),
    ("docs/WSL_INFO.md", "docs/guides/WSL_INFO.md"),
    ("docs/SETUP.md", "docs/guides/SETUP.md"),
]

moved = []
for source, dest in files_to_move:
    source_path = Path(source)
    dest_path = Path(dest)
    if source_path.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(dest_path))
        moved.append(source)
        print(f"✓ Moved: {source} → {dest}")
    else:
        print(f"⚠ Skipped (not found): {source}")

print(f"\n✅ Moved {len(moved)} files to docs/guides/")

