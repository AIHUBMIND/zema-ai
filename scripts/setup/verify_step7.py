#!/usr/bin/env python3
"""
Step 7 Verification: Create .gitignore
Verifies .gitignore file has all required patterns
"""

from pathlib import Path

def verify_step7():
    """Verify Step 7: .gitignore file"""
    
    print("=" * 60)
    print("SETUP-001 Step 7: Create .gitignore")
    print("=" * 60)
    
    # Required patterns from SETUP-001 Step 7
    required_patterns = {
        "Python": [
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
            ".Python",
            "venv/",
            "env/",
            "ENV/",
            ".venv"
        ],
        "Data files": [
            "data/db/*.db",
            "data/logs/*.log",
            "data/models/*",
            "!data/models/.gitkeep",
            "data/backups/*",
            "data/audio/*",
            "data/images/*",
            "data/exports/*"
        ],
        "Environment": [
            ".env",
            ".env.local"
        ],
        "IDE": [
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo"
        ],
        "OS": [
            ".DS_Store",
            "Thumbs.db"
        ],
        "Testing": [
            ".pytest_cache/",
            ".coverage",
            "htmlcov/"
        ],
        "Build": [
            "dist/",
            "build/",
            "*.egg-info/"
        ]
    }
    
    # Check if .gitignore exists
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        print("\n❌ .gitignore file does not exist!")
        return False
    
    print("\n✅ .gitignore file exists")
    
    # Read .gitignore content
    try:
        gitignore_content = gitignore_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"\n❌ Error reading .gitignore: {e}")
        return False
    
    print("\n📋 Checking required patterns...")
    
    all_patterns_present = True
    missing_patterns = {}
    
    for category, patterns in required_patterns.items():
        print(f"\n{category}:")
        category_missing = []
        
        for pattern in patterns:
            # Check if pattern exists in content
            # For negation patterns (!), check exact match
            if pattern.startswith("!"):
                if pattern in gitignore_content:
                    print(f"  ✅ {pattern}")
                else:
                    print(f"  ❌ Missing: {pattern}")
                    category_missing.append(pattern)
                    all_patterns_present = False
            else:
                # For regular patterns, check if pattern exists
                if pattern in gitignore_content:
                    print(f"  ✅ {pattern}")
                else:
                    # Check for similar patterns (e.g., __pycache__ vs __pycache__/)
                    pattern_found = False
                    for line in gitignore_content.split('\n'):
                        if pattern.replace('/', '') in line.replace('/', '') or line.strip() == pattern:
                            pattern_found = True
                            break
                    
                    if pattern_found:
                        print(f"  ✅ {pattern} (found similar)")
                    else:
                        print(f"  ❌ Missing: {pattern}")
                        category_missing.append(pattern)
                        all_patterns_present = False
        
        if category_missing:
            missing_patterns[category] = category_missing
    
    # Check for additional .gitkeep exceptions (bonus - added in Step 3)
    print("\n📋 Checking .gitkeep exceptions...")
    gitkeep_exceptions = [
        "!data/db/.gitkeep",
        "!data/logs/.gitkeep",
        "!data/backups/.gitkeep",
        "!data/audio/.gitkeep",
        "!data/images/.gitkeep",
        "!data/exports/.gitkeep",
        "!data/config/.gitkeep"
    ]
    
    gitkeep_present = []
    gitkeep_missing = []
    
    for exception in gitkeep_exceptions:
        if exception in gitignore_content:
            gitkeep_present.append(exception)
            print(f"  ✅ {exception}")
        else:
            gitkeep_missing.append(exception)
            print(f"  ⚠️  Missing: {exception} (optional, but recommended)")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_patterns_present:
        print("\n✅ All required patterns from SETUP-001 Step 7 are present")
    else:
        print(f"\n⚠️  Missing {sum(len(v) for v in missing_patterns.values())} pattern(s):")
        for category, patterns in missing_patterns.items():
            print(f"  {category}: {', '.join(patterns)}")
    
    if gitkeep_present:
        print(f"\n✅ Found {len(gitkeep_present)} .gitkeep exception(s) (bonus)")
    
    if gitkeep_missing:
        print(f"\n⚠️  Missing {len(gitkeep_missing)} .gitkeep exception(s) (recommended for Step 3)")
    
    # Final status
    if all_patterns_present:
        print("\n✅ Step 7 is COMPLETE!")
        if gitkeep_missing:
            print("   Note: Consider adding .gitkeep exceptions for better directory tracking")
        return True
    else:
        print("\n⚠️  Step 7 has missing patterns")
        print("   Please add missing patterns to .gitignore")
        return False

if __name__ == "__main__":
    success = verify_step7()
    exit(0 if success else 1)

