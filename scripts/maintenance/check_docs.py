"""
Documentation Helper - Check and Update Existing Files
Helps prevent creating duplicate markdown files
"""

from pathlib import Path
from typing import List, Optional, Tuple
import re


class DocumentationManager:
    """Manages documentation files and prevents duplicates"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_root = project_root / "docs"
        
        # Mapping of content types to existing files
        self.file_mapping = {
            "progress": "docs/progress/PROJECT_PROGRESS.md",
            "checkpoint": "docs/progress/CHECKPOINT.md",
            "architecture": "docs/architecture/ARCHITECTURE.md",
            "code": "docs/architecture/CODE_DOCUMENTATION.md",
            "structure": "docs/README.md",
            "setup": "docs/setup/",  # Directory, check for specific file
            "git": "docs/git/",  # Directory, check for specific file
            "hardware": "docs/hardware/",  # Directory
            "development": "docs/development/",  # Directory
        }
    
    def find_existing_file(self, content_type: str, topic: Optional[str] = None) -> Optional[Path]:
        """
        Find existing file for given content type
        
        Args:
            content_type: Type of content (progress, architecture, setup, etc.)
            topic: Optional topic/keyword to search for
            
        Returns:
            Path to existing file if found, None otherwise
        """
        if content_type in self.file_mapping:
            target = self.file_mapping[content_type]
            
            if target.endswith("/"):
                # Directory - search for specific file
                if topic:
                    # Try to find file matching topic
                    dir_path = self.project_root / target
                    if dir_path.exists():
                        # Look for files containing topic in name
                        for file in dir_path.glob("*.md"):
                            if topic.lower() in file.stem.lower():
                                return file
                        # Return first file if topic not found
                        files = list(dir_path.glob("*.md"))
                        if files:
                            return files[0]
                else:
                    # Return directory path
                    return self.project_root / target
            else:
                # Specific file
                file_path = self.project_root / target
                if file_path.exists():
                    return file_path
        
        return None
    
    def should_create_new_file(self, proposed_filename: str, content_type: str) -> Tuple[bool, Optional[str]]:
        """
        Determine if a new file should be created
        
        Args:
            proposed_filename: Name of proposed file
            content_type: Type of content
            
        Returns:
            (should_create, reason_message)
        """
        # Check if file already exists
        proposed_path = self.project_root / proposed_filename
        if proposed_path.exists():
            return False, f"File already exists: {proposed_filename}"
        
        # Check if similar content exists in existing files
        existing_file = self.find_existing_file(content_type)
        if existing_file:
            return False, f"Similar content exists in: {existing_file.relative_to(self.project_root)}. Append to that file instead."
        
        # Check for common duplicate patterns
        if proposed_filename.startswith("docs/"):
            # Check if it's in guides folder (always OK)
            if proposed_filename.startswith("docs/guides/"):
                return True, "New guide file - OK to create"
            
            # Check if similar file exists in same directory
            dir_path = Path(proposed_filename).parent
            if dir_path.exists():
                existing_files = list(dir_path.glob("*.md"))
                for existing in existing_files:
                    # Check if names are similar
                    if self._similar_filename(existing.stem, Path(proposed_filename).stem):
                        return False, f"Similar file exists: {existing.name}. Consider updating that file instead."
        
        # Default: allow creation but warn
        return True, "New file - but verify if similar content exists elsewhere"
    
    def _similar_filename(self, name1: str, name2: str) -> bool:
        """Check if two filenames are similar"""
        name1_lower = name1.lower().replace("_", "").replace("-", "")
        name2_lower = name2.lower().replace("_", "").replace("-", "")
        
        # Check for exact match
        if name1_lower == name2_lower:
            return True
        
        # Check if one contains the other
        if name1_lower in name2_lower or name2_lower in name1_lower:
            return True
        
        # Check for common words
        common_words = ["structure", "documentation", "guide", "setup", "progress", "architecture"]
        for word in common_words:
            if word in name1_lower and word in name2_lower:
                return True
        
        return False
    
    def get_append_location(self, content_type: str, topic: Optional[str] = None) -> Optional[Path]:
        """
        Get the file where content should be appended
        
        Args:
            content_type: Type of content
            topic: Optional topic
            
        Returns:
            Path to file where content should be appended
        """
        return self.find_existing_file(content_type, topic)


def check_before_create(filename: str, content_type: str = "general") -> Tuple[bool, str]:
    """
    Check if file should be created or if existing file should be updated
    
    Args:
        filename: Proposed filename
        content_type: Type of content (progress, architecture, setup, etc.)
        
    Returns:
        (should_create, message)
    """
    project_root = Path(__file__).parent.parent
    manager = DocumentationManager(project_root)
    
    return manager.should_create_new_file(filename, content_type)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python check_docs.py <proposed_filename> [content_type]")
        sys.exit(1)
    
    filename = sys.argv[1]
    content_type = sys.argv[2] if len(sys.argv) > 2 else "general"
    
    should_create, message = check_before_create(filename, content_type)
    
    if should_create:
        print(f"✅ OK to create: {filename}")
        print(f"   Note: {message}")
    else:
        print(f"❌ DO NOT CREATE: {filename}")
        print(f"   Reason: {message}")
        sys.exit(1)

