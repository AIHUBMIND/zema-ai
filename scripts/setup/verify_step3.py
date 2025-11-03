#!/usr/bin/env python3
"""
Step 3 Verification: Data Directory Structure
Creates missing .gitkeep files to ensure directories are tracked by Git
"""

from pathlib import Path

def verify_step3():
    """Verify and fix Step 3: Data directory structure"""
    
    print("=" * 60)
    print("SETUP-001 Step 3: Create Data Directory Structure")
    print("=" * 60)
    
    # Required directories from SETUP-001 Step 3
    required_dirs = [
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
    
    print("\n📁 Checking directories...")
    all_exist = True
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ Missing: {dir_path}")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some directories are missing!")
        return False
    
    print("\n📄 Checking .gitkeep files...")
    missing_gitkeep = []
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        gitkeep_path = path / ".gitkeep"
        
        # Check if directory has files (excluding .gitkeep)
        has_files = False
        if path.exists():
            for item in path.iterdir():
                if item.name != ".gitkeep" and item.is_file():
                    has_files = True
                    break
        
        # If directory is empty or only has .gitkeep, ensure .gitkeep exists
        if not gitkeep_path.exists():
            if not has_files:
                missing_gitkeep.append(dir_path)
                print(f"  ⚠️  Missing .gitkeep: {dir_path}/")
            else:
                print(f"  ℹ️  Has files, skipping .gitkeep: {dir_path}/")
        else:
            print(f"  ✅ {dir_path}/.gitkeep")
    
    # Create missing .gitkeep files
    if missing_gitkeep:
        print(f"\n📝 Creating {len(missing_gitkeep)} missing .gitkeep file(s)...")
        for dir_path in missing_gitkeep:
            gitkeep_path = Path(dir_path) / ".gitkeep"
            gitkeep_path.write_text("# This file ensures the directory is tracked by Git\n")
            print(f"  ✅ Created: {gitkeep_path}")
    else:
        print("\n✅ All required .gitkeep files exist!")
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print("✅ All 9 data directories exist")
    if missing_gitkeep:
        print(f"✅ Created {len(missing_gitkeep)} missing .gitkeep file(s)")
    else:
        print("✅ All .gitkeep files present")
    print("\n✅ Step 3 is COMPLETE!")
    
    return True

if __name__ == "__main__":
    success = verify_step3()
    exit(0 if success else 1)

