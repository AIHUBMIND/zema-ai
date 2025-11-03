"""
Reorganize Project Structure
Organizes all files and documentation into proper subdirectories
"""

import shutil
from pathlib import Path
from typing import Dict, List, Tuple


class ProjectOrganizer:
    """Organizes project files and documentation"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_root = project_root / "docs"
        self.scripts_root = project_root / "scripts"
        
    def organize_all(self) -> None:
        """Organize all project files"""
        print("=" * 70)
        print("ORGANIZING PROJECT STRUCTURE")
        print("=" * 70)
        print()
        
        # Organize documentation
        self.organize_documentation()
        
        # Organize scripts
        self.organize_scripts()
        
        # Clean up root
        self.cleanup_root()
        
        print("\n" + "=" * 70)
        print("✅ PROJECT ORGANIZATION COMPLETE")
        print("=" * 70)
    
    def organize_documentation(self) -> None:
        """Organize documentation files"""
        print("📚 Organizing Documentation...")
        
        # Create new structure
        structure = {
            "progress": {
                "description": "Progress tracking and checkpoints",
                "files": [
                    ("PROJECT_PROGRESS.md", "docs/PROJECT_PROGRESS.md"),
                    ("CHECKPOINT.md", "CHECKPOINT.md"),
                ]
            },
            "architecture": {
                "description": "System architecture and code documentation",
                "files": [
                    ("ARCHITECTURE.md", "docs/ARCHITECTURE.md"),
                    ("CODE_DOCUMENTATION.md", "docs/CODE_DOCUMENTATION.md"),
                    ("PROMPT_ANALYSIS_REPORT.md", "docs/PROMPT_ANALYSIS_REPORT.md"),
                ]
            },
            "setup": {
                "description": "Setup and installation guides",
                "files": [
                    ("SETUP.md", "docs/SETUP.md"),
                    ("ACTIVATION.md", "docs/ACTIVATION.md"),
                    ("WHY_ACTIVATION.md", "docs/WHY_ACTIVATION.md"),
                    ("ADDING_PIP_TO_PATH.md", "docs/ADDING_PIP_TO_PATH.md"),
                    ("PIP_FIXED.md", "docs/PIP_FIXED.md"),
                    ("WSL_INFO.md", "docs/WSL_INFO.md"),
                    ("QUICK_START.md", "QUICK_START.md"),
                ]
            },
            "git": {
                "description": "Git and GitHub related documentation",
                "files": [
                    ("GITHUB_SETUP.md", "docs/GITHUB_SETUP.md"),
                    ("AUTO_COMMIT.md", "docs/AUTO_COMMIT.md"),
                ]
            },
            "hardware": {
                "description": "Hardware configuration and setup",
                "files": [
                    ("BOSGAME_P3_LITE.md", "docs/BOSGAME_P3_LITE.md"),
                ]
            },
            "development": {
                "description": "Development progress and enhancements",
                "files": [
                    ("ENHANCEMENT_PROGRESS.md", "docs/ENHANCEMENT_PROGRESS.md"),
                ]
            },
        }
        
        moved = []
        not_found = []
        
        for folder_name, folder_info in structure.items():
            folder_path = self.docs_root / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"\n  📁 {folder_name}/ ({folder_info['description']})")
            
            for target_name, source_path in folder_info["files"]:
                source = self.project_root / source_path
                target = folder_path / target_name
                
                if source.exists():
                    if source != target:  # Don't move if already in place
                        shutil.move(str(source), str(target))
                        moved.append((source_path, f"docs/{folder_name}/{target_name}"))
                        print(f"    ✓ {source_path} → docs/{folder_name}/{target_name}")
                    else:
                        print(f"    ⊙ Already in place: {source_path}")
                else:
                    not_found.append(source_path)
                    print(f"    ⚠ Not found: {source_path}")
        
        print(f"\n  📊 Moved {len(moved)} files")
        if not_found:
            print(f"  ⚠ {len(not_found)} files not found (may not exist yet)")
    
    def organize_scripts(self) -> None:
        """Organize scripts into categories"""
        print("\n🔧 Organizing Scripts...")
        
        # Create script categories
        script_categories = {
            "setup": {
                "description": "Setup and installation scripts",
                "files": [
                    "setup_github_remote.py",
                    "connect_github.py",
                    "test_setup.py",
                    "verify_setup.py",
                    "verify_step4.py",
                ]
            },
            "maintenance": {
                "description": "Maintenance and utility scripts",
                "files": [
                    "auto_commit.py",
                    "update_docs.py",
                    "check_rules_compliance.py",
                    "check_git_status.py",
                    "backup.sh",
                    "cleanup.sh",
                    "benchmark.py",
                ]
            },
            "development": {
                "description": "Development helper scripts",
                "files": [
                    "download_models.sh",
                ]
            },
            "legacy": {
                "description": "Legacy/organization scripts (can be removed)",
                "files": [
                    "organize_docs.py",
                    "organize_zema_files.py",
                    "reorganize_docs.py",
                    "reverse_reorganization.py",
                    "cleanup_guides.py",
                    "cleanup_guides_folder.py",
                    "move_zema_to_guides.py",
                    "activate_helper.py",
                    "add_pip_to_path.bat",
                    "add_pip_to_path.ps1",
                ]
            },
        }
        
        moved = []
        not_found = []
        
        for category, info in script_categories.items():
            category_path = self.scripts_root / category
            category_path.mkdir(parents=True, exist_ok=True)
            print(f"\n  📁 scripts/{category}/ ({info['description']})")
            
            for script_name in info["files"]:
                source = self.scripts_root / script_name
                target = category_path / script_name
                
                if source.exists():
                    if source != target:
                        shutil.move(str(source), str(target))
                        moved.append((script_name, f"scripts/{category}/{script_name}"))
                        print(f"    ✓ {script_name} → scripts/{category}/{script_name}")
                    else:
                        print(f"    ⊙ Already in place: {script_name}")
                else:
                    not_found.append(script_name)
                    print(f"    ⚠ Not found: {script_name}")
        
        print(f"\n  📊 Moved {len(moved)} scripts")
        if not_found:
            print(f"  ⚠ {len(not_found)} scripts not found")
    
    def cleanup_root(self) -> None:
        """Clean up root directory"""
        print("\n🧹 Cleaning Up Root Directory...")
        
        # Files that should stay in root
        keep_in_root = {
            "README.md",
            "requirements.txt",
            "pyproject.toml",
            ".gitignore",
            ".cursorrules",
            ".env.example",
            "setup.py",
            "setup.sh",
        }
        
        # Check for files that should be moved
        root_files = [f for f in self.project_root.iterdir() 
                     if f.is_file() and f.suffix in ['.md', '.txt', '.py', '.sh', '.toml', '.example']]
        
        moved = []
        for file_path in root_files:
            if file_path.name not in keep_in_root:
                # These should have been moved already, but check anyway
                if file_path.name == "CHECKPOINT.md":
                    # Should be in docs/progress/ now
                    continue
                elif file_path.name == "QUICK_START.md":
                    # Should be in docs/setup/ now
                    continue
        
        print("  ✓ Root directory cleaned")
    
    def update_references(self) -> None:
        """Update file references in key files"""
        print("\n🔄 Updating File References...")
        
        # Update CHECKPOINT.md references
        checkpoint = self.docs_root / "progress" / "CHECKPOINT.md"
        if checkpoint.exists():
            content = checkpoint.read_text(encoding='utf-8')
            content = content.replace(
                "Progress Tracker: `docs/PROJECT_PROGRESS.md`",
                "Progress Tracker: `docs/progress/PROJECT_PROGRESS.md`"
            )
            content = content.replace(
                "Code Docs: `docs/CODE_DOCUMENTATION.md`",
                "Code Docs: `docs/architecture/CODE_DOCUMENTATION.md`"
            )
            content = content.replace(
                "Checkpoint: `CHECKPOINT.md` (this file)",
                "Checkpoint: `docs/progress/CHECKPOINT.md` (this file)"
            )
            checkpoint.write_text(content, encoding='utf-8')
            print("  ✓ Updated CHECKPOINT.md references")
        
        # Update PROJECT_PROGRESS.md references
        progress = self.docs_root / "progress" / "PROJECT_PROGRESS.md"
        if progress.exists():
            content = progress.read_text(encoding='utf-8')
            content = content.replace(
                "`docs/CODE_DOCUMENTATION.md`",
                "`docs/architecture/CODE_DOCUMENTATION.md`"
            )
            content = content.replace(
                "`docs/ARCHITECTURE.md`",
                "`docs/architecture/ARCHITECTURE.md`"
            )
            content = content.replace(
                "`CHECKPOINT.md`",
                "`docs/progress/CHECKPOINT.md`"
            )
            progress.write_text(content, encoding='utf-8')
            print("  ✓ Updated PROJECT_PROGRESS.md references")
        
        # Update .cursorrules references
        cursorrules = self.project_root / ".cursorrules"
        if cursorrules.exists():
            content = cursorrules.read_text(encoding='utf-8')
            content = content.replace(
                "`CHECKPOINT.md`",
                "`docs/progress/CHECKPOINT.md`"
            )
            content = content.replace(
                "`docs/PROJECT_PROGRESS.md`",
                "`docs/progress/PROJECT_PROGRESS.md`"
            )
            content = content.replace(
                "`docs/CODE_DOCUMENTATION.md`",
                "`docs/architecture/CODE_DOCUMENTATION.md`"
            )
            content = content.replace(
                "`docs/ARCHITECTURE.md`",
                "`docs/architecture/ARCHITECTURE.md`"
            )
            cursorrules.write_text(content, encoding='utf-8')
            print("  ✓ Updated .cursorrules references")
        
        # Update scripts/update_docs.py paths
        update_docs = self.scripts_root / "maintenance" / "update_docs.py"
        if update_docs.exists():
            content = update_docs.read_text(encoding='utf-8')
            content = content.replace(
                'progress_file = self.docs_root / "PROJECT_PROGRESS.md"',
                'progress_file = self.docs_root / "progress" / "PROJECT_PROGRESS.md"'
            )
            content = content.replace(
                'checkpoint_file = self.project_root / "CHECKPOINT.md"',
                'checkpoint_file = self.docs_root / "progress" / "CHECKPOINT.md"'
            )
            content = content.replace(
                'doc_file = self.docs_root / "CODE_DOCUMENTATION.md"',
                'doc_file = self.docs_root / "architecture" / "CODE_DOCUMENTATION.md"'
            )
            update_docs.write_text(content, encoding='utf-8')
            print("  ✓ Updated scripts/update_docs.py paths")


def main():
    """Main entry point"""
    project_root = Path(__file__).parent.parent
    
    organizer = ProjectOrganizer(project_root)
    organizer.organize_all()
    organizer.update_references()
    
    print("\n📋 New Structure:")
    print("\ndocs/")
    print("├── progress/          # Progress tracking")
    print("├── architecture/      # Architecture docs")
    print("├── setup/             # Setup guides")
    print("├── git/               # Git/GitHub docs")
    print("├── hardware/          # Hardware config")
    print("├── development/       # Dev progress")
    print("└── guides/           # Main guides (unchanged)")
    print("\nscripts/")
    print("├── setup/             # Setup scripts")
    print("├── maintenance/       # Maintenance scripts")
    print("├── development/      # Dev scripts")
    print("└── legacy/            # Old scripts")


if __name__ == "__main__":
    main()

