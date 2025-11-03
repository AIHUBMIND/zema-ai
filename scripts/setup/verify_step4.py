#!/usr/bin/env python3
"""
Step 4 Verification: Test Directory Structure
Verifies all required test directories and files exist
"""

from pathlib import Path

def verify_step4():
    """Verify and fix Step 4: Test directory structure"""
    
    print("=" * 60)
    print("SETUP-001 Step 4: Create Test Directory Structure")
    print("=" * 60)
    
    # Required directories from SETUP-001 Step 4
    required_dirs = [
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/hardware",
        "tests/fixtures"
    ]
    
    # Required files
    required_files = [
        "tests/__init__.py",
        "tests/conftest.py"
    ]
    
    print("\n📁 Checking test directories...")
    all_dirs_exist = True
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ Missing: {dir_path}")
            all_dirs_exist = False
    
    print("\n📄 Checking required files...")
    missing_files = []
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists() and path.is_file():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    print("\n📄 Checking __init__.py files in subdirectories...")
    missing_init_files = []
    
    # Subdirectories that need __init__.py (excluding root tests/)
    subdirs_needing_init = [
        "tests/unit",
        "tests/integration",
        "tests/hardware",
        "tests/fixtures"
    ]
    
    for dir_path in subdirs_needing_init:
        path = Path(dir_path)
        init_path = path / "__init__.py"
        if path.exists() and path.is_dir():
            if init_path.exists():
                print(f"  ✅ {init_path}")
            else:
                print(f"  ⚠️  Missing: {init_path}")
                missing_init_files.append(init_path)
    
    # Create missing directories
    created_dirs = []
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(dir_path)
            print(f"  ✅ Created: {dir_path}")
    
    # Create missing __init__.py files
    created_init_files = []
    for init_path in missing_init_files:
        init_path.write_text('"""Test module for Zema AI."""\n')
        created_init_files.append(str(init_path))
        print(f"  ✅ Created: {init_path}")
    
    # Create missing files
    created_files = []
    for file_path in missing_files:
        path = Path(file_path)
        if file_path == "tests/__init__.py":
            path.write_text('"""Test package for Zema AI."""\n')
        elif file_path == "tests/conftest.py":
            path.write_text('"""Pytest configuration and fixtures for Zema AI tests."""\n\nimport pytest\nfrom pathlib import Path\n\n# Pytest configuration\npytest_plugins = []\n')
        created_files.append(file_path)
        print(f"  ✅ Created: {file_path}")
    
    # Verify conftest.py has basic content
    if Path("tests/conftest.py").exists():
        conftest_content = Path("tests/conftest.py").read_text()
        if "pytest" not in conftest_content.lower():
            print("  ⚠️  Warning: conftest.py exists but may need pytest configuration")
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if created_dirs:
        print(f"✅ Created {len(created_dirs)} missing directory(ies)")
    if created_init_files:
        print(f"✅ Created {len(created_init_files)} missing __init__.py file(s)")
    if created_files:
        print(f"✅ Created {len(created_files)} missing file(s)")
    
    if all_dirs_exist and not missing_files and not missing_init_files:
        print("\n✅ All required directories exist")
        print("✅ All required files exist")
        print("✅ All __init__.py files present")
        print("\n✅ Step 4 is COMPLETE!")
        return True
    else:
        if created_dirs or created_init_files or created_files:
            print("\n✅ Step 4 is now COMPLETE after fixes!")
            return True
        else:
            print("\n⚠️  Step 4 has issues - please review above")
            return False

if __name__ == "__main__":
    success = verify_step4()
    exit(0 if success else 1)
