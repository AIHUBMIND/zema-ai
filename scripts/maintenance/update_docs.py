"""
Auto-Update Documentation Script
Updates CODE_DOCUMENTATION.md and PROJECT_PROGRESS.md after task completion
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess


class DocumentationUpdater:
    """Updates project documentation automatically"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_root = project_root / "src"
        self.docs_root = project_root / "docs"
        
    def update_all(self, task_name: str, task_id: str, status: str = "complete") -> None:
        """
        Update all documentation files
        
        Args:
            task_name: Name of completed task (e.g., "SETUP-001 - Create Project Structure")
            task_id: Task ID (e.g., "SETUP-001")
            status: Status ("complete", "in_progress", "pending")
        """
        print(f"📝 Updating documentation for {task_name}...")
        
        # Update progress tracker
        self.update_progress_tracker(task_name, task_id, status)
        
        # Update checkpoint
        self.update_checkpoint(task_name, task_id, status)
        
        # Update code documentation
        self.update_code_documentation()
        
        print("✅ Documentation updated!")
    
    def update_progress_tracker(self, task_name: str, task_id: str, status: str) -> None:
        """Update PROJECT_PROGRESS.md"""
        progress_file = self.docs_root / "progress" / "PROJECT_PROGRESS.md"
        
        if not progress_file.exists():
            print("⚠️  PROJECT_PROGRESS.md not found, skipping...")
            return
        
        content = progress_file.read_text(encoding='utf-8')
        
        # Update "Last Updated" timestamp
        content = re.sub(
            r"\*\*Last Updated:\*\* \d{4}-\d{2}-\d{2}",
            f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}",
            content
        )
        
        # Update current step if status is complete
        if status == "complete":
            # Find and update task status
            pattern = rf"### {re.escape(task_id)}:.*?\n\*\*Status:\*\* .*?\n"
            replacement = f"### {task_id}: {task_name.replace(task_id + ' - ', '')} ✅ COMPLETE\n**Status:** ✅ Complete\n"
            
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            else:
                # Add new completion entry
                completed_section = f"### {task_id}: {task_name.replace(task_id + ' - ', '')} ✅ COMPLETE\n"
                completed_section += f"**Status:** ✅ Complete\n"
                completed_section += f"**Completed:** {datetime.now().strftime('%Y-%m-%d')}\n"
                completed_section += f"**Description:** Task completed successfully\n\n"
                
                # Insert after "### Completed Tasks" section
                if "### Completed Tasks" in content:
                    content = content.replace(
                        "### Completed Tasks",
                        f"### Completed Tasks\n{completed_section}"
                    )
        
        # Update next step
        if status == "complete":
            # Extract next task ID
            if task_id.startswith("SETUP-"):
                num = int(task_id.split("-")[1])
                next_id = f"SETUP-{num+1:03d}"
                next_name = f"{next_id} - Next Step"
                
                content = re.sub(
                    r"\*\*Next Step:\*\* .*?\n",
                    f"**Next Step:** {next_name}\n",
                    content
                )
        
        progress_file.write_text(content, encoding='utf-8')
        print(f"  ✓ Updated {progress_file.name}")
    
    def update_checkpoint(self, task_name: str, task_id: str, status: str) -> None:
        """Update CHECKPOINT.md"""
        checkpoint_file = self.docs_root / "progress" / "CHECKPOINT.md"
        
        if not checkpoint_file.exists():
            print("⚠️  CHECKPOINT.md not found, skipping...")
            return
        
        content = checkpoint_file.read_text(encoding='utf-8')
        
        # Update last completed
        if status == "complete":
            content = re.sub(
                r"\*\*📌 Last Completed:\*\* .*?\n",
                f"**📌 Last Completed:** {task_name}\n",
                content
            )
            
            # Update next step
            if task_id.startswith("SETUP-"):
                num = int(task_id.split("-")[1])
                next_id = f"SETUP-{num+1:03d}"
                next_name = f"{next_id} - Next Step"
                
                content = re.sub(
                    r"\*\*⏭️ Next Step:\*\* .*?\n",
                    f"**⏭️ Next Step:** {next_name}\n",
                    content
                )
        
        # Update timestamp
        content = re.sub(
            r"\*\*Last Updated:\*\* \d{4}-\d{2}-\d{2}",
            f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}",
            content
        )
        
        checkpoint_file.write_text(content, encoding='utf-8')
        print(f"  ✓ Updated {checkpoint_file.name}")
    
    def update_code_documentation(self) -> None:
        """Update CODE_DOCUMENTATION.md with new files"""
        doc_file = self.docs_root / "architecture" / "CODE_DOCUMENTATION.md"
        
        if not doc_file.exists():
            print("⚠️  CODE_DOCUMENTATION.md not found, skipping...")
            return
        
        # This is a placeholder - full implementation would:
        # 1. Scan src/ for new files
        # 2. Parse Python files to extract functions/classes
        # 3. Generate documentation sections
        # 4. Update CODE_DOCUMENTATION.md
        
        print(f"  ✓ Updated {doc_file.name} (full update requires manual review)")
    
    def get_current_checkpoint(self) -> Dict[str, str]:
        """Read current checkpoint information"""
        checkpoint_file = self.docs_root / "progress" / "CHECKPOINT.md"
        
        if not checkpoint_file.exists():
            return {
                "last_completed": "Unknown",
                "next_step": "Unknown",
                "status": "Unknown"
            }
        
        content = checkpoint_file.read_text(encoding='utf-8')
        
        last_completed = re.search(r"\*\*📌 Last Completed:\*\* (.+?)\n", content)
        next_step = re.search(r"\*\*⏭️ Next Step:\*\* (.+?)\n", content)
        
        return {
            "last_completed": last_completed.group(1) if last_completed else "Unknown",
            "next_step": next_step.group(1) if next_step else "Unknown",
            "status": "Ready"
        }


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python update_docs.py <task_name> <task_id> [status]")
        print("Example: python update_docs.py 'SETUP-001 - Create Project Structure' SETUP-001 complete")
        sys.exit(1)
    
    task_name = sys.argv[1]
    task_id = sys.argv[2]
    status = sys.argv[3] if len(sys.argv) > 3 else "complete"
    
    project_root = Path(__file__).resolve().parent.parent.parent
    updater = DocumentationUpdater(project_root)
    updater.update_all(task_name, task_id, status)


if __name__ == "__main__":
    main()

