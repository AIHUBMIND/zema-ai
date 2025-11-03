#!/usr/bin/env python3
"""Comprehensive STEP 4 verification script."""
import sys
from pathlib import Path
import subprocess

def print_section(title):
    """Print section header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def check_item(name, condition, details=""):
    """Check and print item status."""
    status = "✓" if condition else "✗"
    print(f"{status} {name}")
    if details:
        print(f"  {details}")

def main():
    """Run STEP 4 verification."""
    print_section("STEP 4: VERIFY SETUP")
    print("\nChecking all requirements from ZEMA-GETTING-STARTED.md...")
    
    # 1. Virtual Environment
    print_section("1. Virtual Environment")
    venv_exists = Path("venv").exists()
    venv_python = Path("venv/Scripts/python.exe")
    check_item("venv/ folder exists", venv_exists)
    
    if venv_exists:
        try:
            result = subprocess.run(
                [str(venv_python), "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                check_item("Python works", True, version)
            else:
                check_item("Python works", False)
        except Exception as e:
            check_item("Python works", False, str(e))
    
    # 2. Dependencies
    print_section("2. Dependencies")
    required_packages = ["fastapi", "pydantic", "sqlalchemy", "uvicorn", "httpx"]
    
    try:
        result = subprocess.run(
            [str(venv_python), "-m", "pip", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        installed = result.stdout.lower()
        
        for pkg in required_packages:
            found = pkg.lower() in installed
            check_item(f"{pkg} installed", found)
    except Exception as e:
        print(f"✗ Could not check packages: {e}")
    
    # 3. Git
    print_section("3. Git Repository")
    git_dir = Path(".git")
    git_config = Path(".git/config")
    
    check_item("Git initialized", git_dir.exists())
    
    if git_config.exists():
        config_content = git_config.read_text()
        has_remote = "[remote" in config_content
        check_item("Remote configured", has_remote)
        if has_remote and "github.com/AIHUBMIND/zema-ai" in config_content:
            check_item("GitHub remote correct", True, "https://github.com/AIHUBMIND/zema-ai.git")
    
    # 4. Project Structure
    print_section("4. Project Structure")
    
    required_dirs = {
        "src/": ["core", "config", "voice", "vision", "ai", "tools", "api", "utils"],
        "data/": ["config", "logs", "db", "models", "backups"],
    }
    
    for base_dir, subdirs in required_dirs.items():
        base_path = Path(base_dir)
        check_item(f"{base_dir} exists", base_path.exists())
        
        if base_path.exists():
            for subdir in subdirs:
                subdir_path = base_path / subdir
                check_item(f"  {base_dir}{subdir}/", subdir_path.exists())
    
    check_item("scripts/ exists", Path("scripts").exists())
    check_item("tests/ exists", Path("tests").exists())
    
    # 5. Configuration Files
    print_section("5. Configuration Files")
    config_files = {
        ".gitignore": "Git ignore rules",
        ".cursorrules": "Cursor AI rules",
        "requirements.txt": "Python dependencies",
        "README.md": "Project README",
        "setup.py": "Setup script",
    }
    
    for filename, description in config_files.items():
        check_item(f"{filename} exists", Path(filename).exists(), description)
    
    # 6. Test Import
    print_section("6. Code Verification")
    try:
        # Use test_setup.py which properly sets up paths
        result = subprocess.run(
            [str(venv_python), "scripts/test_setup.py"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(Path.cwd())
        )
        if result.returncode == 0:
            check_item("Settings import works", True)
            # Show key lines from output
            for line in result.stdout.strip().split('\n'):
                if '✓' in line or '✅' in line:
                    print(f"  {line.strip()}")
        else:
            check_item("Settings import works", False)
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
    except Exception as e:
        check_item("Settings import works", False, str(e))
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    print("\n✅ All critical checks completed!")
    print("\nNext steps:")
    print("1. Review any items marked with ✗")
    print("2. If all checks pass, proceed to STEP 5")
    print("3. Start building with prompts from ZEMA-CURSOR-PROMPTS.md")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

