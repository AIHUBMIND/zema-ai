#!/usr/bin/env python3
"""Comprehensive setup verification script based on ZEMA-GETTING-STARTED.md checklist."""
import sys
from pathlib import Path
import subprocess

def check_file(path: Path, name: str) -> tuple[bool, str]:
    """Check if file exists."""
    if path.exists():
        return True, f"✓ {name} exists"
    return False, f"✗ {name} MISSING"

def check_dir(path: Path, name: str) -> tuple[bool, str]:
    """Check if directory exists."""
    if path.exists() and path.is_dir():
        # Check if it has expected subdirectories/files
        items = list(path.iterdir())
        return True, f"✓ {name} exists ({len(items)} items)"
    return False, f"✗ {name} MISSING"

def check_python_packages() -> tuple[bool, list[str]]:
    """Check if required Python packages are installed."""
    required = [
        "fastapi",
        "pydantic",
        "sqlalchemy",
        "uvicorn",
        "httpx",
        "aiosqlite",
        "aiofiles",
        "structlog",
    ]
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        installed = result.stdout.lower()
        
        missing = []
        for pkg in required:
            if pkg.lower() not in installed:
                missing.append(pkg)
        
        if missing:
            return False, missing
        return True, []
    except Exception as e:
        return False, [f"Error checking packages: {e}"]

def check_git() -> tuple[bool, str]:
    """Check if Git is initialized."""
    git_dir = Path(".git")
    git_config = Path(".git/config")
    
    if git_dir.exists():
        # Check if remote is configured
        if git_config.exists():
            config_content = git_config.read_text()
            if "[remote" in config_content:
                return True, "✓ Git initialized with remote configured"
            else:
                return True, "✓ Git initialized (local only - remote not configured)"
        return True, "✓ Git initialized (.git/ folder exists)"
    return False, "✗ Git NOT initialized"

def check_src_structure() -> tuple[bool, list[str]]:
    """Check src/ folder structure."""
    expected_dirs = [
        "core",
        "config",
        "voice",
        "vision",
        "ai",
        "tools",
        "api",
        "utils",
    ]
    
    src_path = Path("src")
    if not src_path.exists():
        return False, ["✗ src/ folder MISSING"]
    
    missing = []
    for dir_name in expected_dirs:
        dir_path = src_path / dir_name
        if not dir_path.exists():
            missing.append(f"✗ src/{dir_name}/ MISSING")
        elif not (dir_path / "__init__.py").exists():
            missing.append(f"⚠ src/{dir_name}/__init__.py MISSING")
    
    if missing:
        return False, missing
    return True, ["✓ All src/ subdirectories exist"]

def check_data_structure() -> tuple[bool, list[str]]:
    """Check data/ folder structure."""
    expected_dirs = [
        "config",
        "logs",
        "db",
        "models",
        "backups",
    ]
    
    data_path = Path("data")
    if not data_path.exists():
        return False, ["✗ data/ folder MISSING"]
    
    missing = []
    for dir_name in expected_dirs:
        dir_path = data_path / dir_name
        if not dir_path.exists():
            missing.append(f"✗ data/{dir_name}/ MISSING")
    
    if missing:
        return False, missing
    return True, ["✓ All data/ subdirectories exist"]

def main():
    """Run comprehensive verification."""
    print("=" * 60)
    print("ZEMA AI SETUP VERIFICATION")
    print("Based on ZEMA-GETTING-STARTED.md STEP 3 Checklist")
    print("=" * 60)
    print()
    
    checks = []
    
    # Basic structure checks
    print("📁 STRUCTURE CHECK:")
    print("-" * 60)
    
    checks.append(check_dir(Path("venv"), "venv/"))
    checks.append(check_dir(Path(".git"), ".git/"))
    checks.append(check_file(Path(".gitignore"), ".gitignore"))
    checks.append(check_file(Path(".cursorrules"), ".cursorrules"))
    checks.append(check_file(Path("requirements.txt"), "requirements.txt"))
    checks.append(check_dir(Path("src"), "src/"))
    checks.append(check_dir(Path("scripts"), "scripts/"))
    checks.append(check_dir(Path("tests"), "tests/"))
    checks.append(check_dir(Path("data"), "data/"))
    
    for success, message in checks:
        print(f"  {message}")
    
    print()
    
    # Detailed structure checks
    print("📂 DETAILED STRUCTURE CHECK:")
    print("-" * 60)
    
    src_check, src_messages = check_src_structure()
    for msg in src_messages:
        print(f"  {msg}")
    
    data_check, data_messages = check_data_structure()
    for msg in data_messages:
        print(f"  {msg}")
    
    print()
    
    # Python environment check
    print("🐍 PYTHON ENVIRONMENT CHECK:")
    print("-" * 60)
    print(f"  Python version: {sys.version.split()[0]}")
    print(f"  Python path: {sys.executable}")
    
    # Check packages
    pkgs_ok, pkgs_missing = check_python_packages()
    if pkgs_ok:
        print("  ✓ Required packages installed")
    else:
        print("  ✗ Missing packages:")
        for pkg in pkgs_missing:
            print(f"    - {pkg}")
    
    print()
    
    # Git check
    print("🔧 GIT CHECK:")
    print("-" * 60)
    git_ok, git_msg = check_git()
    print(f"  {git_msg}")
    
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY:")
    print("-" * 60)
    
    basic_checks_passed = sum(1 for s, _ in checks if s)
    total_basic_checks = len(checks)
    
    all_passed = (
        basic_checks_passed == total_basic_checks and
        src_check and
        data_check and
        pkgs_ok and
        git_ok
    )
    
    print(f"  Basic structure: {basic_checks_passed}/{total_basic_checks} checks passed")
    print(f"  src/ structure: {'✓ PASS' if src_check else '✗ FAIL'}")
    print(f"  data/ structure: {'✓ PASS' if data_check else '✗ FAIL'}")
    print(f"  Python packages: {'✓ PASS' if pkgs_ok else '✗ FAIL'}")
    print(f"  Git setup: {'✓ PASS' if git_ok else '✗ FAIL'}")
    print()
    
    if all_passed:
        print("✅ ALL CHECKS PASSED - Setup is complete!")
        print("   You're ready to start building with prompts from ZEMA-CURSOR-PROMPTS.md")
    else:
        print("⚠️  SOME CHECKS FAILED - Review items above")
        print("   Fix missing items before proceeding")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

