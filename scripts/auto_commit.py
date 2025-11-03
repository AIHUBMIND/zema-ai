#!/usr/bin/env python3
"""Auto-commit and push to GitHub after task completion."""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

GITHUB_REPO = "https://github.com/AIHUBMIND/zema-ai.git"
REMOTE = "origin"
BRANCH = "main"

def find_git_command():
    """Find git command path."""
    # Common Git installation paths on Windows
    possible_paths = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe",
    ]
    
    # Try direct git command first
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
    
    # Try full paths
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
        print("\nPlease ensure Git is installed and accessible.")
        print("Or add Git to PATH:")
        print("  $env:Path += ';C:\\Program Files\\Git\\cmd'")
        return False
    
    # Build command
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
                output = result.stdout.strip()[:100]
                if output:
                    print(f"  {output}")
            return True
        else:
            print(f"✗ {description}")
            if result.stderr:
                error = result.stderr.strip()[:200]
                if error:
                    print(f"  Error: {error}")
            return False
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Error: {e}")
        return False

def check_changes():
    """Check if there are uncommitted changes."""
    git_cmd = find_git_command()
    if not git_cmd:
        return False
    
    cmd_list = ["status", "--porcelain"]
    if isinstance(git_cmd, str) and git_cmd.endswith(".exe"):
        full_cmd = [git_cmd] + cmd_list
    else:
        full_cmd = ["git"] + cmd_list
    
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        return bool(result.stdout.strip())
    except:
        return False

def auto_commit(task_description=""):
    """Automatically commit and push changes."""
    print("=" * 60)
    print("AUTO-COMMIT TO GITHUB")
    print("=" * 60)
    print(f"\nRepository: {GITHUB_REPO}")
    print(f"Remote: {REMOTE}")
    print(f"Branch: {BRANCH}")
    print()
    
    # Check if Git is available
    git_cmd = find_git_command()
    if not git_cmd:
        print("⚠ Git command not found")
        print("\nPlease:")
        print("1. Install Git: https://git-scm.com/downloads")
        print("2. Or add to PATH: $env:Path += ';C:\\Program Files\\Git\\cmd'")
        return False
    
    print(f"✓ Using Git: {git_cmd}")
    print()
    
    # Check if there are changes
    if not check_changes():
        print("ℹ No changes to commit")
        return True
    
    # Generate commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if task_description:
        commit_msg = f"feat: {task_description} - {timestamp}"
    else:
        commit_msg = f"chore: Auto-commit - {timestamp}"
    
    print(f"Commit message: {commit_msg}")
    print()
    
    # Stage all changes
    if not run_git_command(["add", "."], "Staging all changes"):
        return False
    
    # Commit
    if not run_git_command(["commit", "-m", commit_msg], "Creating commit"):
        return False
    
    # Push
    print()
    print("=" * 60)
    print("PUSHING TO GITHUB")
    print("=" * 60)
    print()
    
    push_success = run_git_command(["push", REMOTE, BRANCH], f"Pushing to {REMOTE}/{BRANCH}")
    
    if push_success:
        print()
        print("=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"\nChanges committed and pushed to:")
        print(f"  {GITHUB_REPO}")
        print(f"\nView at: https://github.com/AIHUBMIND/zema-ai")
    else:
        print()
        print("=" * 60)
        print("⚠️  PUSH FAILED")
        print("=" * 60)
        print("\nCommit was created locally, but push failed.")
        print("\nPossible issues:")
        print("1. Not authenticated with GitHub")
        print("   - Use: gh auth login (GitHub CLI)")
        print("   - Or: Set up SSH keys")
        print("2. Authentication token needed")
        print("   - Generate: https://github.com/settings/tokens")
        print("\nYou can push manually later with:")
        print(f"  git push {REMOTE} {BRANCH}")
    
    return push_success

if __name__ == "__main__":
    task_desc = sys.argv[1] if len(sys.argv) > 1 else ""
    success = auto_commit(task_desc)
    sys.exit(0 if success else 1)
