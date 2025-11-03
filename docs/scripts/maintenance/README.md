# Maintenance Scripts Folder

## Purpose
The `scripts/maintenance/` folder contains scripts for ongoing maintenance, monitoring, and quality assurance tasks. These scripts help ensure code quality, automate repetitive tasks, and monitor system health.

## Files in This Folder

### `benchmark.py`
System performance benchmarking script. Measures CPU, memory, and disk performance to establish baseline metrics for the BOSGAME P3 Lite mini PC.

### `auto_commit.py`
Automated Git workflow script. Automatically stages, commits, and pushes changes to GitHub after task completion.

### `check_rules_compliance.py`
Code compliance checker. Verifies that all code follows the rules defined in `.cursorrules` (PEP 8, type hints, docstrings, etc.).

### `update_docs.py`
Documentation updater. Automatically updates progress tracking files (`PROJECT_PROGRESS.md`, `CHECKPOINT.md`) after task completion.

### `check_docs.py`
Documentation manager. Prevents creating duplicate markdown files by checking if similar content already exists.

### `check_git_status.py`
Git status checker. Verifies Git repository initialization and remote configuration status.

## Usage Pattern
These scripts are typically run after completing a development task:
```bash
# After completing a task
python scripts/maintenance/auto_commit.py "Task description"
python scripts/maintenance/update_docs.py "Task Name" TASK-ID complete
python scripts/maintenance/check_rules_compliance.py
```

## Integration
These scripts are integrated into the project workflow via `.cursorrules` to ensure they run automatically after each task completion.

