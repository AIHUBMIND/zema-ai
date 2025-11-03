# check_git_status.py Documentation

## File Location
`scripts/maintenance/check_git_status.py`

## Purpose
Checks Git repository status and provides instructions for GitHub setup. Useful for verifying Git configuration and getting guidance on connecting to GitHub.

## Why It Was Created
During initial setup, developers needed to:
- Verify Git repository was initialized
- Check if GitHub remote was configured
- Get instructions for GitHub setup
- Understand Git repository status

## How It Works

### Function: `check_git_status()`
**Purpose**: Checks Git repository initialization status
**How it works**:
1. Checks if `.git/` directory exists
2. If exists:
   - Reports Git is initialized
   - Checks if `.git/config` file exists
   - Reads config file to check for remote configuration
   - Prints remote URL if configured
   - Warns if no remote configured
3. Returns `True` if initialized, `False` otherwise

**Checks Performed**:
- `.git/` folder existence
- `.git/config` file existence
- `[remote` section in config (indicates remote configured)
- Remote URL display

### Function: `generate_github_setup_instructions()`
**Purpose**: Generates detailed GitHub setup instructions
**How it works**:
1. Prints three setup options:
   - **Option 1**: Manual GitHub repo creation (Recommended)
   - **Option 2**: Using GitHub CLI
   - **Option 3**: Script-based setup
2. Provides step-by-step instructions for each option
3. Includes exact commands to run

**Options Provided**:

#### Option 1: Manual Setup (Recommended)
1. Go to https://github.com/new
2. Create repository with specific settings
3. Run provided Git commands

#### Option 2: GitHub CLI
- Single command using `gh` CLI tool
- Requires GitHub CLI installation

#### Option 3: Script-Based
- Mentions script can be created
- Requires user input (username, repo name, visibility)

## Dependencies
- `pathlib.Path`: Path handling
- `sys`: System operations (for exit codes)

## Usage
```bash
# From project root
python scripts/maintenance/check_git_status.py
```

## Output Format
```
============================================================
GIT REPOSITORY STATUS
============================================================

✓ Git repository initialized (.git/ folder exists)
✓ Git config file exists
✓ Remote repository configured

Current remote configuration:
  [remote "origin"]
          url = https://github.com/AIHUBMIND/zema-ai.git

============================================================
GITHUB REPOSITORY SETUP OPTIONS
============================================================

OPTION 1: Create GitHub repo manually (Recommended)
------------------------------------------------------------
1. Go to https://github.com/new
2. Repository name: zema-ai
...
```

## Integration
This script is useful for:
- Initial project setup verification
- Troubleshooting Git issues
- Getting GitHub setup guidance
- Verifying remote configuration

## When to Use
- After initial `git init`
- When setting up GitHub remote
- When troubleshooting Git issues
- When verifying repository status

## Related Scripts
- `scripts/setup/connect_github.py`: Actually connects to GitHub
- `scripts/setup/setup_github_remote.py`: Interactive GitHub setup
- `scripts/maintenance/auto_commit.py`: Uses Git for commits

## Notes
- Doesn't require Git to be in PATH (checks `.git/` folder directly)
- Provides helpful instructions even if Git command not available
- Non-destructive (only reads, doesn't modify)

