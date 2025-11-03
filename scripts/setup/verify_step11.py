#!/usr/bin/env python3
"""
Step 11 Verification: Create .env.example
Verifies .env.example has all required environment variables
"""

from pathlib import Path

def verify_step11():
    """Verify Step 11: .env.example file"""
    
    print("=" * 60)
    print("SETUP-001 Step 11: Create .env.example")
    print("=" * 60)
    
    # Required environment variables from SETUP-001 Step 11
    required_vars = {
        "General": [
            "ENVIRONMENT",
            "LOG_LEVEL",
            "HOSTNAME"
        ],
        "Dashboard": [
            "ENABLE_DASHBOARD",
            "DASHBOARD_PORT",
            "DASHBOARD_HOST"
        ],
        "Privacy": [
            "PRIVACY_MODE",
            "DATA_RETENTION_DAYS"
        ],
        "Audio": [
            "AUDIO_SAMPLE_RATE",
            "AUDIO_CHANNELS"
        ],
        "Voice": [
            "STT_MODEL",
            "STT_LANGUAGE",
            "TTS_ENGINE",
            "TTS_VOICE",
            "TTS_SPEED"
        ],
        "LLM": [
            "LLM_MODEL",
            "LLM_TEMPERATURE",
            "LLM_MAX_TOKENS"
        ],
        "Camera": [
            "CAMERA_DEVICE",
            "CAMERA_WIDTH",
            "CAMERA_HEIGHT",
            "CAMERA_FPS"
        ]
    }
    
    # Check if .env.example exists
    env_example_path = Path(".env.example")
    
    if not env_example_path.exists():
        print("\n❌ .env.example file does not exist!")
        return False
    
    print("\n✅ .env.example file exists")
    
    # Read .env.example content
    try:
        env_content = env_example_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"\n❌ Error reading .env.example: {e}")
        return False
    
    # Get file stats
    lines = env_content.split('\n')
    non_empty_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
    
    print(f"\n📊 File Statistics:")
    print(f"  Total lines: {len(lines)}")
    print(f"  Variable lines: {len(non_empty_lines)}")
    print(f"  Comment lines: {len([l for l in lines if l.strip().startswith('#')])}")
    
    print("\n📋 Checking required environment variables...")
    
    all_vars_present = True
    missing_vars = {}
    
    for category, vars_list in required_vars.items():
        print(f"\n{category}:")
        category_missing = []
        
        for var in vars_list:
            # Check if variable exists (case-sensitive)
            if var in env_content:
                # Try to find the actual line
                found_line = None
                for line in lines:
                    if line.strip().startswith(var + "=") or line.strip().startswith(var + " ="):
                        found_line = line.strip()
                        break
                
                if found_line:
                    print(f"  ✅ {var}")
                    if "=" in found_line:
                        value = found_line.split("=", 1)[1].strip()
                        if value:
                            print(f"    Value: {value}")
                else:
                    print(f"  ⚠️  {var} mentioned but not properly formatted")
                    category_missing.append(var)
                    all_vars_present = False
            else:
                print(f"  ❌ Missing: {var}")
                category_missing.append(var)
                all_vars_present = False
        
        if category_missing:
            missing_vars[category] = category_missing
    
    # Check for comments/documentation
    print("\n📋 Checking documentation...")
    
    has_header_comment = "#" in env_content and ("zema" in env_content.lower() or "configuration" in env_content.lower())
    has_category_comments = env_content.count("# ") >= 5  # At least 5 comment sections
    
    if has_header_comment:
        print("  ✅ Has header comment")
    else:
        print("  ⚠️  Missing header comment")
    
    if has_category_comments:
        print(f"  ✅ Has {env_content.count('# ')} category comments")
    else:
        print(f"  ⚠️  Only {env_content.count('# ')} category comments (recommended: 5+)")
    
    # Check for copy instruction
    has_copy_instruction = "copy" in env_content.lower() or "cp" in env_content.lower() or ".env" in env_content
    if has_copy_instruction:
        print("  ✅ Has copy instruction")
    else:
        print("  ⚠️  Missing copy instruction")
    
    # Check file format
    print("\n📋 Checking file format...")
    
    valid_format = True
    format_issues = []
    
    for line in non_empty_lines:
        if "=" not in line:
            format_issues.append(f"Line without '=': {line[:50]}")
            valid_format = False
    
    if valid_format:
        print("  ✅ All variable lines have proper format (VAR=value)")
    else:
        print(f"  ⚠️  Found {len(format_issues)} format issue(s)")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    total_required = sum(len(vars_list) for vars_list in required_vars.values())
    total_found = total_required - sum(len(vars_list) for vars_list in missing_vars.values())
    
    print(f"\n📊 Variables Required: {total_required}")
    print(f"📊 Variables Found: {total_found}/{total_required}")
    
    if all_vars_present:
        print("\n✅ All required environment variables from SETUP-001 Step 11 are present")
    else:
        print(f"\n⚠️  Missing {sum(len(v) for v in missing_vars.values())} variable(s):")
        for category, vars_list in missing_vars.items():
            print(f"  {category}: {', '.join(vars_list)}")
    
    # Final status
    if all_vars_present:
        print("\n✅ Step 11 is COMPLETE!")
        if has_header_comment and has_category_comments:
            print("   ✅ Well-documented with comments")
        if valid_format:
            print("   ✅ Proper format for all variables")
        return True
    else:
        print("\n⚠️  Step 11 has missing variables")
        print("   Please add missing variables to .env.example")
        return False

if __name__ == "__main__":
    success = verify_step11()
    exit(0 if success else 1)

