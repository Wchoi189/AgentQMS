#!/usr/bin/env python3
"""
Legacy Artifact Date Fixer

This script identifies and fixes artifacts with incorrect dates in filenames and frontmatter.
It updates dates to match the actual file creation timestamps.

Usage:
    python fix_legacy_artifact_dates.py --dry-run  # Preview changes
    python fix_legacy_artifact_dates.py --fix     # Apply fixes
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


class LegacyArtifactDateFixer:
    """Fix incorrect dates in legacy artifacts."""

    def __init__(self, artifacts_root: str = "docs/artifacts"):
        self.artifacts_root = Path(artifacts_root)
        self.fixed_files: list[str] = []
        self.errors: list[str] = []

    def find_legacy_artifacts(self) -> list:
        """Find artifacts with incorrect dates."""
        legacy_files = []

        for md_file in self.artifacts_root.rglob("*.md"):
            if self._has_incorrect_date(md_file):
                legacy_files.append(md_file)

        return legacy_files

    def _has_incorrect_date(self, file_path: Path) -> bool:
        """Check if file has incorrect date in filename or frontmatter."""
        filename = file_path.name

        # Check filename for 2025-01-27 pattern
        if "2025-01-27" in filename:
            return True

        # Check frontmatter for incorrect date
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Extract frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]
                    if "2025-01-27" in frontmatter_text:
                        return True
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

        return False

    def get_file_creation_date(self, file_path: Path) -> datetime:
        """Get the actual file creation date."""
        stat = file_path.stat()
        return datetime.fromtimestamp(stat.st_ctime)

    def fix_artifact_date(self, file_path: Path, dry_run: bool = True) -> bool:
        """Fix the date in a single artifact."""
        try:
            creation_date = self.get_file_creation_date(file_path)
            date_str = creation_date.strftime("%Y-%m-%d")
            time_str = creation_date.strftime("%H%M")
            iso_date = creation_date.isoformat() + "Z"

            print(f"\n🔧 Fixing: {file_path.name}")
            print(f"   Creation date: {creation_date}")
            print(f"   New date string: {date_str}_{time_str}")
            print(f"   New ISO date: {iso_date}")

            if dry_run:
                print("   [DRY RUN] Would fix this file")
                return True

            # Read current content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Fix frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]

                    # Replace incorrect date in frontmatter
                    frontmatter_text = re.sub(
                        r'date:\s*"2025-01-27T\d{2}:\d{2}:\d{2}Z"',
                        f'date: "{iso_date}"',
                        frontmatter_text,
                    )

                    content = f"---{frontmatter_text}---{parts[2]}"

            # Write updated content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            # Rename file if needed
            if "2025-01-27" in file_path.name:
                new_name = file_path.name.replace("2025-01-27", f"{date_str}")
                new_path = file_path.parent / new_name

                if new_path.exists():
                    print(f"   ⚠️  Warning: Target file {new_path.name} already exists")
                    return False

                file_path.rename(new_path)
                print(f"   ✅ Renamed to: {new_path.name}")
                self.fixed_files.append(str(new_path))
            else:
                self.fixed_files.append(str(file_path))

            print("   ✅ Fixed successfully")
            return True

        except Exception as e:
            error_msg = f"Error fixing {file_path}: {e}"
            print(f"   ❌ {error_msg}")
            self.errors.append(error_msg)
            return False

    def fix_all_legacy_artifacts(self, dry_run: bool = True) -> dict:
        """Fix all legacy artifacts."""
        legacy_files = self.find_legacy_artifacts()

        print(f"Found {len(legacy_files)} legacy artifacts with incorrect dates:")
        for file_path in legacy_files:
            print(f"  - {file_path}")

        if not legacy_files:
            print("✅ No legacy artifacts found!")
            return {"fixed": 0, "errors": 0, "files": []}

        fixed_count = 0
        error_count = 0

        for file_path in legacy_files:
            if self.fix_artifact_date(file_path, dry_run):
                fixed_count += 1
            else:
                error_count += 1

        return {
            "fixed": fixed_count,
            "errors": error_count,
            "files": self.fixed_files,
            "error_messages": self.errors,
        }


def main():
    parser = argparse.ArgumentParser(description="Fix legacy artifact dates")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without applying them"
    )
    parser.add_argument("--fix", action="store_true", help="Apply the fixes")
    parser.add_argument(
        "--artifacts-root",
        default="docs/artifacts",
        help="Root directory for artifacts",
    )

    args = parser.parse_args()

    if not args.dry_run and not args.fix:
        print("❌ Please specify either --dry-run or --fix")
        return 1

    fixer = LegacyArtifactDateFixer(args.artifacts_root)

    print("🔍 Legacy Artifact Date Fixer")
    print("=" * 50)

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    else:
        print("🔧 FIX MODE - Changes will be applied")

    results = fixer.fix_all_legacy_artifacts(dry_run=args.dry_run)

    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print(f"✅ Fixed: {results['fixed']} files")
    print(f"❌ Errors: {results['errors']} files")

    if results["errors"] > 0:
        print("\n❌ ERRORS:")
        for error in results["error_messages"]:
            print(f"  - {error}")

    if results["fixed"] > 0 and not args.dry_run:
        print(f"\n✅ Successfully fixed {len(results['files'])} files:")
        for file_path in results["files"]:
            print(f"  - {file_path}")

    return 0 if results["errors"] == 0 else 1


if __name__ == "__main__":
    exit(main())
