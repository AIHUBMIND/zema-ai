# check_rules_compliance.py Documentation

## File Location
`scripts/maintenance/check_rules_compliance.py`

## Purpose
Verifies that all code in the project complies with the rules defined in `.cursorrules`. This includes checking for PEP 8 compliance, type hints, docstrings, async/await usage, and project structure.

## Why It Was Created
To ensure code quality and consistency across the project. The `.cursorrules` file defines many requirements (PEP 8, type hints, docstrings, etc.), and this script automates checking for violations.

## How It Works

### Main Class: `RuleChecker`

#### `check_all()`
**Purpose**: Runs all compliance checks
**How it works**:
1. Checks project structure
2. Checks Python files for style violations
3. Checks dependencies
4. Checks Git workflow compliance
5. Prints summary report

**Returns**: Dictionary with violations and statistics

#### `check_project_structure()`
**Purpose**: Verifies required directories exist
**How it works**:
1. Checks for required directories:
   - `src/core`
   - `src/config`
   - `src/voice`
   - `src/vision`
   - `src/ai`
   - `src/tools`
   - `src/api`
   - `src/utils`
2. Reports missing directories

#### `check_python_files()`
**Purpose**: Checks all Python files for compliance
**How it works**:
1. Finds all `.py` files in `src/`
2. Parses each file using AST (Abstract Syntax Tree)
3. Checks for:
   - Module docstrings
   - Function/class docstrings
   - Type hints on functions
   - Async/await preference for I/O operations
4. Records violations by category

#### `check_file_docstring(file_path, content, tree)`
**Purpose**: Verifies file has module docstring
**How it works**:
1. Uses `ast.get_docstring()` to check for docstring
2. Allows empty `__init__.py` files
3. Reports missing docstrings

#### `check_functions_and_classes(file_path, tree)`
**Purpose**: Checks functions and classes for type hints and docstrings
**How it works**:
1. Walks AST tree to find all functions and classes
2. For each function:
   - Checks for return type hints
   - Checks for parameter type hints
   - Checks for docstring
   - Allows `__init__` methods without return type
   - Allows private methods (starting with `_`) without docstrings
3. For each class:
   - Checks for docstring
4. Records violations with file path and line number

#### `check_imports(file_path, tree)`
**Purpose**: Checks for async/await preference
**How it works**:
1. Finds sync file operations (`open`, `read`, `write`) in async functions
2. Suggests using `aiofiles` instead
3. Warns about sync I/O in async contexts

#### `check_dependencies()`
**Purpose**: Verifies required dependencies are in `requirements.txt`
**How it works**:
1. Reads `requirements.txt`
2. Checks for required packages:
   - `fastapi`
   - `pydantic`
   - `sqlalchemy`
   - `pyaudio`
   - `opencv-python`
   - `faster-whisper`
3. Reports missing dependencies

#### `check_git_workflow()`
**Purpose**: Verifies Git workflow compliance
**How it works**:
1. Checks for `scripts/auto_commit.py` (or `scripts/maintenance/auto_commit.py`)
2. Checks `.gitignore` contains required patterns:
   - `.env`
   - `venv/`
   - `__pycache__/`
   - `*.log`
   - `data/db/`

## Dependencies
- `ast`: Python AST parsing
- `re`: Regular expressions
- `pathlib.Path`: Path handling
- `collections.defaultdict`: Efficient violation tracking

## Usage
```bash
# From project root
python scripts/maintenance/check_rules_compliance.py
```

## Output Format
The script prints:
1. **Section headers** for each check type
2. **Check marks** (✓) for passing checks
3. **Violation markers** (✗) for failures
4. **Summary statistics**:
   - Python files checked
   - Functions found
   - Classes found
   - Directories found
   - Dependencies found
5. **Violations grouped by category**:
   - Structure violations
   - Type hint violations
   - Docstring violations
   - Dependency violations
   - Git workflow violations

## Example Output
```
============================================================
CURSOR RULES COMPLIANCE CHECK
============================================================

📁 Checking Project Structure...
  ✓ src/core
  ✓ src/config
  ...

🐍 Checking Python Code Style...
  Checking src/main.py...
  ✓ File has docstring
  ✗ Function 'start' missing type hints

📦 Checking Dependencies...
  ✓ fastapi
  ✓ pydantic
  ...

============================================================
COMPLIANCE SUMMARY
============================================================

📊 Statistics:
  • Python files checked: 45
  • Functions found: 120
  • Classes found: 30
  • Directories: 8/8
  • Dependencies: 6/6

⚠️  Violations Found: 5

❌ Compliance Issues Found:

  TYPE_HINTS (3 issues):
    • src/main.py:12 - Function 'start' missing type hints
    • src/api/server.py:45 - Async function 'websocket_endpoint' missing type hints
    ...
```

## Exit Code
- `0`: All checks passed (no violations)
- `1`: Violations found (can be used in CI/CD)

## Integration
This script can be integrated into:
- Pre-commit hooks
- CI/CD pipelines
- Development workflow (run before committing)

## Fixing Violations
Common violations and fixes:

1. **Missing type hints**: Add return type and parameter types
   ```python
   # Before
   def process_data(data):
       return data.upper()
   
   # After
   def process_data(data: str) -> str:
       return data.upper()
   ```

2. **Missing docstrings**: Add docstring explaining purpose
   ```python
   # Before
   def calculate_total(items):
       return sum(items)
   
   # After
   def calculate_total(items: List[float]) -> float:
       """Calculate total of all items."""
       return sum(items)
   ```

3. **Sync I/O in async**: Use `aiofiles` instead
   ```python
   # Before (in async function)
   with open('file.txt') as f:
       content = f.read()
   
   # After
   async with aiofiles.open('file.txt') as f:
       content = await f.read()
   ```

