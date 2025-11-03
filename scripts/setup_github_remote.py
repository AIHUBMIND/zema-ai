#!/usr/bin/env python3
"""Script to configure GitHub remote repository."""
import sys
from pathlib import Path

print("=" * 60)
print("GITHUB REMOTE SETUP SCRIPT")
print("=" * 60)
print()

# Get GitHub details
github_username = input("Enter your GitHub username: ").strip()
repo_name = input("Enter repository name (default: zema-ai): ").strip() or "zema-ai"
is_private = input("Is repository private? (y/n, default: y): ").strip().lower() != "n"

print()
print(f"Configuration:")
print(f"  Username: {github_username}")
print(f"  Repository: {repo_name}")
print(f"  Visibility: {'Private' if is_private else 'Public'}")
print()

confirm = input("Create GitHub repository and configure remote? (y/n): ").strip().lower()
if confirm != "y":
    print("Cancelled.")
    sys.exit(0)

print()
print("=" * 60)
print("SETUP INSTRUCTIONS")
print("=" * 60)
print()

print("STEP 1: Create GitHub Repository")
print("-" * 60)
print(f"""
1. Go to: https://github.com/new
2. Repository name: {repo_name}
3. Description: Privacy-first voice assistant for mini PC
4. Visibility: {'Private' if is_private else 'Public'}
5. DO NOT initialize with README, .gitignore, or license
6. Click "Create repository"
""")

input("Press Enter after you've created the repository...")

print()
print("STEP 2: Configure Remote")
print("-" * 60)

remote_url = f"https://github.com/{github_username}/{repo_name}.git"

print(f"Remote URL: {remote_url}")
print()

# Generate commands
commands = f"""
# Add remote repository
git remote add origin {remote_url}

# Set main branch
git branch -M main

# Stage all files
git add .

# Initial commit
git commit -m "Initial commit: Zema AI project setup"

# Push to GitHub
git push -u origin main
"""

print("Run these commands:")
print("-" * 60)
print(commands)

print()
print("=" * 60)
print("ALTERNATIVE: Use GitHub CLI")
print("=" * 60)
print()
print("If you have GitHub CLI installed, you can run:")
print(f"  gh repo create {repo_name} --{'private' if is_private else 'public'} --source=. --remote=origin --push")
print()

