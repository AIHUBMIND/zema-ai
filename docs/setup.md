# setup.py Documentation

## File Location
`setup.py` (root level)

## Purpose
Python package setup script using setuptools. Allows the project to be installed as a package, making imports easier and enabling distribution.

## Why It Was Created
Standard Python projects use `setup.py` for:
- Package installation (`pip install -e .`)
- Distribution packaging
- Entry point definition
- Dependency management
- Metadata definition

## How It Works

### Package Configuration
```python
setup(
    name="zema-ai",
    version="0.1.0",
    author="Zema AI Team",
    description="Privacy-first voice assistant for mini PC",
    ...
)
```

### Key Sections

#### Package Discovery
```python
packages=find_packages(where="src"),
package_dir={"": "src"},
```
- Finds all packages in `src/` directory
- Sets `src/` as root package directory
- Enables imports like `from core import ...` instead of `from src.core import ...`

#### Dependencies
```python
install_requires=requirements,
```
- Reads `requirements.txt` and installs all dependencies
- Ensures all required packages are installed

#### Development Dependencies
```python
extras_require={
    "dev": [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "black",
        "flake8",
        "mypy",
    ],
}
```
- Optional dev dependencies
- Install with: `pip install -e .[dev]`

#### Entry Points
```python
entry_points={
    "console_scripts": [
        "zema=core.main:main",
    ],
}
```
- Creates `zema` command-line tool
- Points to `main()` function in `core.main` module
- Allows running: `zema` instead of `python -m src.main`

## Dependencies
- `setuptools`: Package setup and distribution
- Reads `README.md` for long description
- Reads `requirements.txt` for dependencies

## Usage

### Install Package (Editable Mode)
```bash
# From project root
pip install -e .

# With dev dependencies
pip install -e .[dev]
```

### What This Does
- Installs package in editable mode (changes reflect immediately)
- Makes imports work: `from core import ...`
- Creates `zema` command-line tool
- Installs all dependencies from `requirements.txt`

### Build Distribution
```bash
# Create source distribution
python setup.py sdist

# Create wheel distribution
python setup.py bdist_wheel
```

## Benefits
1. **Easier imports**: No need for `sys.path` manipulation
2. **Standard structure**: Follows Python packaging conventions
3. **CLI tool**: Creates `zema` command
4. **Distribution ready**: Can be packaged for PyPI
5. **Development mode**: Editable install for development

## Project Structure Expected
```
zema-ai/
├── setup.py           # This file
├── README.md          # Long description source
├── requirements.txt   # Dependencies source
└── src/               # Package source
    ├── core/
    ├── config/
    └── ...
```

## Entry Point Explanation
```python
"zema=core.main:main"
```
- `zema`: Command name (what user types)
- `core.main`: Module path (`src/core/main.py`)
- `main`: Function name to call

**Note**: Currently points to `core.main:main`, but actual entry point is `src/main.py`. This may need updating.

## Metadata Fields
- `name`: Package name
- `version`: Package version (should match `src/__init__.py`)
- `author`: Author/team name
- `description`: Short description
- `long_description`: From README.md
- `url`: Project URL (GitHub)
- `classifiers`: PyPI metadata (status, audience, license, Python versions)
- `python_requires`: Minimum Python version (3.11+)

## Future Enhancements
- Fix entry point to point to `src.main:main`
- Add more metadata (license, keywords, etc.)
- Add setup.cfg for modern configuration
- Consider migrating to `pyproject.toml` (modern standard)

## Related Files
- `pyproject.toml`: Modern Python project configuration
- `requirements.txt`: Dependency list
- `README.md`: Project description
- `src/__init__.py`: Package version

