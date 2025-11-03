#!/usr/bin/env python3
"""
SETUP-001 Verification Script
Checks if all required files and directories from SETUP-001 are present
"""

import os
from pathlib import Path
from typing import List, Tuple

def check_setup001() -> Tuple[bool, List[str]]:
    """Verify SETUP-001 completion"""
    issues = []
    base_path = Path(".")
    
    # Step 1: Root directory structure
    print("=" * 60)
    print("SETUP-001 Verification: Create Project Structure")
    print("=" * 60)
    
    # Step 2: Python package structure
    print("\n📁 Checking Python package structure...")
    src_dirs = [
        "src/core",
        "src/config",
        "src/voice",
        "src/vision",
        "src/ai",
        "src/tools",
        "src/api",
        "src/utils"
    ]
    
    for dir_path in src_dirs:
        if not Path(dir_path).exists():
            issues.append(f"❌ Missing directory: {dir_path}")
        elif not Path(dir_path, "__init__.py").exists():
            issues.append(f"❌ Missing __init__.py: {dir_path}/__init__.py")
        else:
            print(f"  ✅ {dir_path}")
    
    # Step 3: Data directory structure
    print("\n📁 Checking data directory structure...")
    data_dirs = [
        "data/config",
        "data/logs",
        "data/db",
        "data/models",
        "data/backups",
        "data/audio",
        "data/images",
        "data/knowledge",
        "data/exports"
    ]
    
    for dir_path in data_dirs:
        if not Path(dir_path).exists():
            issues.append(f"❌ Missing directory: {dir_path}")
        else:
            print(f"  ✅ {dir_path}")
    
    # Step 4: Test directory structure
    print("\n📁 Checking test directory structure...")
    test_dirs = [
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/hardware",
        "tests/fixtures"
    ]
    
    for dir_path in test_dirs:
        if not Path(dir_path).exists():
            issues.append(f"❌ Missing directory: {dir_path}")
        elif not Path(dir_path, "__init__.py").exists() and dir_path != "tests":
            issues.append(f"❌ Missing __init__.py: {dir_path}/__init__.py")
        else:
            print(f"  ✅ {dir_path}")
    
    # Check conftest.py
    if not Path("tests/conftest.py").exists():
        issues.append("❌ Missing tests/conftest.py")
    else:
        print("  ✅ tests/conftest.py")
    
    # Step 5: Scripts directory
    print("\n📁 Checking scripts directory...")
    required_scripts = [
        "scripts/__init__.py",
        "scripts/download_models.sh",
        "scripts/verify_hardware.py",
        "scripts/backup.sh",
        "scripts/cleanup.sh",
        "scripts/benchmark.py"
    ]
    
    for script_path in required_scripts:
        if not Path(script_path).exists():
            # Check if it's in a subdirectory
            script_name = Path(script_path).name
            found = False
            for root, dirs, files in os.walk("scripts"):
                if script_name in files:
                    found = True
                    print(f"  ⚠️  {script_path} found at {Path(root, script_name)}")
                    break
            if not found:
                issues.append(f"❌ Missing script: {script_path}")
        else:
            print(f"  ✅ {script_path}")
    
    # Step 6: Root files
    print("\n📄 Checking root files...")
    root_files = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "setup.py",
        "setup.sh"
    ]
    
    for file_path in root_files:
        if not Path(file_path).exists():
            issues.append(f"❌ Missing file: {file_path}")
        else:
            print(f"  ✅ {file_path}")
    
    # Step 7: Check .gitignore content
    if Path(".gitignore").exists():
        gitignore_content = Path(".gitignore").read_text()
        required_patterns = [
            "__pycache__/",
            "venv/",
            ".env",
            "data/db/*.db",
            "data/logs/*.log"
        ]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in gitignore_content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            issues.append(f"⚠️  .gitignore missing patterns: {', '.join(missing_patterns)}")
        else:
            print("  ✅ .gitignore has required patterns")
    
    # Step 8: Check requirements.txt dependencies
    if Path("requirements.txt").exists():
        req_content = Path("requirements.txt").read_text()
        required_deps = [
            "fastapi",
            "pydantic",
            "sqlalchemy",
            "pyaudio",
            "faster-whisper",
            "opencv-python-headless",
            "pytest"
        ]
        
        missing_deps = []
        for dep in required_deps:
            if dep.lower() not in req_content.lower():
                missing_deps.append(dep)
        
        if missing_deps:
            issues.append(f"⚠️  requirements.txt missing dependencies: {', '.join(missing_deps)}")
        else:
            print("  ✅ requirements.txt has required dependencies")
    
    # Step 9: Check README.md content
    if Path("README.md").exists():
        readme_content = Path("README.md").read_text()
        required_sections = [
            "Features",
            "Quick Start",
            "Installation"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section.lower() not in readme_content.lower():
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(f"⚠️  README.md missing sections: {', '.join(missing_sections)}")
        else:
            print("  ✅ README.md has required sections")
    
    # Step 10: Check pyproject.toml content
    if Path("pyproject.toml").exists():
        pyproject_content = Path("pyproject.toml").read_text()
        required_items = [
            "[build-system]",
            "[project]",
            "name = \"zema-ai\"",
            "requires-python = \">=3.11\""
        ]
        
        missing_items = []
        for item in required_items:
            if item not in pyproject_content:
                missing_items.append(item)
        
        if missing_items:
            issues.append(f"⚠️  pyproject.toml missing items: {', '.join(missing_items)}")
        else:
            print("  ✅ pyproject.toml has required configuration")
    
    # Step 11: Check .env.example
    if not Path(".env.example").exists():
        issues.append("❌ Missing .env.example file")
    else:
        env_example = Path(".env.example").read_text()
        required_vars = [
            "ENVIRONMENT",
            "LOG_LEVEL",
            "DASHBOARD_PORT",
            "PRIVACY_MODE",
            "LLM_MODEL"
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in env_example:
                missing_vars.append(var)
        
        if missing_vars:
            issues.append(f"⚠️  .env.example missing variables: {', '.join(missing_vars)}")
        else:
            print("  ✅ .env.example has required variables")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} issue(s):\n")
        for issue in issues:
            print(f"  {issue}")
        return False, issues
    else:
        print("\n✅ SETUP-001 is COMPLETE!")
        print("\nAll required files and directories are present.")
        print("Structure is ready for development.")
        return True, []

if __name__ == "__main__":
    success, issues = check_setup001()
    exit(0 if success else 1)

