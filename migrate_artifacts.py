#!/usr/bin/env python3
"""
Migration script to standardize artifact naming and directory structure.

This script:
1. Renames artifacts to timestamped format: YYYY-MM-DD_HHMM_[PREFIX]descriptive-name.md
2. Ensures artifacts are in correct type-based directories
3. Updates any references if needed
"""

import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import shutil

# Mapping of artifact types to prefixes and directories
ARTIFACT_CONFIG = {
    "implementation_plan": {
        "prefix": "implementation_plan_",
        "directory": "implementation_plans",
    },
    "assessment": {
        "prefix": "assessment-",
        "directory": "assessments",
    },
    "design": {
        "prefix": "design-",
        "directory": "design_documents",
    },
    "research": {
        "prefix": "research-",
        "directory": "research",
    },
    "template": {
        "prefix": "template-",
        "directory": "templates",
    },
    "bug_report": {
        "prefix": "BUG_",
        "directory": "bug_reports",
    },
    "session_note": {
        "prefix": "SESSION_",
        "directory": "completed_plans/completion_summaries/session_notes",
    },
}

# Directory to type mapping (for files already in correct directories)
DIRECTORY_TO_TYPE = {
    "implementation_plans": "implementation_plan",
    "assessments": "assessment",
    "design_documents": "design",
    "research": "research",
    "templates": "template",
    "bug_reports": "bug_report",
    "rfcs": "design",  # RFCs are design documents
}


def extract_frontmatter(file_path: Path) -> Optional[dict]:
    """Extract frontmatter from a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for frontmatter
        if not content.startswith("---"):
            return None
        
        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        
        frontmatter_text = parts[1].strip()
        if not frontmatter_text:
            return None
        
        try:
            return yaml.safe_load(frontmatter_text)
        except yaml.YAMLError:
            return None
    except Exception:
        return None


def get_artifact_type(file_path: Path, frontmatter: Optional[dict] = None) -> Optional[str]:
    """Determine artifact type from frontmatter or directory."""
    # Try frontmatter first
    if frontmatter and "type" in frontmatter:
        artifact_type = frontmatter["type"]
        if artifact_type in ARTIFACT_CONFIG:
            return artifact_type
    
    # Check if in templates subdirectory - these should stay as templates
    if "templates" in str(file_path.parent) or "agent_workflows" in str(file_path.parent):
        return "template"
    
    # Try directory
    parent_dir = file_path.parent.name
    if parent_dir in DIRECTORY_TO_TYPE:
        return DIRECTORY_TO_TYPE[parent_dir]
    
    # Try to infer from filename
    filename = file_path.name.lower()
    if "template" in filename:
        return "template"
    elif "implementation" in filename or "plan" in filename:
        return "implementation_plan"
    elif "assessment" in filename:
        return "assessment"
    elif "design" in filename or "rfc" in filename or "rft" in filename:
        return "design"
    elif "bug" in filename:
        return "bug_report"
    elif "research" in filename:
        return "research"
    elif "summary" in filename or "archive" in str(file_path.parent):
        # Archive files - try to infer from content or default to assessment
        return "assessment"  # Default for archive/summary files
    
    return None


def extract_timestamp(file_path: Path, frontmatter: Optional[dict] = None) -> str:
    """Extract or generate timestamp for filename."""
    # Try to get from frontmatter date
    if frontmatter and "date" in frontmatter:
        date_str = frontmatter["date"]
        # Parse various date formats
        # Format: "2025-11-09 00:00 (KST)" or "2025-11-09" or "2025-11-09 12:34"
        try:
            # Try parsing with time
            if " " in date_str:
                date_part = date_str.split()[0]
                time_part = date_str.split()[1] if len(date_str.split()) > 1 else "00:00"
                # Remove timezone info if present
                time_part = time_part.split("(")[0].strip()
                if ":" in time_part:
                    hour, minute = time_part.split(":")[:2]
                    return f"{date_part}_{hour.zfill(2)}{minute.zfill(2)}"
                else:
                    return f"{date_part}_0000"
            else:
                return f"{date_str}_0000"
        except Exception:
            pass
    
    # Try to extract from filename
    filename = file_path.name
    # Pattern: YYYY-MM-DD or YYYY-MM-DD_HHMM
    match = re.match(r"(\d{4}-\d{2}-\d{2})(?:_(\d{4}))?", filename)
    if match:
        date_part = match.group(1)
        time_part = match.group(2) if match.group(2) else "0000"
        return f"{date_part}_{time_part}"
    
    # Use file modification time as fallback
    try:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mtime.strftime("%Y-%m-%d_%H%M")
    except Exception:
        # Final fallback: use current time
        return datetime.now().strftime("%Y-%m-%d_%H%M")


def extract_descriptive_name(file_path: Path, artifact_type: str) -> str:
    """Extract descriptive name from filename."""
    filename = file_path.stem  # Without extension
    
    # Remove timestamp if present
    filename = re.sub(r"^\d{4}-\d{2}-\d{2}(?:_\d{4})?", "", filename)
    filename = filename.strip("_-")
    
    # Remove type prefix if present (check all variants)
    if artifact_type in ARTIFACT_CONFIG:
        prefix = ARTIFACT_CONFIG[artifact_type]["prefix"]
        
        # Handle special cases first
        if artifact_type == "implementation_plan":
            if filename.startswith("IMPLEMENTATION_PLAN_"):
                filename = filename[len("IMPLEMENTATION_PLAN_"):]
            elif filename.startswith("IMPLEMENTATION-PLAN-"):
                filename = filename[len("IMPLEMENTATION-PLAN-"):]
            elif filename.startswith("implementation_plan_"):
                filename = filename[len("implementation_plan_"):]
        elif artifact_type == "assessment":
            # Remove all variants of assessment prefix
            prefixes_to_remove = ["ASSESSMENT_", "assessment_", "assessment-", "ASSESSMENT-"]
            for prefix in prefixes_to_remove:
                if filename.startswith(prefix):
                    filename = filename[len(prefix):]
                    break
        elif artifact_type == "design":
            # Remove all variants of design/RFC/RFT prefix
            prefixes_to_remove = ["RFT_", "RFC_", "design_", "design-", "RFT-", "RFC-"]
            for prefix in prefixes_to_remove:
                if filename.startswith(prefix):
                    filename = filename[len(prefix):]
                    break
        elif artifact_type == "template":
            # For templates, preserve "template-" prefix in subdirectories
            if "agent_workflows" in str(file_path.parent):
                # These are template files, keep the template- prefix
                if filename.startswith("template-"):
                    # Already has prefix, don't remove it
                    pass
            elif filename.startswith("template_"):
                filename = filename[len("template_"):]
            elif filename.startswith("template-"):
                filename = filename[len("template-"):]
        
        # Remove standard prefix if still present
        if filename.startswith(prefix):
            filename = filename[len(prefix):]
        # Also handle uppercase variants
        prefix_upper = prefix.upper()
        if filename.startswith(prefix_upper):
            filename = filename[len(prefix_upper):]
    
    # Normalize to kebab-case
    filename = filename.replace("_", "-").replace(" ", "-")
    filename = re.sub(r"-+", "-", filename)  # Replace multiple dashes
    filename = filename.strip("-").lower()
    
    # If empty, use a default based on type
    if not filename:
        filename = f"{artifact_type.replace('_', '-')}-document"
    
    return filename


def generate_new_filename(artifact_type: str, timestamp: str, descriptive_name: str) -> str:
    """Generate new filename in correct format."""
    if artifact_type not in ARTIFACT_CONFIG:
        # Fallback format
        return f"{timestamp}_{artifact_type.replace('_', '-')}_{descriptive_name}.md"
    
    config = ARTIFACT_CONFIG[artifact_type]
    prefix = config["prefix"]
    
    # Special handling for bug reports
    if artifact_type == "bug_report":
        # Bug reports format: BUG_YYYY-MM-DD_HHMM_NNN_descriptive-name.md
        # Extract bug ID from descriptive name if present
        if "_" in descriptive_name:
            parts = descriptive_name.split("_", 1)
            bug_id = parts[0] if parts[0].isdigit() else "001"
            descriptive_name = parts[1] if len(parts) > 1 else descriptive_name
        else:
            bug_id = "001"
        return f"BUG_{timestamp}_{bug_id}_{descriptive_name}.md"
    
    # Standard format: YYYY-MM-DD_HHMM_[PREFIX]descriptive-name.md
    return f"{timestamp}_{prefix}{descriptive_name}.md"


def migrate_artifact(file_path: Path, target_root: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """Migrate a single artifact file."""
    try:
        # Extract frontmatter
        frontmatter = extract_frontmatter(file_path)
        
        # Determine artifact type
        artifact_type = get_artifact_type(file_path, frontmatter)
        if not artifact_type:
            return False, f"Could not determine artifact type for {file_path}"
        
        # Get configuration
        if artifact_type not in ARTIFACT_CONFIG:
            return False, f"Unknown artifact type: {artifact_type}"
        
        config = ARTIFACT_CONFIG[artifact_type]
        
        # Extract timestamp
        timestamp = extract_timestamp(file_path, frontmatter)
        
        # Extract descriptive name
        descriptive_name = extract_descriptive_name(file_path, artifact_type)
        
        # Generate new filename
        new_filename = generate_new_filename(artifact_type, timestamp, descriptive_name)
        
        # Determine target directory
        target_dir = target_root / config["directory"]
        target_path = target_dir / new_filename
        
        # Check if target already exists
        if target_path.exists() and target_path != file_path:
            return False, f"Target file already exists: {target_path}"
        
        if dry_run:
            return True, f"Would migrate: {file_path} -> {target_path}"
        
        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Move and rename file
        if file_path != target_path:
            shutil.move(str(file_path), str(target_path))
            return True, f"Migrated: {file_path} -> {target_path}"
        else:
            # File is already in correct location, just ensure name is correct
            if file_path.name != new_filename:
                file_path.rename(target_path)
                return True, f"Renamed: {file_path.name} -> {new_filename}"
            else:
                return True, f"Already correct: {file_path}"
    
    except Exception as e:
        return False, f"Error migrating {file_path}: {e}"


def main():
    """Main migration function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate artifacts to standardized naming and structure")
    parser.add_argument("--source", default="docs_deprecated/artifacts", help="Source artifacts directory")
    parser.add_argument("--target", default="docs/artifacts", help="Target artifacts directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    source_root = Path(args.source)
    target_root = Path(args.target)
    
    if not source_root.exists():
        print(f"Error: Source directory does not exist: {source_root}")
        return 1
    
    # Find all markdown files
    artifact_files = list(source_root.rglob("*.md"))
    
    # Filter out index files and special files
    artifact_files = [
        f for f in artifact_files
        if f.name.lower() not in ["index.md", "readme.md"]
        and not f.name.startswith(".")  # Skip hidden files
    ]
    
    print(f"Found {len(artifact_files)} artifact files to migrate")
    print(f"Source: {source_root}")
    print(f"Target: {target_root}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'MIGRATION'}")
    print()
    
    success_count = 0
    error_count = 0
    
    for file_path in sorted(artifact_files):
        success, message = migrate_artifact(file_path, target_root, dry_run=args.dry_run)
        if success:
            success_count += 1
            if args.verbose or args.dry_run:
                print(f"✓ {message}")
        else:
            error_count += 1
            print(f"✗ {message}")
    
    print()
    print(f"Summary: {success_count} succeeded, {error_count} failed")
    
    if args.dry_run:
        print("\nThis was a dry run. Use without --dry-run to perform the migration.")
    
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())

