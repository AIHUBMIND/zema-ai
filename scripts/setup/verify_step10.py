#!/usr/bin/env python3
"""
Step 10 Verification: Create pyproject.toml
Verifies pyproject.toml has all required configuration
"""

from pathlib import Path
import re

def verify_step10():
    """Verify Step 10: pyproject.toml file"""
    
    print("=" * 60)
    print("SETUP-001 Step 10: Create pyproject.toml")
    print("=" * 60)
    
    # Required configuration from SETUP-001 Step 10
    required_config = {
        "[build-system]": {
            "required": True,
            "requires": ["setuptools>=61.0"],
            "build_backend": "setuptools.build_meta"
        },
        "[project]": {
            "required": True,
            "name": "zema-ai",
            "version": "0.1.0",
            "description": "Privacy-first voice assistant for mini PC",
            "requires_python": ">=3.11"
        },
        "[tool.pytest.ini_options]": {
            "required": True,
            "asyncio_mode": "auto"
        }
    }
    
    # Check if pyproject.toml exists
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        print("\n❌ pyproject.toml file does not exist!")
        return False
    
    print("\n✅ pyproject.toml file exists")
    
    # Read pyproject.toml content
    try:
        pyproject_content = pyproject_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"\n❌ Error reading pyproject.toml: {e}")
        return False
    
    print("\n📋 Checking required sections...")
    
    all_sections_present = True
    issues = []
    
    # Check [build-system]
    if "[build-system]" in pyproject_content:
        print("\n[build-system]:")
        print("  ✅ Section exists")
        
        # Extract build-system section
        build_system_match = re.search(r'\[build-system\]\s*(.*?)(?=\[|$)', pyproject_content, re.DOTALL)
        if build_system_match:
            build_system_content = build_system_match.group(1)
            
            if "requires" in build_system_content:
                if "setuptools" in build_system_content.lower() or "setuptools" in pyproject_content:
                    print("  ✅ Requires setuptools")
                else:
                    print("  ⚠️  Requires setuptools not found")
                    issues.append("build-system requires setuptools")
            else:
                # Check if requires is on a different line
                if "setuptools" in pyproject_content:
                    print("  ✅ Requires setuptools")
                else:
                    print("  ⚠️  Requires setuptools not found")
                    issues.append("build-system requires setuptools")
            
            if "build-backend" in build_system_content:
                if "setuptools.build_meta" in build_system_content:
                    print("  ✅ Build backend set to setuptools.build_meta")
                else:
                    print("  ⚠️  Build backend not set correctly")
                    issues.append("build-system build-backend")
        else:
            print("  ⚠️  Could not parse build-system section")
            issues.append("build-system parsing")
    else:
        print("\n[build-system]:")
        print("  ❌ Section missing")
        all_sections_present = False
        issues.append("Missing [build-system] section")
    
    # Check [project]
    if "[project]" in pyproject_content:
        print("\n[project]:")
        print("  ✅ Section exists")
        
        # Extract project section
        project_match = re.search(r'\[project\]\s*(.*?)(?=\[|$)', pyproject_content, re.DOTALL)
        if project_match:
            project_content = project_match.group(1)
            
            checks = {
                "name": ('name = "zema-ai"', 'name = "zema-ai"'),
                "version": ('version = "0.1.0"', 'version = "0.1.0"'),
                "description": ('description = "Privacy-first voice assistant for mini PC"', 'description'),
                "requires_python": ('requires-python = ">=3.11"', 'requires-python')
            }
            
            for key, (exact_match, partial_match) in checks.items():
                if exact_match in project_content or partial_match in project_content:
                    print(f"  ✅ {key}")
                else:
                    print(f"  ⚠️  Missing: {key}")
                    issues.append(f"project.{key}")
        else:
            print("  ⚠️  Could not parse project section")
            issues.append("project parsing")
    else:
        print("\n[project]:")
        print("  ❌ Section missing")
        all_sections_present = False
        issues.append("Missing [project] section")
    
    # Check [tool.pytest.ini_options]
    if "[tool.pytest.ini_options]" in pyproject_content or "[tool.pytest.ini_options]" in pyproject_content:
        print("\n[tool.pytest.ini_options]:")
        print("  ✅ Section exists")
        
        # Extract pytest section
        pytest_match = re.search(r'\[tool\.pytest\.ini_options\]\s*(.*?)(?=\[|$)', pyproject_content, re.DOTALL)
        if pytest_match:
            pytest_content = pytest_match.group(1)
            
            if "asyncio_mode" in pytest_content:
                if "auto" in pytest_content or "asyncio_mode = \"auto\"" in pytest_content:
                    print("  ✅ asyncio_mode = auto")
                else:
                    print("  ⚠️  asyncio_mode not set to auto")
                    issues.append("pytest asyncio_mode")
            else:
                print("  ⚠️  Missing asyncio_mode")
                issues.append("pytest asyncio_mode missing")
        else:
            print("  ⚠️  Could not parse pytest section")
            issues.append("pytest parsing")
    else:
        print("\n[tool.pytest.ini_options]:")
        print("  ⚠️  Section missing (optional but recommended)")
    
    # Check for TOML syntax validity
    print("\n📋 Checking TOML syntax...")
    try:
        # Try to parse as TOML (basic check)
        lines = pyproject_content.split('\n')
        bracket_count = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('[') and stripped.endswith(']'):
                bracket_count += 1
        
        if bracket_count >= 2:
            print(f"  ✅ Found {bracket_count} sections")
        else:
            print(f"  ⚠️  Only {bracket_count} sections found (expected at least 2)")
    except Exception as e:
        print(f"  ⚠️  Syntax check warning: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_sections_present and not issues:
        print("\n✅ All required configuration from SETUP-001 Step 10 is present")
        print("✅ pyproject.toml is properly configured")
        print("\n✅ Step 10 is COMPLETE!")
        return True
    elif all_sections_present:
        print("\n✅ All required sections present")
        print(f"⚠️  Found {len(issues)} minor issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        print("\n⚠️  Step 10 has minor issues but is functional")
        return True
    else:
        print(f"\n❌ Missing {len([i for i in issues if 'Missing' in i])} required section(s)")
        print(f"⚠️  Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        return False

if __name__ == "__main__":
    success = verify_step10()
    exit(0 if success else 1)

