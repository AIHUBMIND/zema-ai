#!/usr/bin/env python3
"""Move all ZEMA markdown files from Downloads to docs/guides/ folder."""
import shutil
from pathlib import Path

downloads_dir = Path("C:/Users/abrah/Downloads")
docs_guides_dir = Path("docs/guides")

# Create guides folder
docs_guides_dir.mkdir(parents=True, exist_ok=True)

# Find all ZEMA-*.md files
zema_files = sorted(downloads_dir.glob("ZEMA-*.md"))

print(f"Moving ZEMA files to docs/guides/...\n")

moved = []
skipped = []
errors = []

for source_file in zema_files:
    # Keep the original filename
    target_file = docs_guides_dir / source_file.name
    
    try:
        shutil.copy2(str(source_file), str(target_file))
        moved.append(source_file.name)
        print(f"✓ Moved: {source_file.name}")
    except Exception as e:
        errors.append((source_file.name, str(e)))
        print(f"✗ Error: {source_file.name} - {e}")

print(f"\n✅ Summary:")
print(f"  Successfully moved: {len(moved)} files")
print(f"  Errors: {len(errors)} files")

if moved:
    print(f"\n📁 Files now in docs/guides/:")
    for f in sorted(moved):
        print(f"  - {f}")

if errors:
    print(f"\n⚠ Errors:")
    for f, e in errors:
        print(f"  - {f}: {e}")

