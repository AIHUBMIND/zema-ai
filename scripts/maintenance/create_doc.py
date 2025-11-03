#!/usr/bin/env python3
"""
Auto-Documentation Generator
Creates documentation template for new Python files
"""

import ast
import sys
from pathlib import Path
from typing import Optional, List, Dict


def get_file_info(python_file: Path) -> Dict[str, any]:
    """Extract information from Python file"""
    try:
        content = python_file.read_text(encoding='utf-8')
        tree = ast.parse(content, filename=str(python_file))
        
        info = {
            "module_docstring": ast.get_docstring(tree) or "",
            "classes": [],
            "functions": [],
            "imports": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                info["classes"].append({
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or ""
                })
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if isinstance(node, ast.FunctionDef):
                    # Only top-level functions
                    for parent in ast.walk(tree):
                        if isinstance(parent, (ast.ClassDef, ast.FunctionDef)):
                            if node in ast.walk(parent):
                                break
                    else:
                        info["functions"].append({
                            "name": node.name,
                            "docstring": ast.get_docstring(node) or "",
                            "is_async": False
                        })
                else:
                    info["functions"].append({
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "is_async": True
                    })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    info["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    info["imports"].append(f"{module}.{alias.name}")
        
        return info
    except Exception as e:
        print(f"Error parsing file: {e}", file=sys.stderr)
        return {"module_docstring": "", "classes": [], "functions": [], "imports": []}


def generate_doc_template(python_file: Path, doc_file: Path) -> str:
    """Generate documentation template"""
    relative_path = python_file.relative_to(Path.cwd())
    doc_relative_path = doc_file.relative_to(Path.cwd())
    
    info = get_file_info(python_file)
    
    # Determine folder and purpose based on path
    folder_purpose = {
        "src/core": "Core system components",
        "src/config": "Configuration management",
        "src/voice": "Voice processing",
        "src/vision": "Vision processing",
        "src/ai": "AI/LLM components",
        "src/tools": "Personal assistant tools",
        "src/api": "FastAPI server and routes",
        "src/utils": "Utility functions",
        "scripts/maintenance": "Maintenance scripts",
        "scripts/setup": "Setup scripts",
    }
    
    folder = str(relative_path.parent)
    purpose_hint = folder_purpose.get(folder, "Project component")
    
    template = f"""# {relative_path.name} Documentation

## File Location
`{relative_path}`

## Purpose
{f"TODO: Describe what this file does. {info['module_docstring'][:100] if info['module_docstring'] else purpose_hint}"}

## Why It Was Created
TODO: Explain the context and reasoning for creating this file. What problem does it solve?

## How It Works

"""
    
    if info["classes"]:
        template += "### Classes\n\n"
        for cls in info["classes"]:
            template += f"#### `{cls['name']}`\n"
            template += f"**Purpose**: {cls['docstring'][:100] if cls['docstring'] else 'TODO: Describe class purpose'}\n\n"
            template += "**How it works**:\n"
            template += "TODO: Detailed explanation\n\n"
    
    if info["functions"]:
        template += "### Functions\n\n"
        for func in info["functions"]:
            async_prefix = "async " if func["is_async"] else ""
            template += f"#### `{async_prefix}{func['name']}()`\n"
            template += f"**Purpose**: {func['docstring'][:100] if func['docstring'] else 'TODO: Describe function purpose'}\n\n"
            template += "**How it works**:\n"
            template += "TODO: Detailed explanation\n\n"
    
    template += f"""## Dependencies
TODO: List required libraries/modules

"""
    
    if info["imports"]:
        template += "**Imports used**:\n"
        for imp in info["imports"][:10]:  # Limit to first 10
            template += f"- `{imp}`\n"
        template += "\n"
    
    template += f"""## Usage
```python
# TODO: Add usage examples
from {relative_path.parent.as_posix().replace('/', '.')} import ...

# Example usage
```

## Integration
TODO: Explain how this file fits into the project architecture

## Current Status
- ⏳ Implementation status (TODO/In Progress/Complete)
- 📝 Notes about current implementation

## Future Enhancements
- TODO: Planned improvements or features
"""
    
    return template


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python create_doc.py <python_file_path>")
        print("Example: python create_doc.py src/voice/wakeword.py")
        sys.exit(1)
    
    python_file = Path(sys.argv[1])
    
    if not python_file.exists():
        print(f"Error: File not found: {python_file}")
        sys.exit(1)
    
    if not python_file.suffix == ".py":
        print(f"Error: Not a Python file: {python_file}")
        sys.exit(1)
    
    # Create corresponding doc file path
    # Remove 'src/' or 'scripts/' prefix and add 'docs/' prefix
    relative = python_file.relative_to(Path.cwd())
    doc_file = Path("docs") / relative.with_suffix(".md")
    
    # Create directory if needed
    doc_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if doc already exists
    if doc_file.exists():
        response = input(f"Documentation file exists: {doc_file}\nOverwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    # Generate template
    template = generate_doc_template(python_file, doc_file)
    
    # Write file
    doc_file.write_text(template, encoding='utf-8')
    
    print(f"✅ Created documentation template: {doc_file}")
    print(f"   Please fill in the TODO sections with actual content")


if __name__ == "__main__":
    main()

