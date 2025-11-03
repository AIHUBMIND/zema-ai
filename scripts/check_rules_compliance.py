"""
Cursor Rules Compliance Checker
Verifies codebase compliance with .cursorrules requirements
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any
from collections import defaultdict


class RuleChecker:
    """Checks compliance with .cursorrules"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_root = project_root / "src"
        self.violations: Dict[str, List[str]] = defaultdict(list)
        self.stats: Dict[str, int] = defaultdict(int)
        
    def check_all(self) -> Dict[str, Any]:
        """Run all compliance checks"""
        print("=" * 70)
        print("CURSOR RULES COMPLIANCE CHECK")
        print("=" * 70)
        print()
        
        # Check project structure
        print("📁 Checking Project Structure...")
        self.check_project_structure()
        
        # Check Python files
        print("\n🐍 Checking Python Code Style...")
        self.check_python_files()
        
        # Check dependencies
        print("\n📦 Checking Dependencies...")
        self.check_dependencies()
        
        # Check git workflow
        print("\n� Git Workflow Check...")
        self.check_git_workflow()
        
        # Print summary
        print("\n" + "=" * 70)
        print("COMPLIANCE SUMMARY")
        print("=" * 70)
        self.print_summary()
        
        return {
            "violations": dict(self.violations),
            "stats": dict(self.stats),
            "pass": len(self.violations) == 0
        }
    
    def check_project_structure(self):
        """Verify project structure matches .cursorrules"""
        required_dirs = {
            "src/core": "Core orchestrator, state management",
            "src/config": "Configuration management (Pydantic)",
            "src/voice": "Voice I/O, wake word, STT, TTS",
            "src/vision": "Camera, vision processing",
            "src/ai": "LLM client, context management",
            "src/tools": "Personal assistant tools",
            "src/api": "FastAPI server, routes",
            "src/utils": "Utilities, logging, helpers",
        }
        
        for dir_path, description in required_dirs.items():
            full_path = self.project_root / dir_path
            if full_path.exists():
                print(f"  ✓ {dir_path}")
                self.stats["directories_found"] += 1
            else:
                print(f"  ✗ {dir_path} - MISSING")
                self.violations["structure"].append(f"Missing directory: {dir_path}")
        
        self.stats["directories_required"] = len(required_dirs)
    
    def check_python_files(self):
        """Check Python files for compliance"""
        python_files = list(self.src_root.rglob("*.py"))
        
        for py_file in python_files:
            if "__pycache__" in str(py_file):
                continue
            
            self.stats["python_files_checked"] += 1
            
            # Read file content
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except Exception as e:
                self.violations["syntax"].append(f"{py_file}: Parse error - {e}")
                continue
            
            # Check file-level docstring
            self.check_file_docstring(py_file, content, tree)
            
            # Check functions and classes
            self.check_functions_and_classes(py_file, tree)
            
            # Check imports
            self.check_imports(py_file, tree)
    
    def check_file_docstring(self, file_path: Path, content: str, tree: ast.AST):
        """Check if file has module docstring"""
        if ast.get_docstring(tree) is None:
            rel_path = file_path.relative_to(self.project_root)
            if rel_path.name != "__init__.py":  # Allow empty __init__.py
                self.violations["docstrings"].append(
                    f"{rel_path}: Missing module docstring"
                )
    
    def check_functions_and_classes(self, file_path: Path, tree: ast.AST):
        """Check functions and classes for type hints and docstrings"""
        rel_path = file_path.relative_to(self.project_root)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for type hints
                if not node.returns and not self._has_type_hints(node):
                    # Allow __init__ methods without return type
                    if node.name != "__init__":
                        self.violations["type_hints"].append(
                            f"{rel_path}:{node.lineno} - Function '{node.name}' missing type hints"
                        )
                
                # Check for docstring
                if not ast.get_docstring(node):
                    # Allow private methods
                    if not node.name.startswith("_"):
                        self.violations["docstrings"].append(
                            f"{rel_path}:{node.lineno} - Function '{node.name}' missing docstring"
                        )
                
                self.stats["functions_found"] += 1
                
            elif isinstance(node, ast.AsyncFunctionDef):
                # Check for type hints
                if not node.returns and not self._has_type_hints(node):
                    self.violations["type_hints"].append(
                        f"{rel_path}:{node.lineno} - Async function '{node.name}' missing type hints"
                    )
                
                # Check for docstring
                if not ast.get_docstring(node):
                    if not node.name.startswith("_"):
                        self.violations["docstrings"].append(
                            f"{rel_path}:{node.lineno} - Async function '{node.name}' missing docstring"
                        )
                
                self.stats["async_functions_found"] += 1
                
            elif isinstance(node, ast.ClassDef):
                # Check for docstring
                if not ast.get_docstring(node):
                    self.violations["docstrings"].append(
                        f"{rel_path}:{node.lineno} - Class '{node.name}' missing docstring"
                    )
                
                self.stats["classes_found"] += 1
    
    def _has_type_hints(self, node: ast.FunctionDef) -> bool:
        """Check if function has type hints in annotations"""
        if node.args.args:
            return any(arg.annotation for arg in node.args.args)
        return False
    
    def check_imports(self, file_path: Path, tree: ast.AST):
        """Check imports for async/await preference"""
        rel_path = file_path.relative_to(self.project_root)
        
        # Check for sync I/O operations
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                # Warn about sync file operations when async alternatives exist
                sync_file_ops = ["open", "read", "write"]
                if func_name in sync_file_ops:
                    # Check if we're in an async function
                    parent = self._get_parent_function(node, tree)
                    if parent and isinstance(parent, ast.AsyncFunctionDef):
                        self.violations["async_preference"].append(
                            f"{rel_path}:{node.lineno} - Consider using aiofiles instead of sync '{func_name}'"
                        )
    
    def _get_parent_function(self, node: ast.AST, tree: ast.AST) -> ast.FunctionDef | None:
        """Get parent function node"""
        for parent in ast.walk(tree):
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for child in ast.walk(parent):
                    if child == node:
                        return parent
        return None
    
    def check_dependencies(self):
        """Check if required dependencies are in requirements.txt"""
        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            self.violations["dependencies"].append("requirements.txt not found")
            return
        
        requirements = req_file.read_text()
        
        required = {
            "fastapi": "FastAPI for web API",
            "pydantic": "Pydantic for validation",
            "sqlalchemy": "SQLAlchemy for database",
            "pyaudio": "PyAudio for audio I/O",
            "opencv-python": "OpenCV for vision processing",
            "faster-whisper": "Faster Whisper for STT",
        }
        
        for dep, description in required.items():
            # Check if dependency is listed (case-insensitive)
            pattern = re.compile(rf"^{re.escape(dep)}", re.IGNORECASE | re.MULTILINE)
            if pattern.search(requirements):
                print(f"  ✓ {dep}")
                self.stats["dependencies_found"] += 1
            else:
                print(f"  ✗ {dep} - MISSING ({description})")
                self.violations["dependencies"].append(f"Missing dependency: {dep}")
        
        self.stats["dependencies_required"] = len(required)
    
    def check_git_workflow(self):
        """Check git workflow compliance"""
        auto_commit_script = self.project_root / "scripts" / "auto_commit.py"
        if auto_commit_script.exists():
            print("  ✓ auto_commit.py script exists")
            self.stats["git_workflow_ok"] = 1
        else:
            print("  ✗ auto_commit.py script missing")
            self.violations["git_workflow"].append("Missing scripts/auto_commit.py")
        
        # Check .gitignore
        gitignore = self.project_root / ".gitignore"
        if gitignore.exists():
            gitignore_content = gitignore.read_text()
            required_ignores = [".env", "venv/", "__pycache__/", "*.log", "data/db/"]
            
            for ignore_pattern in required_ignores:
                if ignore_pattern in gitignore_content:
                    print(f"  ✓ .gitignore contains '{ignore_pattern}'")
                else:
                    print(f"  ✗ .gitignore missing '{ignore_pattern}'")
                    self.violations["git_workflow"].append(
                        f".gitignore should ignore '{ignore_pattern}'"
                    )
    
    def print_summary(self):
        """Print compliance summary"""
        total_violations = sum(len(v) for v in self.violations.values())
        
        print(f"\n📊 Statistics:")
        print(f"  • Python files checked: {self.stats['python_files_checked']}")
        print(f"  • Functions found: {self.stats['functions_found']}")
        print(f"  • Async functions: {self.stats['async_functions_found']}")
        print(f"  • Classes found: {self.stats['classes_found']}")
        print(f"  • Directories: {self.stats['directories_found']}/{self.stats['directories_required']}")
        print(f"  • Dependencies: {self.stats['dependencies_found']}/{self.stats['dependencies_required']}")
        
        print(f"\n⚠️  Violations Found: {total_violations}")
        
        if total_violations == 0:
            print("\n✅ ALL CHECKS PASSED - Codebase is compliant!")
        else:
            print("\n❌ Compliance Issues Found:\n")
            
            for category, issues in self.violations.items():
                if issues:
                    print(f"  {category.upper()} ({len(issues)} issues):")
                    for issue in issues[:5]:  # Show first 5
                        print(f"    • {issue}")
                    if len(issues) > 5:
                        print(f"    ... and {len(issues) - 5} more")
                    print()


def main():
    """Main entry point"""
    project_root = Path(__file__).parent.parent
    
    checker = RuleChecker(project_root)
    results = checker.check_all()
    
    # Exit with error code if violations found
    exit(0 if results["pass"] else 1)


if __name__ == "__main__":
    main()

