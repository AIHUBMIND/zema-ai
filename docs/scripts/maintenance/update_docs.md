# update_docs.py Documentation

## File Location
`scripts/maintenance/update_docs.py`

## Purpose
Automatically updates project documentation files after task completion. This ensures progress tracking files (`PROJECT_PROGRESS.md`, `CHECKPOINT.md`) stay synchronized with actual development progress.

## Why It Was Created
Manual documentation updates are error-prone and often forgotten. This script automates the process, ensuring:
- Progress tracking is always up-to-date
- Consistent formatting across documentation
- Timestamps are automatically updated
- Next steps are automatically calculated

## How It Works

### Main Class: `DocumentationUpdater`

#### `update_all(task_name, task_id, status)`
**Purpose**: Main orchestration method
**How it works**:
1. Updates `PROJECT_PROGRESS.md` with task completion
2. Updates `CHECKPOINT.md` with latest completed task
3. Updates code documentation (placeholder)
4. Prints progress messages

**Parameters**:
- `task_name`: Full task name (e.g., "SETUP-001 - Create Project Structure")
- `task_id`: Task ID (e.g., "SETUP-001")
- `status`: Task status ("complete", "in_progress", "pending")

#### `update_progress_tracker(task_name, task_id, status)`
**Purpose**: Updates `PROJECT_PROGRESS.md`
**How it works**:
1. Reads `docs/progress/PROJECT_PROGRESS.md`
2. Updates "Last Updated" timestamp using regex
3. If status is "complete":
   - Finds task section and marks as complete
   - Or adds new completion entry if task not found
   - Calculates next task ID (increments SETUP-XXX)
4. Updates "Next Step" field
5. Writes updated content back to file

**Regex Patterns Used**:
- `\*\*Last Updated:\*\* \d{4}-\d{2}-\d{2}` - Matches timestamp line
- `### {task_id}:.*?\n\*\*Status:\*\* .*?\n` - Matches task section

#### `update_checkpoint(task_name, task_id, status)`
**Purpose**: Updates `CHECKPOINT.md`
**How it works**:
1. Reads `docs/progress/CHECKPOINT.md`
2. If status is "complete":
   - Updates "Last Completed" field
   - Calculates next step (increments task ID)
   - Updates "Next Step" field
3. Updates "Last Updated" timestamp
4. Writes updated content back

**Why CHECKPOINT.md matters**: Quick resume point for new chat sessions.

#### `update_code_documentation()`
**Purpose**: Placeholder for code documentation updates
**Current implementation**: Only prints placeholder message
**Future implementation**:
- Scan `src/` for new files
- Parse Python files using AST
- Generate documentation sections
- Update `CODE_DOCUMENTATION.md`

#### `get_current_checkpoint()`
**Purpose**: Read current checkpoint information
**Returns**: Dictionary with:
- `last_completed`: Last completed task name
- `next_step`: Next task name
- `status`: Current status

**Use case**: Can be used by other scripts to determine where to resume.

## Dependencies
- `ast`: Python AST parsing (for future code analysis)
- `re`: Regular expressions for pattern matching
- `pathlib.Path`: Path handling
- `datetime`: Timestamp generation
- `subprocess`: External process execution (not currently used)

## Usage
```bash
# After completing a task
python scripts/maintenance/update_docs.py "SETUP-001 - Create Project Structure" SETUP-001 complete

# For in-progress tasks
python scripts/maintenance/update_docs.py "SETUP-002 - Configuration System" SETUP-002 in_progress
```

## File Structure Expected

### PROJECT_PROGRESS.md Structure
```markdown
**Last Updated:** YYYY-MM-DD

### SETUP-001: Task Name ✅ COMPLETE
**Status:** ✅ Complete
**Completed:** YYYY-MM-DD

**Next Step:** SETUP-002 - Next Step
```

### CHECKPOINT.md Structure
```markdown
**📌 Last Completed:** SETUP-001 - Task Name
**⏭️ Next Step:** SETUP-002 - Next Step
**Last Updated:** YYYY-MM-DD
```

## Integration
This script is integrated into the project workflow:
- Called automatically after `auto_commit.py`
- Part of task completion checklist in `.cursorrules`
- Can be called manually for corrections

## Error Handling
- Checks if files exist before reading
- Provides warning messages if files missing
- Uses `encoding='utf-8'` to handle Unicode correctly
- Gracefully handles missing sections

## Future Enhancements
- Full code documentation generation
- Automatic function/class documentation extraction
- Architecture diagram updates
- Dependency graph generation

