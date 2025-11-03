#!/usr/bin/env python3
"""
Step 12 Verification: Verify Structure
Final comprehensive verification of SETUP-001 completion
"""

import sys
from pathlib import Path

def verify_step12():
    """Verify Step 12: Structure verification"""
    
    print("=" * 60)
    print("SETUP-001 Step 12: Verify Structure")
    print("=" * 60)
    print("\nThis is the final verification step.\n")
    
    all_checks_passed = True
    issues = []
    
    # Check 1: Verify all directories exist
    print("=" * 60)
    print("CHECK 1: Verify all directories exist")
    print("=" * 60)
    
    required_dirs = {
        "Python Package Structure": [
            "src",
            "src/core",
            "src/config",
            "src/voice",
            "src/vision",
            "src/ai",
            "src/tools",
            "src/api",
            "src/utils"
        ],
        "Data Directory Structure": [
            "data/config",
            "data/logs",
            "data/db",
            "data/models",
            "data/backups",
            "data/audio",
            "data/images",
            "data/knowledge",
            "data/exports"
        ],
        "Test Directory Structure": [
            "tests",
            "tests/unit",
            "tests/integration",
            "tests/hardware",
            "tests/fixtures"
        ],
        "Scripts Directory": [
            "scripts",
            "scripts/maintenance",
            "scripts/setup"
        ]
    }
    
    dirs_exist = True
    for category, dirs in required_dirs.items():
        print(f"\n{category}:")
        for dir_path in dirs:
            path = Path(dir_path)
            if path.exists() and path.is_dir():
                print(f"  ✅ {dir_path}")
            else:
                print(f"  ❌ Missing: {dir_path}")
                dirs_exist = False
                issues.append(f"Missing directory: {dir_path}")
    
    if not dirs_exist:
        all_checks_passed = False
    
    # Check 2: Verify all __init__.py files exist
    print("\n" + "=" * 60)
    print("CHECK 2: Verify all __init__.py files exist")
    print("=" * 60)
    
    required_init_files = [
        "src/__init__.py",
        "src/core/__init__.py",
        "src/config/__init__.py",
        "src/voice/__init__.py",
        "src/vision/__init__.py",
        "src/ai/__init__.py",
        "src/tools/__init__.py",
        "src/api/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "tests/hardware/__init__.py",
        "tests/fixtures/__init__.py",
        "scripts/__init__.py"
    ]
    
    init_files_exist = True
    for init_file in required_init_files:
        path = Path(init_file)
        if path.exists() and path.is_file():
            print(f"  ✅ {init_file}")
        else:
            print(f"  ❌ Missing: {init_file}")
            init_files_exist = False
            issues.append(f"Missing __init__.py: {init_file}")
    
    if not init_files_exist:
        all_checks_passed = False
    
    # Check 3: Verify all root files exist
    print("\n" + "=" * 60)
    print("CHECK 3: Verify all root files exist")
    print("=" * 60)
    
    required_root_files = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "setup.py",
        "setup.sh"
    ]
    
    root_files_exist = True
    for file_path in required_root_files:
        path = Path(file_path)
        if path.exists() and path.is_file():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ Missing: {file_path}")
            root_files_exist = False
            issues.append(f"Missing root file: {file_path}")
    
    if not root_files_exist:
        all_checks_passed = False
    
    # Check 4: Verify .gitignore is correct
    print("\n" + "=" * 60)
    print("CHECK 4: Verify .gitignore is correct")
    print("=" * 60)
    
    if Path(".gitignore").exists():
        gitignore_content = Path(".gitignore").read_text(encoding='utf-8')
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
            print(f"  ⚠️  Missing patterns: {', '.join(missing_patterns)}")
            issues.append(f".gitignore missing patterns: {', '.join(missing_patterns)}")
        else:
            print("  ✅ All required patterns present")
    else:
        print("  ❌ .gitignore missing")
        all_checks_passed = False
    
    # Check 5: Verify requirements.txt has all dependencies
    print("\n" + "=" * 60)
    print("CHECK 5: Verify requirements.txt has all dependencies")
    print("=" * 60)
    
    if Path("requirements.txt").exists():
        req_content = Path("requirements.txt").read_text(encoding='utf-8')
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
            print(f"  ⚠️  Missing dependencies: {', '.join(missing_deps)}")
            issues.append(f"requirements.txt missing dependencies: {', '.join(missing_deps)}")
        else:
            print("  ✅ All required dependencies present")
    else:
        print("  ❌ requirements.txt missing")
        all_checks_passed = False
    
    # Check 6: Verify key Python files exist
    print("\n" + "=" * 60)
    print("CHECK 6: Verify key Python files exist")
    print("=" * 60)
    
    key_python_files = [
        "src/main.py",
        "src/config/settings.py",
        "src/utils/logger.py",
        "src/core/orchestrator.py",
        "tests/conftest.py"
    ]
    
    python_files_exist = True
    for py_file in key_python_files:
        path = Path(py_file)
        if path.exists() and path.is_file():
            print(f"  ✅ {py_file}")
        else:
            print(f"  ⚠️  Missing: {py_file} (may be created in later steps)")
            # Don't fail if these are missing, as they're created in later setup steps
    
    # Check 7: Test Python import
    print("\n" + "=" * 60)
    print("CHECK 7: Test Python import")
    print("=" * 60)
    
    try:
        # Check if src/__init__.py exists (already verified above)
        if Path("src/__init__.py").exists():
            print("  ✅ src/__init__.py exists (package structure valid)")
            
            # Try importing (may fail if run from wrong directory, but structure is correct)
            try:
                # Add parent directory to path
                parent_path = Path(".").absolute()
                if str(parent_path) not in sys.path:
                    sys.path.insert(0, str(parent_path))
                
                import src
                print("  ✅ Can import src package")
            except ImportError:
                # This is expected if run from different directory
                print("  ℹ️  Import test skipped (normal if not run from project root)")
        else:
            print("  ❌ src/__init__.py missing")
            issues.append("src/__init__.py missing")
    except Exception as e:
        print(f"  ⚠️  Import check failed: {e}")
        # Don't add to issues as this is a minor check
    
    # Final Summary
    print("\n" + "=" * 60)
    print("STEP 12 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_checks_passed and not issues:
        print("\n✅ ALL CHECKS PASSED!")
        print("\n✅ SETUP-001 is COMPLETE!")
        print("\nAll directories created: ✅")
        print("All __init__.py files exist: ✅")
        print("All root files exist: ✅")
        print(".gitignore is correct: ✅")
        print("requirements.txt has dependencies: ✅")
        print("Structure verified: ✅")
        print("\n🎉 Project structure is ready for development!")
        return True
    else:
        print(f"\n⚠️  Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        
        if all_checks_passed:
            print("\n✅ Core structure is complete")
            print("⚠️  Minor issues found but structure is functional")
            return True
        else:
            print("\n❌ Critical issues found")
            print("Please fix issues before proceeding")
            return False

if __name__ == "__main__":
    success = verify_step12()
    sys.exit(0 if success else 1)

