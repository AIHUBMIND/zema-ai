# check_docs.py Documentation

## File Location
`scripts/maintenance/check_docs.py`

## Purpose
Prevents creating duplicate markdown files by checking if similar content already exists. This enforces the documentation policy of updating existing files rather than creating new ones.

## Why It Was Created
The project had a problem where duplicate markdown files were being created for similar content. This script:
- Enforces the "append/update existing files" policy
- Prevents documentation fragmentation
- Maintains documentation organization
- Provides clear guidance on where to add content

## How It Works

### Main Class: `DocumentationManager`

#### `find_existing_file(content_type, topic)`
**Purpose**: Finds existing file for a given content type
**How it works**:
1. Looks up content type in `file_mapping` dictionary
2. If target is a directory:
   - Searches for files matching topic keyword
   - Returns first matching file or first file in directory
3. If target is a specific file:
   - Returns path if file exists
   - Returns `None` if not found

**Content Types Mapped**:
- `progress` → `docs/progress/PROJECT_PROGRESS.md`
- `checkpoint` → `docs/progress/CHECKPOINT.md`
- `architecture` → `docs/architecture/ARCHITECTURE.md`
- `code` → `docs/architecture/CODE_DOCUMENTATION.md`
- `structure` → `docs/README.md`
- `setup` → `docs/setup/` (directory)
- `git` → `docs/git/` (directory)
- `hardware` → `docs/hardware/` (directory)
- `development` → `docs/development/` (directory)

#### `should_create_new_file(proposed_filename, content_type)`
**Purpose**: Determines if a new file should be created
**How it works**:
1. **Checks if file already exists**: Returns `False` if file exists
2. **Checks for similar content**: Looks up existing file for content type
3. **Checks for similar filenames**: Compares proposed filename with existing files
4. **Special handling**: Always allows files in `docs/guides/` folder
5. **Returns**: Tuple of `(should_create: bool, reason: str)`

**Return Values**:
- `(False, "File already exists: ...")` - File exists
- `(False, "Similar content exists in: ...")` - Should append to existing
- `(True, "New guide file - OK to create")` - Guides folder file
- `(True, "New file - but verify...")` - New file, but verify

#### `_similar_filename(name1, name2)`
**Purpose**: Checks if two filenames are similar
**How it works**:
1. Normalizes filenames (lowercase, remove `_` and `-`)
2. Checks for exact match
3. Checks if one contains the other
4. Checks for common words (structure, documentation, guide, setup, progress, architecture)
5. Returns `True` if similar, `False` otherwise

**Why this matters**: Prevents `STRUCTURE.md` and `structure.md` duplicates.

#### `get_append_location(content_type, topic)`
**Purpose**: Gets file where content should be appended
**Returns**: Path to existing file where content should be added

**Use case**: When creating new content, tells you where to add it instead.

### Helper Function: `check_before_create()`
**Purpose**: Standalone function for command-line usage
**How it works**:
1. Creates `DocumentationManager` instance
2. Calls `should_create_new_file()`
3. Returns result tuple

## Dependencies
- `pathlib.Path`: Path handling
- `re`: Regular expressions (for future enhancements)
- `typing`: Type hints

## Usage

### Command Line
```bash
# Check if file should be created
python scripts/maintenance/check_docs.py docs/new_file.md setup

# Output:
# ✅ OK to create: docs/new_file.md
#    Note: New file - but verify if similar content exists elsewhere

# Or:
# ❌ DO NOT CREATE: docs/new_file.md
#    Reason: Similar content exists in: docs/setup/SETUP.md. Append to that file instead.
```

### In Python Code
```python
from scripts.maintenance.check_docs import check_before_create

should_create, message = check_before_create("docs/new_structure.md", "structure")
if not should_create:
    print(f"Don't create: {message}")
```

## File Mapping Configuration
The `file_mapping` dictionary maps content types to existing files:
```python
{
    "progress": "docs/progress/PROJECT_PROGRESS.md",
    "checkpoint": "docs/progress/CHECKPOINT.md",
    "architecture": "docs/architecture/ARCHITECTURE.md",
    "code": "docs/architecture/CODE_DOCUMENTATION.md",
    "structure": "docs/README.md",
    "setup": "docs/setup/",  # Directory
    "git": "docs/git/",      # Directory
    # ...
}
```

## Integration
This script is integrated into:
- `.cursorrules`: Documentation policy enforcement
- Development workflow: Run before creating new docs
- CI/CD: Can be used to prevent duplicate files in PRs

## Examples

### Example 1: Duplicate Prevention
```bash
$ python scripts/maintenance/check_docs.py docs/structure.md structure
❌ DO NOT CREATE: docs/structure.md
   Reason: Similar content exists in: docs/README.md. Append to that file instead.
```

### Example 2: OK to Create
```bash
$ python scripts/maintenance/check_docs.py docs/guides/new_guide.md guide
✅ OK to create: docs/guides/new_guide.md
   Note: New guide file - OK to create
```

### Example 3: File Already Exists
```bash
$ python scripts/maintenance/check_docs.py docs/progress/PROJECT_PROGRESS.md progress
❌ DO NOT CREATE: docs/progress/PROJECT_PROGRESS.md
   Reason: File already exists: docs/progress/PROJECT_PROGRESS.md
```

## Benefits
1. **Prevents duplication**: No more duplicate documentation files
2. **Maintains organization**: Keeps documentation structure clean
3. **Clear guidance**: Tells you exactly where to add content
4. **Enforces policy**: Makes it easy to follow documentation rules

## Limitations
- Only checks filename similarity, not content similarity
- Requires manual content type specification
- Doesn't analyze actual file content (future enhancement)

## Future Enhancements
- Content similarity analysis using text comparison
- Automatic content type detection
- Integration with Git hooks
- Webhook support for automated checking

