#!/usr/bin/env python3
"""Quick activation helper script."""
import sys
import os
from pathlib import Path

venv_path = Path(__file__).parent.parent / "venv"

if sys.platform == "win32":
    if venv_path.exists():
        print("=" * 60)
        print("Virtual Environment Activation Instructions")
        print("=" * 60)
        print("\nPowerShell:")
        print("  .\\venv\\Scripts\\Activate.ps1")
        print("\nCommand Prompt:")
        print("  venv\\Scripts\\activate.bat")
        print("\nGit Bash:")
        print("  source venv/Scripts/activate")
        print("\n" + "=" * 60)
        print("\nOr use pip directly without activation:")
        print("  .\\venv\\Scripts\\python.exe -m pip list")
        print("\n" + "=" * 60)
    else:
        print("Virtual environment not found at:", venv_path)
else:
    print("source venv/bin/activate")

