#!/usr/bin/env python3
"""
Step 9 Verification: Create README.md
Verifies README.md has all required sections
"""

from pathlib import Path

def verify_step9():
    """Verify Step 9: README.md file"""
    
    print("=" * 60)
    print("SETUP-001 Step 9: Create README.md")
    print("=" * 60)
    
    # Required sections from SETUP-001 Step 9
    required_sections = {
        "Project title and description": [
            "zema",
            "privacy",
            "voice assistant",
            "mini pc"
        ],
        "Features list": [
            "features",
            "privacy",
            "offline",
            "voice"
        ],
        "Quick start guide": [
            "quick start",
            "prerequisites",
            "installation",
            "clone"
        ],
        "Installation instructions": [
            "install",
            "setup",
            "requirements",
            "venv"
        ],
        "Usage examples": [
            "usage",
            "example",
            "how to",
            "voice interaction"
        ],
        "Project structure overview": [
            "structure",
            "directory",
            "src/",
            "data/",
            "tests/"
        ],
        "Contributing guidelines": [
            "contributing",
            "contribute",
            "development"
        ]
    }
    
    # Check if README.md exists
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("\n❌ README.md file does not exist!")
        return False
    
    print("\n✅ README.md file exists")
    
    # Read README.md content
    try:
        readme_content = readme_path.read_text(encoding='utf-8')
        readme_lower = readme_content.lower()
    except Exception as e:
        print(f"\n❌ Error reading README.md: {e}")
        return False
    
    # Get file stats
    file_size = len(readme_content)
    line_count = len(readme_content.split('\n'))
    
    print(f"\n📊 File Statistics:")
    print(f"  Size: {file_size:,} characters")
    print(f"  Lines: {line_count:,} lines")
    
    print("\n📋 Checking required sections...")
    
    all_sections_present = True
    missing_sections = []
    
    for section_name, keywords in required_sections.items():
        print(f"\n{section_name}:")
        
        # Check if at least 2 keywords are found (flexible matching)
        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in readme_lower:
                found_keywords.append(keyword)
        
        if len(found_keywords) >= 2:
            print(f"  ✅ Found ({len(found_keywords)}/{len(keywords)} keywords)")
            for kw in found_keywords:
                print(f"    - {kw}")
        else:
            print(f"  ⚠️  Missing ({len(found_keywords)}/{len(keywords)} keywords)")
            missing_sections.append(section_name)
            all_sections_present = False
    
    # Check for markdown formatting
    print("\n📋 Checking markdown formatting...")
    
    has_headers = "#" in readme_content
    has_code_blocks = "```" in readme_content
    has_lists = "- " in readme_content or "* " in readme_content
    has_links = "[" in readme_content and "]" in readme_content and "(" in readme_content
    
    if has_headers:
        print("  ✅ Has markdown headers (#)")
    else:
        print("  ⚠️  Missing markdown headers")
    
    if has_code_blocks:
        print("  ✅ Has code blocks (```)")
    else:
        print("  ⚠️  Missing code blocks")
    
    if has_lists:
        print("  ✅ Has lists (- or *)")
    else:
        print("  ⚠️  Missing lists")
    
    # Count sections
    header_count = readme_content.count('# ')
    print(f"\n📊 Markdown Structure:")
    print(f"  Headers (H1): {readme_content.count('# ')}")
    print(f"  Headers (H2): {readme_content.count('## ')}")
    print(f"  Code blocks: {readme_content.count('```') // 2}")
    print(f"  List items: {readme_content.count('- ')}")
    
    # Check for specific important content
    print("\n📋 Checking important content...")
    
    important_checks = {
        "Project title": "zema" in readme_lower,
        "GitHub repository link": "github.com" in readme_lower or "git clone" in readme_lower,
        "Python version": "python 3.11" in readme_lower or "python3.11" in readme_lower,
        "Installation steps": "pip install" in readme_lower or "requirements.txt" in readme_lower,
        "Usage examples": "usage" in readme_lower or "example" in readme_lower,
        "Project structure": "src/" in readme_content or "structure" in readme_lower
    }
    
    for check_name, check_result in important_checks.items():
        if check_result:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ⚠️  Missing: {check_name}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_sections_present:
        print("\n✅ All required sections from SETUP-001 Step 9 are present")
    else:
        print(f"\n⚠️  Missing {len(missing_sections)} section(s):")
        for section in missing_sections:
            print(f"  - {section}")
    
    # Quality assessment
    quality_score = 0
    max_score = 7
    
    if all_sections_present:
        quality_score += 7
    
    if has_headers and has_code_blocks and has_lists:
        quality_score += 1
    
    quality_percentage = (quality_score / max_score) * 100
    
    print(f"\n📊 Quality Score: {quality_score}/{max_score} ({quality_percentage:.0f}%)")
    
    # Final status
    if all_sections_present:
        print("\n✅ Step 9 is COMPLETE!")
        if quality_percentage >= 90:
            print("   ✅ High-quality README with good formatting")
        elif quality_percentage >= 70:
            print("   ✅ Good README with minor improvements possible")
        return True
    else:
        print("\n⚠️  Step 9 has missing sections")
        print("   Please add missing sections to README.md")
        return False

if __name__ == "__main__":
    success = verify_step9()
    exit(0 if success else 1)

