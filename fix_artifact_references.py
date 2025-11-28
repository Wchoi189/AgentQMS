#!/usr/bin/env python3
"""
Fix internal references to old artifact paths and filenames.
"""

import re
from pathlib import Path

# Mapping of old paths/names to new paths/names
REFERENCE_FIXES = [
    # Old path patterns
    (r"docs_deprecated/artifacts/", "docs/artifacts/"),
    (r"docs/artifacts/rfcs/", "docs/artifacts/design_documents/"),
    
    # Old filename patterns
    (r"2025-11-20_assessment_framework_structure\.md", "2025-11-20_0000_assessment-framework-structure.md"),
    (r"2025-11-20_IMPLEMENTATION_PLAN_framework_structure_refactor\.md", "2025-11-20_0000_implementation_plan_framework-structure-refactor.md"),
    (r"2025-11-20_RFT_directory_naming_refactor\.md", "2025-11-20_0000_design-directory-naming-refactor.md"),
    (r"2025-11-20_RFT_configuration_hierarchy\.md", "2025-11-20_0000_design-configuration-hierarchy.md"),
    (r"2025-11-20_design_config_hierarchy\.md", "2025-11-20_0000_design-config-hierarchy.md"),
    (r"2025-11-25_assessment_plugin_architecture_design\.md", "2025-11-25_1830_assessment-plugin-architecture-design.md"),
    (r"2025-11-24-IMPLEMENTATION_PLAN_post_audit_fixes\.md", "2025-11-24_0000_implementation_plan_post-audit-fixes.md"),
]


def fix_file_references(file_path: Path) -> bool:
    """Fix references in a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes
        for old_pattern, new_pattern in REFERENCE_FIXES:
            content = re.sub(old_pattern, new_pattern, content)
        
        # Only write if changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix internal references to old artifact paths")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed")
    parser.add_argument("--file", help="Fix a specific file")
    
    args = parser.parse_args()
    
    files_to_fix = []
    
    if args.file:
        files_to_fix = [Path(args.file)]
    else:
        # Find all markdown files in docs/artifacts
        artifacts_dir = Path("docs/artifacts")
        if artifacts_dir.exists():
            files_to_fix = list(artifacts_dir.rglob("*.md"))
        
        # Also fix CHANGELOG.md
        changelog = Path("CHANGELOG.md")
        if changelog.exists():
            files_to_fix.append(changelog)
    
    fixed_count = 0
    for file_path in files_to_fix:
        if args.dry_run:
            # Just check if it would be changed
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                original_content = content
                for old_pattern, new_pattern in REFERENCE_FIXES:
                    content = re.sub(old_pattern, new_pattern, content)
                if content != original_content:
                    print(f"Would fix: {file_path}")
                    fixed_count += 1
            except Exception as e:
                print(f"Error checking {file_path}: {e}")
        else:
            if fix_file_references(file_path):
                print(f"Fixed: {file_path}")
                fixed_count += 1
    
    if args.dry_run:
        print(f"\nWould fix {fixed_count} files")
        print("Use without --dry-run to apply fixes")
    else:
        print(f"\nFixed {fixed_count} files")
    
    return 0


if __name__ == "__main__":
    exit(main())

