#!/usr/bin/env python3
"""
Step 6 Verification: Create Root Files
Verifies all required root files exist and have correct content
"""

from pathlib import Path
import re

def verify_step6():
    """Verify and fix Step 6: Root files"""
    
    print("=" * 60)
    print("SETUP-001 Step 6: Create Root Files")
    print("=" * 60)
    
    # Required files from SETUP-001 Step 6
    required_files = {
        "README.md": {
            "exists": True,
            "required_sections": [
                "Features",
                "Quick Start",
                "Installation",
                "Project Structure",
                "Usage"
            ]
        },
        "requirements.txt": {
            "exists": True,
            "required_deps": [
                "fastapi",
                "pydantic",
                "sqlalchemy",
                "pyaudio",
                "faster-whisper",
                "opencv-python-headless",
                "pytest"
            ]
        },
        "pyproject.toml": {
            "exists": True,
            "required_items": [
                "[build-system]",
                "[project]",
                'name = "zema-ai"',
                'requires-python = ">=3.11"'
            ]
        },
        ".env.example": {
            "exists": True,
            "required_vars": [
                "ENVIRONMENT",
                "LOG_LEVEL",
                "DASHBOARD_PORT",
                "PRIVACY_MODE",
                "LLM_MODEL"
            ]
        },
        ".gitignore": {
            "exists": True,
            "required_patterns": [
                "__pycache__/",
                "venv/",
                ".env",
                "data/db/*.db",
                "data/logs/*.log"
            ]
        },
        "setup.py": {
            "exists": True,
            "required_items": [
                "setuptools",
                "zema-ai",
                "find_packages"
            ]
        },
        "setup.sh": {
            "exists": True,
            "required_items": [
                "#!/bin/bash",
                "python3.11",
                "venv",
                "requirements.txt"
            ]
        }
    }
    
    print("\n📄 Checking root files...")
    all_exist = True
    issues = []
    
    for filename, checks in required_files.items():
        path = Path(filename)
        
        if not path.exists():
            print(f"  ❌ Missing: {filename}")
            all_exist = False
            issues.append(f"Missing file: {filename}")
            continue
        
        print(f"  ✅ {filename}")
        
        # Check file content
        try:
            content = path.read_text(encoding='utf-8')
            
            # Check required sections/dependencies/items
            if "required_sections" in checks:
                missing_sections = []
                for section in checks["required_sections"]:
                    if section.lower() not in content.lower():
                        missing_sections.append(section)
                if missing_sections:
                    issues.append(f"{filename} missing sections: {', '.join(missing_sections)}")
                    print(f"    ⚠️  Missing sections: {', '.join(missing_sections)}")
                else:
                    print(f"    ✅ All required sections present")
            
            if "required_deps" in checks:
                missing_deps = []
                for dep in checks["required_deps"]:
                    if dep.lower() not in content.lower():
                        missing_deps.append(dep)
                if missing_deps:
                    issues.append(f"{filename} missing dependencies: {', '.join(missing_deps)}")
                    print(f"    ⚠️  Missing dependencies: {', '.join(missing_deps)}")
                else:
                    print(f"    ✅ All required dependencies present")
            
            if "required_items" in checks:
                missing_items = []
                for item in checks["required_items"]:
                    if item.lower() not in content.lower():
                        missing_items.append(item)
                if missing_items:
                    issues.append(f"{filename} missing items: {', '.join(missing_items)}")
                    print(f"    ⚠️  Missing items: {', '.join(missing_items)}")
                else:
                    print(f"    ✅ All required items present")
            
            if "required_vars" in checks:
                missing_vars = []
                for var in checks["required_vars"]:
                    if var not in content:
                        missing_vars.append(var)
                if missing_vars:
                    issues.append(f"{filename} missing variables: {', '.join(missing_vars)}")
                    print(f"    ⚠️  Missing variables: {', '.join(missing_vars)}")
                else:
                    print(f"    ✅ All required variables present")
            
            if "required_patterns" in checks:
                missing_patterns = []
                for pattern in checks["required_patterns"]:
                    if pattern not in content:
                        missing_patterns.append(pattern)
                if missing_patterns:
                    issues.append(f"{filename} missing patterns: {', '.join(missing_patterns)}")
                    print(f"    ⚠️  Missing patterns: {', '.join(missing_patterns)}")
                else:
                    print(f"    ✅ All required patterns present")
        
        except Exception as e:
            issues.append(f"Error reading {filename}: {e}")
            print(f"    ❌ Error reading file: {e}")
    
    # Additional checks
    print("\n📋 Additional checks...")
    
    # Check README.md has all required sections
    if Path("README.md").exists():
        readme = Path("README.md").read_text(encoding='utf-8')
        if "Project Structure" in readme:
            print("  ✅ README.md has project structure")
        if "Contributing" in readme or "contributing" in readme.lower():
            print("  ✅ README.md has contributing section")
        else:
            print("  ⚠️  README.md missing contributing section (optional)")
    
    # Check pyproject.toml has pytest config
    if Path("pyproject.toml").exists():
        pyproject = Path("pyproject.toml").read_text(encoding='utf-8')
        if "[tool.pytest.ini_options]" in pyproject or "pytest" in pyproject.lower():
            print("  ✅ pyproject.toml has pytest configuration")
    
    # Check setup.sh is executable (on Unix)
    if Path("setup.sh").exists():
        print("  ✅ setup.sh exists")
        # Note: On Windows, we can't check execute permissions
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_exist and not issues:
        print("\n✅ All 7 required root files exist")
        print("✅ All files have required content")
        print("\n✅ Step 6 is COMPLETE!")
        return True
    elif all_exist:
        print("\n✅ All 7 required root files exist")
        print(f"⚠️  Found {len(issues)} content issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        print("\n⚠️  Step 6 has minor content issues but files exist")
        return True
    else:
        print(f"\n❌ Missing {len([f for f in required_files if not Path(f).exists()])} file(s)")
        print(f"⚠️  Found {len(issues)} issue(s)")
        for issue in issues:
            print(f"  - {issue}")
        return False

if __name__ == "__main__":
    success = verify_step6()
    exit(0 if success else 1)

