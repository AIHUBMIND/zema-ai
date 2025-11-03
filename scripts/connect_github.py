#!/usr/bin/env python3
"""Connect local Git repository to GitHub and push initial commit."""
import subprocess
import sys
from pathlib import Path

GITHUB_URL = "https://github.com/AIHUBMIND/zema-ai.git"
REMOTE_NAME = "origin"
BRANCH_NAME = "main"

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"   ✓ Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()[:100]}")
            return True
        else:
            print(f"   ✗ Failed")
            print(f"   Error: {result.stderr.strip()[:200]}")
            return False
    except FileNotFoundError:
        print(f"   ✗ Git command not found")
        print(f"   Make sure Git is installed and in PATH")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("GITHUB REMOTE SETUP")
    print("=" * 60)
    print(f"\nRepository: {GITHUB_URL}")
    print(f"Remote name: {REMOTE_NAME}")
    print(f"Branch: {BRANCH_NAME}")
    print()
    
    # Check if git is available
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Git found: {result.stdout.strip()}")
        else:
            print("✗ Git command failed")
            sys.exit(1)
    except FileNotFoundError:
        print("✗ Git command not found in PATH")
        print("\nPlease ensure Git is installed and accessible.")
        print("\nManual steps:")
        print(f"1. git remote add origin {GITHUB_URL}")
        print(f"2. git branch -M main")
        print(f"3. git add .")
        print(f"4. git commit -m 'Initial commit: Zema AI project setup'")
        print(f"5. git push -u origin main")
        sys.exit(1)
    
    # Check if remote already exists
    result = subprocess.run(
        ["git", "remote", "get-url", REMOTE_NAME],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        existing_url = result.stdout.strip()
        print(f"\n⚠ Remote '{REMOTE_NAME}' already exists:")
        print(f"   {existing_url}")
        
        if existing_url != GITHUB_URL:
            overwrite = input(f"\nReplace with {GITHUB_URL}? (y/n): ").strip().lower()
            if overwrite == "y":
                run_command(["git", "remote", "set-url", REMOTE_NAME, GITHUB_URL], 
                           f"Updating remote URL")
            else:
                print("Keeping existing remote")
        else:
            print("✓ Remote URL is correct")
    else:
        # Add remote
        run_command(["git", "remote", "add", REMOTE_NAME, GITHUB_URL],
                   f"Adding remote '{REMOTE_NAME}'")
    
    # Set branch name
    run_command(["git", "branch", "-M", BRANCH_NAME],
               f"Setting branch to '{BRANCH_NAME}'")
    
    # Stage all files
    run_command(["git", "add", "."],
               "Staging all files")
    
    # Check if there are changes to commit
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        # Make initial commit
        commit_msg = "Initial commit: Zema AI project setup"
        run_command(["git", "commit", "-m", commit_msg],
                   f"Creating initial commit")
    else:
        print("\n⚠ No changes to commit (all files already committed)")
    
    # Push to GitHub
    print("\n" + "=" * 60)
    print("PUSHING TO GITHUB")
    print("=" * 60)
    print("\n⚠ This will push your code to GitHub.")
    print("   Make sure you're authenticated (GitHub CLI or SSH keys)")
    
    push_ok = input("\nPush to GitHub now? (y/n): ").strip().lower()
    
    if push_ok == "y":
        success = run_command(
            ["git", "push", "-u", REMOTE_NAME, BRANCH_NAME],
            f"Pushing to {REMOTE_NAME}/{BRANCH_NAME}"
        )
        
        if success:
            print("\n" + "=" * 60)
            print("✅ SUCCESS!")
            print("=" * 60)
            print(f"\nYour code has been pushed to:")
            print(f"  {GITHUB_URL}")
            print("\nYou can view it at:")
            print(f"  https://github.com/AIHUBMIND/zema-ai")
        else:
            print("\n" + "=" * 60)
            print("⚠️  PUSH FAILED")
            print("=" * 60)
            print("\nPossible issues:")
            print("1. Not authenticated with GitHub")
            print("   - Use: gh auth login (GitHub CLI)")
            print("   - Or: Set up SSH keys")
            print("2. Authentication token needed")
            print("   - Generate token: https://github.com/settings/tokens")
            print("\nYou can push manually later with:")
            print(f"  git push -u {REMOTE_NAME} {BRANCH_NAME}")
    else:
        print("\n✓ Remote configured successfully")
        print("\nYou can push manually later with:")
        print(f"  git push -u {REMOTE_NAME} {BRANCH_NAME}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

