#!/usr/bin/env python3
"""Review and delete non-relevant files from docs/guides/ folder."""
from pathlib import Path

# Files to DELETE (not relevant for the project)
files_to_delete = [
    "ZEMA-RASPBERRY-PI-SETUP-GUIDE.md",  # ❌ Using BOSGAME P3 Lite, not Raspberry Pi
    "ZEMA-INFRASTRUCTURE.md",             # ❌ Raspberry Pi infrastructure, replaced by BOSGAME config
    "ZEMA-DOCUMENTATION-STATUS.md",       # ❌ Meta document about documentation status
    "ZEMA-FILE-ORGANIZATION.md",          # ❌ About organizing docs, not project content
    "ZEMA-CLEANUP-AND-CLARIFICATIONS.md", # ❌ One-time cleanup guide, not ongoing content
]

# Files to KEEP (relevant for project)
files_to_keep = [
    "ZEMA-GETTING-STARTED.md",            # ✅ Getting started guide
    "ZEMA-CURSOR-PROMPTS.md",              # ✅ Coding prompts
    "ZEMA-PRD-PERSONAL (1).md",            # ✅ Product Requirements Document
    "ZEMA-IMPLEMENTATION.md",              # ✅ Implementation guide
    "ZEMA-BOSGAME-P3-LITE-CONFIG.md",     # ✅ Actual hardware config
    "ZEMA-LOCAL-DEVELOPMENT.md",          # ✅ Local development guide
    "ZEMA-WINDOWS-UBUNTU-MIGRATION.md",   # ✅ Migration guide
    "ZEMA-SENIOR-DEV-DEVOPS.md",          # ✅ DevOps best practices
    "ZEMA-TROUBLESHOOTING.md",            # ✅ Troubleshooting guide
    "ZEMA-QUICK-REFERENCE.md",            # ✅ Quick reference
    "ZEMA-GESTURE-INTEGRATION.md",        # ✅ Camera integration
    "ZEMA-MINI-PC-SETUP-GUIDE.md",       # ✅ General mini PC guide (reference)
]

guides_dir = Path("docs/guides")

print("Reviewing files in docs/guides/...\n")

deleted = []
not_found = []

for filename in files_to_delete:
    file_path = guides_dir / filename
    if file_path.exists():
        file_path.unlink()
        deleted.append(filename)
        print(f"✓ Deleted: {filename}")
    else:
        not_found.append(filename)
        print(f"⚠ Not found: {filename}")

print(f"\n✅ Summary:")
print(f"  Deleted: {len(deleted)} files")
print(f"  Keeping: {len(files_to_keep)} relevant files")

if deleted:
    print(f"\n📁 Remaining files in docs/guides/:")
    remaining = sorted([f.name for f in guides_dir.glob("*.md")])
    for f in remaining:
        print(f"  ✓ {f}")

