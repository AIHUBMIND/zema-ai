#!/usr/bin/env python3
"""
Version Tagging Script
Creates and pushes Git tags for project milestones
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

GITHUB_REPO = "https://github.com/AIHUBMIND/zema-ai.git"
REMOTE = "origin"

def find_git_command():
    """Find git command path."""
    possible_paths = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe",
    ]
    
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return "git"
    except:
        pass
    
    for git_path in possible_paths:
        if Path(git_path).exists():
            return git_path
    
    return None

def run_git_command(cmd_list, description):
    """Run a git command."""
    git_cmd = find_git_command()
    
    if not git_cmd:
        print(f"✗ {description}")
        print("  Error: Git command not found")
        return False
    
    if isinstance(git_cmd, str) and git_cmd.endswith(".exe"):
        full_cmd = [git_cmd] + cmd_list
    else:
        full_cmd = ["git"] + cmd_list
    
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ {description}")
            if result.stdout.strip():
                print(f"  {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {description}")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Error: {e}")
        return False

def create_tag(version, message=""):
    """Create a Git tag."""
    print("=" * 60)
    print("CREATING VERSION TAG")
    print("=" * 60)
    print(f"\nVersion: {version}")
    print(f"Message: {message or 'No message provided'}")
    print()
    
    git_cmd = find_git_command()
    if not git_cmd:
        print("⚠ Git command not found")
        return False
    
    # Check if tag already exists
    check_cmd = ["tag", "-l", version]
    if isinstance(git_cmd, str) and git_cmd.endswith(".exe"):
        check_full = [git_cmd] + check_cmd
    else:
        check_full = ["git"] + check_cmd
    
    try:
        result = subprocess.run(
            check_full,
            capture_output=True,
            text=True,
            timeout=5
        )
        if version in result.stdout:
            print(f"⚠ Tag {version} already exists")
            response = input(f"Do you want to overwrite it? (y/n): ").strip().lower()
            if response != "y":
                print("Cancelled.")
                return False
            # Delete existing tag
            run_git_command(["tag", "-d", version], f"Deleting existing tag {version}")
            run_git_command(["push", REMOTE, "--delete", version], f"Deleting remote tag {version}")
    except:
        pass
    
    # Create annotated tag
    tag_msg = message or f"Version {version}"
    if not run_git_command(["tag", "-a", version, "-m", tag_msg], f"Creating tag {version}"):
        return False
    
    print()
    print("=" * 60)
    print("PUSHING TAG TO GITHUB")
    print("=" * 60)
    print()
    
    # Push tag to remote
    if run_git_command(["push", REMOTE, version], f"Pushing tag {version} to {REMOTE}"):
        print()
        print("=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"\nTag {version} created and pushed to:")
        print(f"  {GITHUB_REPO}")
        print(f"\nView at: https://github.com/AIHUBMIND/zema-ai/releases/tag/{version}")
        return True
    else:
        print()
        print("=" * 60)
        print("⚠️  PUSH FAILED")
        print("=" * 60)
        print(f"\nTag {version} created locally, but push failed.")
        print("You can push manually later with:")
        print(f"  git push {REMOTE} {version}")
        return False

def list_tags():
    """List all tags."""
    print("=" * 60)
    print("EXISTING TAGS")
    print("=" * 60)
    print()
    
    git_cmd = find_git_command()
    if not git_cmd:
        print("⚠ Git command not found")
        return
    
    check_cmd = ["tag", "-l", "--sort=-version:refname"]
    if isinstance(git_cmd, str) and git_cmd.endswith(".exe"):
        check_full = [git_cmd] + check_cmd
    else:
        check_full = ["git"] + check_cmd
    
    try:
        result = subprocess.run(
            check_full,
            capture_output=True,
            text=True,
            timeout=5
        )
        tags = result.stdout.strip().split("\n")
        if tags and tags[0]:
            for tag in tags:
                print(f"  • {tag}")
        else:
            print("  No tags found")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/maintenance/create_tag.py <version> [message]")
        print("  python scripts/maintenance/create_tag.py list")
        print()
        print("Examples:")
        print("  python scripts/maintenance/create_tag.py v0.1.0 'SETUP-001 Complete'")
        print("  python scripts/maintenance/create_tag.py v0.2.0 'SETUP-002 Complete'")
        print("  python scripts/maintenance/create_tag.py list")
        sys.exit(1)
    
    if sys.argv[1] == "list":
        list_tags()
    else:
        version = sys.argv[1]
        message = sys.argv[2] if len(sys.argv) > 2 else ""
        success = create_tag(version, message)
        sys.exit(0 if success else 1)

