#!/usr/bin/env python3
"""Remove empty guides folder."""
from pathlib import Path
import shutil

guides_dir = Path("docs/guides")
if guides_dir.exists():
    if not any(guides_dir.iterdir()):
        shutil.rmtree(guides_dir)
        print("✓ Removed empty guides folder")
    else:
        print("⚠ Guides folder not empty, keeping it")

