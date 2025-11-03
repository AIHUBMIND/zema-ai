#!/usr/bin/env python3
"""Git repository setup and remote configuration helper."""
import sys
from pathlib import Path

def check_git_status():
    """Check Git repository status."""
    git_dir = Path(".git")
    git_config = Path(".git/config")
    
    print("=" * 60)
    print("GIT REPOSITORY STATUS")
    print("=" * 60)
    print()
    
    if not git_dir.exists():
        print("✗ Git repository NOT initialized")
        return False
    
    print("✓ Git repository initialized (.git/ folder exists)")
    
    if git_config.exists():
        print("✓ Git config file exists")
        
        # Check for remote
        config_content = git_config.read_text()
        if "[remote" in config_content:
            print("✓ Remote repository configured")
            print("\nCurrent remote configuration:")
            for line in config_content.split("\n"):
                if "url" in line.lower() or "remote" in line.lower():
                    print(f"  {line.strip()}")
        else:
            print("⚠ No remote repository configured")
            print("  (This is fine for local development)")
    
    return True

def generate_github_setup_instructions():
    """Generate instructions for GitHub setup."""
    print("\n" + "=" * 60)
    print("GITHUB REPOSITORY SETUP OPTIONS")
    print("=" * 60)
    print()
    
    print("OPTION 1: Create GitHub repo manually (Recommended)")
    print("-" * 60)
    print("""
1. Go to https://github.com/new
2. Repository name: zema-ai
3. Description: Privacy-first voice assistant for mini PC
4. Visibility: Private (recommended) or Public
5. DO NOT initialize with README, .gitignore, or license
6. Click "Create repository"

7. After creation, GitHub will show commands. Run these locally:
   
   git remote add origin https://github.com/YOUR_USERNAME/zema-ai.git
   git branch -M main
   git add .
   git commit -m "Initial commit: Zema AI project setup"
   git push -u origin main
""")
    
    print("\nOPTION 2: Using GitHub CLI (if installed)")
    print("-" * 60)
    print("""
If you have GitHub CLI installed:
   gh repo create zema-ai --private --source=. --remote=origin --push
""")
    
    print("\nOPTION 3: I can prepare a script")
    print("-" * 60)
    print("""
I can create a setup script that you can run after creating the GitHub repo.
Just provide:
- Your GitHub username
- Repository name (default: zema-ai)
- Whether it's private or public
""")

if __name__ == "__main__":
    is_initialized = check_git_status()
    
    if is_initialized:
        generate_github_setup_instructions()
        
        print("\n" + "=" * 60)
        print("RECOMMENDATION")
        print("=" * 60)
        print("""
Your Git repository is initialized locally. You can:
1. Continue development locally (no remote needed)
2. Set up GitHub remote when ready
3. Use the verification script - it will pass Git checks now

The verification script has been updated to recognize that Git is
initialized even if the 'git' command isn't in PATH.
""")
    else:
        print("\n⚠ Git repository needs to be initialized.")
        print("Run: git init")

