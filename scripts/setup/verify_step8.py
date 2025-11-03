#!/usr/bin/env python3
"""
Step 8 Verification: Create requirements.txt
Verifies requirements.txt has all required dependencies
"""

from pathlib import Path

def verify_step8():
    """Verify Step 8: requirements.txt file"""
    
    print("=" * 60)
    print("SETUP-001 Step 8: Create requirements.txt")
    print("=" * 60)
    
    # Required dependencies from SETUP-001 Step 8
    required_deps = {
        "Core": [
            "fastapi",
            "uvicorn",
            "pydantic",
            "pydantic-settings",
            "httpx",
            "python-dotenv",
            "pyyaml"
        ],
        "Database": [
            "sqlalchemy",
            "aiosqlite"
        ],
        "Async": [
            "aiofiles",
            "python-multipart"
        ],
        "Logging": [
            "structlog",
            "rich"
        ],
        "Audio": [
            "pyaudio",
            "webrtcvad",
            "pvporcupine"
        ],
        "AI/ML": [
            "faster-whisper",
            "piper-tts",
            "ultralytics"
        ],
        "Vision": [
            "opencv-python-headless",
            "numpy",
            "pillow"
        ],
        "Testing": [
            "pytest",
            "pytest-asyncio",
            "pytest-cov"
        ],
        "Utilities": [
            "psutil",
            "python-dateutil"
        ]
    }
    
    # Check if requirements.txt exists
    req_path = Path("requirements.txt")
    
    if not req_path.exists():
        print("\n❌ requirements.txt file does not exist!")
        return False
    
    print("\n✅ requirements.txt file exists")
    
    # Read requirements.txt content
    try:
        req_content = req_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"\n❌ Error reading requirements.txt: {e}")
        return False
    
    print("\n📋 Checking required dependencies...")
    
    all_deps_present = True
    missing_deps = {}
    
    for category, deps in required_deps.items():
        print(f"\n{category}:")
        category_missing = []
        
        for dep in deps:
            # Check if dependency exists (case-insensitive)
            dep_lower = dep.lower()
            found = False
            
            for line in req_content.split('\n'):
                line_lower = line.lower().strip()
                # Skip comments and empty lines
                if line_lower.startswith('#') or not line_lower:
                    continue
                
                # Check if dependency name is in the line
                # Handle version specifiers (>=, ==, etc.)
                if dep_lower in line_lower.split('>=')[0].split('==')[0].split('<=')[0].split('[')[0].strip():
                    found = True
                    # Extract version if present
                    version_info = ""
                    if '>=' in line_lower or '==' in line_lower or '<=' in line_lower:
                        version_info = " (with version)"
                    print(f"  ✅ {dep}{version_info}")
                    break
            
            if not found:
                print(f"  ❌ Missing: {dep}")
                category_missing.append(dep)
                all_deps_present = False
        
        if category_missing:
            missing_deps[category] = category_missing
    
    # Check for proper organization (comments)
    print("\n📋 Checking file organization...")
    has_comments = False
    comment_categories = []
    
    for line in req_content.split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('#') and line_stripped[1:].strip():
            has_comments = True
            category = line_stripped[1:].strip()
            if category not in comment_categories:
                comment_categories.append(category)
    
    if has_comments:
        print(f"  ✅ File has organizational comments ({len(comment_categories)} categories)")
        for cat in comment_categories:
            print(f"    - {cat}")
    else:
        print("  ⚠️  File lacks organizational comments (optional but recommended)")
    
    # Check for version specifiers
    print("\n📋 Checking version specifiers...")
    lines_with_versions = 0
    total_deps = 0
    
    for line in req_content.split('\n'):
        line_stripped = line.strip()
        if line_stripped and not line_stripped.startswith('#'):
            total_deps += 1
            if '>=' in line_stripped or '==' in line_stripped or '<=' in line_stripped:
                lines_with_versions += 1
    
    if total_deps > 0:
        version_percentage = (lines_with_versions / total_deps) * 100
        print(f"  ✅ {lines_with_versions}/{total_deps} dependencies have version specifiers ({version_percentage:.0f}%)")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_deps_present:
        print("\n✅ All required dependencies from SETUP-001 Step 8 are present")
    else:
        print(f"\n⚠️  Missing {sum(len(v) for v in missing_deps.values())} dependency(ies):")
        for category, deps in missing_deps.items():
            print(f"  {category}: {', '.join(deps)}")
    
    # Dependency count
    total_required = sum(len(deps) for deps in required_deps.values())
    print(f"\n📊 Total required dependencies: {total_required}")
    print(f"📊 Dependencies found: {total_required - sum(len(v) for v in missing_deps.values())}")
    
    # Final status
    if all_deps_present:
        print("\n✅ Step 8 is COMPLETE!")
        if has_comments:
            print("   ✅ File is well-organized with comments")
        if version_percentage >= 80:
            print("   ✅ Most dependencies have version specifiers")
        return True
    else:
        print("\n⚠️  Step 8 has missing dependencies")
        print("   Please add missing dependencies to requirements.txt")
        return False

if __name__ == "__main__":
    success = verify_step8()
    exit(0 if success else 1)

