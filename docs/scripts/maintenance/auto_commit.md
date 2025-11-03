# auto_commit.py Documentation

## File Location
`scripts/maintenance/auto_commit.py`

## Purpose
Automates the Git workflow by automatically staging, committing, and pushing changes to GitHub after task completion. This ensures consistent commit messages and eliminates manual Git operations.

## Why It Was Created
The project requires that every completed task be committed to GitHub. This script:
- Eliminates manual Git commands
- Ensures consistent commit message format
- Handles branch name standardization (master → main)
- Provides clear success/failure feedback
- Works even when Git isn't in PATH

## How It Works

### Main Functions

#### `find_git_command()`
**Purpose**: Locates the Git executable
**How it works**:
1. First tries running `git --version` directly
2. If that fails, checks common Windows installation paths:
   - `C:\Program Files\Git\cmd\git.exe`
   - `C:\Program Files (x86)\Git\cmd\git.exe`
   - `C:\Program Files\Git\bin\git.exe`
3. Returns the path to Git executable or `None` if not found

**Why this is needed**: Git may not be in PATH on Windows, so we need to find it manually.

#### `run_git_command(cmd_list, description)`
**Purpose**: Executes a Git command safely
**How it works**:
1. Gets Git command path using `find_git_command()`
2. Builds full command (handles both direct `git` and full paths)
3. Runs command with 30-second timeout
4. Captures output and errors
5. Returns `True` on success, `False` on failure
6. Prints formatted status messages

**Features**:
- Handles both `git` command and full `.exe` paths
- Provides clear error messages
- Shows command output (truncated to 100 chars)

#### `check_changes()`
**Purpose**: Checks if there are uncommitted changes
**How it works**:
1. Runs `git status --porcelain`
2. Returns `True` if output is non-empty (changes exist)

**Why**: Avoids creating empty commits.

#### `auto_commit(task_description)`
**Purpose**: Main function that orchestrates the auto-commit process
**How it works**:
1. **Verifies Git is available**: Checks if Git command exists
2. **Checks current branch**: Gets current branch name
3. **Renames branch if needed**: If branch is `master`, renames to `main`
4. **Checks for changes**: Skips if no changes exist
5. **Generates commit message**: Format: `feat: {task_description} - {timestamp}`
6. **Stages all changes**: `git add .`
7. **Creates commit**: `git commit -m "{message}"`
8. **Pushes to GitHub**: `git push origin main`
9. **Provides feedback**: Clear success/failure messages

### Configuration Constants
- `GITHUB_REPO`: Repository URL (`https://github.com/AIHUBMIND/zema-ai.git`)
- `REMOTE`: Remote name (`origin`)
- `BRANCH`: Branch name (`main`)

## Dependencies
- `subprocess`: Execute Git commands
- `sys`: Command-line arguments
- `pathlib.Path`: Path handling
- `datetime`: Timestamp generation

## Usage
```bash
# Basic usage (no description)
python scripts/maintenance/auto_commit.py

# With task description
python scripts/maintenance/auto_commit.py "Added configuration system"
```

## Commit Message Format
```
feat: {task_description} - YYYY-MM-DD HH:MM:SS
```

Example:
```
feat: Added configuration system - 2025-11-02 14:30:45
```

## Error Handling
The script handles:
- Git not found in PATH → Provides installation instructions
- Authentication failures → Provides GitHub authentication guidance
- Network issues → Commits locally, provides manual push instructions
- No changes → Skips commit gracefully

## Integration
This script is integrated into `.cursorrules` as a CRITICAL requirement:
- Must run after every task completion
- Part of the task completion checklist
- Ensures all work is version controlled

## Success Output
```
============================================================
AUTO-COMMIT TO GITHUB
============================================================

Repository: https://github.com/AIHUBMIND/zema-ai.git
Remote: origin
Branch: main

✓ Staging all changes
✓ Creating commit
✓ Pushing to origin/main

============================================================
✅ SUCCESS!
============================================================

Changes committed and pushed to:
  https://github.com/AIHUBMIND/zema-ai.git

View at: https://github.com/AIHUBMIND/zema-ai
```

## Failure Scenarios
If push fails:
- Commit is still created locally
- User can push manually later
- Clear instructions provided for authentication

## Security Notes
- Never commits `.env` files (handled by `.gitignore`)
- Never commits sensitive data
- Uses HTTPS for GitHub (no credentials stored)

