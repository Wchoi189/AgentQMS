#!/usr/bin/env python3
"""
Migration Package Script for AgentQMS
Unboxes AgentQMS framework into an existing project.
"""

import shutil
from pathlib import Path
import argparse

def copy_framework(source_dir: Path, target_dir: Path):
    """Copy AgentQMS/ and .agentqms/ to target directory."""
    agentqms_src = source_dir / "AgentQMS"
    agentqms_target = target_dir / "AgentQMS"
    dotagentqms_src = source_dir / ".agentqms"
    dotagentqms_target = target_dir / ".agentqms"

    if agentqms_src.exists():
        shutil.copytree(agentqms_src, agentqms_target, dirs_exist_ok=True)
        print(f"Copied AgentQMS/ to {agentqms_target}")
    else:
        print("Warning: AgentQMS/ not found in source")

    if dotagentqms_src.exists():
        shutil.copytree(dotagentqms_src, dotagentqms_target, dirs_exist_ok=True)
        print(f"Copied .agentqms/ to {dotagentqms_target}")
    else:
        print("Warning: .agentqms/ not found in source")

def scan_and_adjust_paths(target_dir: Path):
    """Scan for relative paths in configs and adjust if easy."""
    config_dirs = [
        target_dir / "AgentQMS" / "interface" / "config",
        target_dir / "AgentQMS" / "conventions"
    ]
    adjusted = False
    for config_dir in config_dirs:
        if config_dir.exists():
            for file_path in config_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        content = file_path.read_text()
                        # Simple adjustment: if paths start with ../, and can be made absolute or relative to target
                        # For now, just notify if relative paths found
                        if "../" in content:
                            print(f"Relative path found in {file_path}. Manual review recommended.")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    if not adjusted:
        print("No easy path adjustments needed.")

def create_artifacts_dirs(target_dir: Path):
    """Create artifact subdirs."""
    artifacts_dir = target_dir / "docs" / "artifacts"
    if artifacts_dir.exists():
        print("Artifacts directory already exists in target root, skipping creation.")
        return

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    subdirs = ["assessments", "implementation_plans", "bug_reports", "audits", "design_documents"]
    for subdir in subdirs:
        (artifacts_dir / subdir).mkdir(exist_ok=True)
    print(f"Created artifact subdirs in {artifacts_dir}")

    # Alternative: create in AgentQMS/docs/artifacts/ and instruct to move
    agentqms_artifacts = target_dir / "AgentQMS" / "docs" / "artifacts"
    if not agentqms_artifacts.exists():
        agentqms_artifacts.mkdir(parents=True, exist_ok=True)
        for subdir in subdirs:
            (agentqms_artifacts / subdir).mkdir(exist_ok=True)
        print(f"Created artifact subdirs in {agentqms_artifacts}")
        print("Move AgentQMS/docs/artifacts/ to project root/docs/artifacts")

def main():
    parser = argparse.ArgumentParser(description="Migrate AgentQMS to existing project")
    parser.add_argument("--source", required=True, help="Source directory containing AgentQMS and .agentqms")
    parser.add_argument("--target", default=".", help="Target project root directory")
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    target_dir = Path(args.target).resolve()

    print("Starting AgentQMS migration...")
    copy_framework(source_dir, target_dir)
    scan_and_adjust_paths(target_dir)
    create_artifacts_dirs(target_dir)
    print("Migration complete.")

if __name__ == "__main__":
    main()