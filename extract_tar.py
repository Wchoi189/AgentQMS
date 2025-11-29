#!/usr/bin/env python3
"""Script to extract tar file and set up refactor branch."""
import os
import subprocess
import tarfile
from datetime import datetime

def run_cmd(cmd, cwd=None):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd,
            capture_output=True, text=True, check=False
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    workspace = "/workspaces/agent_qms"
    os.chdir(workspace)
    
    print("=" * 60)
    print("Pre-extraction Safety Checks")
    print("=" * 60)
    
    # Check tar file
    tar_path = "agentqms-export.tar.gz"
    if not os.path.exists(tar_path):
        print(f"ERROR: {tar_path} not found!")
        return 1
    tar_size = os.path.getsize(tar_path)
    print(f"✓ Tar file exists: {tar_path} ({tar_size:,} bytes)")
    
    # Check git status
    success, stdout, stderr = run_cmd("git status --porcelain", cwd=workspace)
    if success:
        if stdout:
            print(f"⚠ WARNING: Working directory has uncommitted changes:")
            print(stdout)
        else:
            print("✓ Working directory is clean")
    else:
        print(f"⚠ Could not check git status: {stderr}")
    
    # Get current branch
    success, branch, stderr = run_cmd("git branch --show-current", cwd=workspace)
    if success:
        print(f"✓ Current branch: {branch}")
        current_branch = branch
    else:
        print(f"⚠ Could not get current branch: {stderr}")
        current_branch = "unknown"
    
    # List tar contents
    print("\n" + "=" * 60)
    print("Tar File Contents Preview")
    print("=" * 60)
    try:
        with tarfile.open(tar_path, 'r:gz') as t:
            files = t.getnames()
            print(f"Total files in tar: {len(files)}")
            print("\nFirst 30 files:")
            for f in files[:30]:
                print(f"  {f}")
            if len(files) > 30:
                print(f"  ... and {len(files) - 30} more files")
            
            # Show directory structure
            dirs = sorted(set(os.path.dirname(f) for f in files if os.path.dirname(f)))
            print(f"\nDirectory structure ({len(dirs)} directories):")
            for d in dirs[:20]:
                print(f"  {d}/")
            if len(dirs) > 20:
                print(f"  ... and {len(dirs) - 20} more directories")
    except Exception as e:
        print(f"ERROR reading tar file: {e}")
        return 1
    
    # Create backup branch
    print("\n" + "=" * 60)
    print("Creating Backup Branch")
    print("=" * 60)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_branch = f"backup-before-refactor-merge-{timestamp}"
    success, stdout, stderr = run_cmd(f"git branch {backup_branch}", cwd=workspace)
    if success:
        print(f"✓ Created backup branch: {backup_branch}")
    else:
        print(f"⚠ Could not create backup branch: {stderr}")
        if "already exists" not in stderr.lower():
            print("Continuing anyway...")
    
    # Create refactor/main branch
    print("\n" + "=" * 60)
    print("Creating refactor/main Branch")
    print("=" * 60)
    success, stdout, stderr = run_cmd("git checkout -b refactor/main", cwd=workspace)
    if success:
        print("✓ Created and checked out branch: refactor/main")
    else:
        if "already exists" in stderr.lower():
            print("⚠ Branch refactor/main already exists, checking it out...")
            success, _, _ = run_cmd("git checkout refactor/main", cwd=workspace)
            if success:
                print("✓ Checked out existing refactor/main branch")
            else:
                print(f"ERROR: Could not checkout refactor/main: {stderr}")
                return 1
        else:
            print(f"ERROR: Could not create branch: {stderr}")
            return 1
    
    # Extract tar file
    print("\n" + "=" * 60)
    print("Extracting Tar File")
    print("=" * 60)
    try:
        with tarfile.open(tar_path, 'r:gz') as t:
            t.extractall(path=workspace)
        print("✓ Tar file extracted successfully")
    except Exception as e:
        print(f"ERROR extracting tar file: {e}")
        return 1
    
    # Verify extraction
    print("\n" + "=" * 60)
    print("Verification")
    print("=" * 60)
    success, stdout, stderr = run_cmd("git status --short", cwd=workspace)
    if success:
        changed_files = [line for line in stdout.split('\n') if line.strip()]
        print(f"✓ Files changed: {len(changed_files)}")
        if changed_files:
            print("\nSample of changed files:")
            for line in changed_files[:20]:
                print(f"  {line}")
            if len(changed_files) > 20:
                print(f"  ... and {len(changed_files) - 20} more files")
    else:
        print(f"⚠ Could not check git status: {stderr}")
    
    # Check key files
    key_files = [
        "AgentQMS/agent_tools/compliance/validate_artifacts.py",
        ".agentqms/plugins/validators.yaml",
    ]
    print("\nKey files check:")
    for key_file in key_files:
        if os.path.exists(key_file):
            print(f"  ✓ {key_file}")
        else:
            print(f"  ⚠ {key_file} (not found)")
    
    # Stage and commit
    print("\n" + "=" * 60)
    print("Staging and Committing")
    print("=" * 60)
    success, stdout, stderr = run_cmd("git add -A", cwd=workspace)
    if success:
        print("✓ Staged all changes")
    else:
        print(f"⚠ Could not stage changes: {stderr}")
    
    success, stdout, stderr = run_cmd(
        'git commit -m "Extract integration test updates from agentqms-export.tar.gz"',
        cwd=workspace
    )
    if success:
        print("✓ Committed changes")
        print(f"  Commit message: Extract integration test updates from agentqms-export.tar.gz")
    else:
        if "nothing to commit" in stderr.lower():
            print("⚠ No changes to commit (files may be identical)")
        else:
            print(f"⚠ Could not commit: {stderr}")
    
    print("\n" + "=" * 60)
    print("Extraction Complete!")
    print("=" * 60)
    print(f"Backup branch: {backup_branch}")
    print(f"Current branch: refactor/main")
    print("\nNext steps:")
    print("1. Review the changes: git diff backup-before-refactor-merge-{timestamp}..refactor/main")
    print("2. Test the refactored code")
    print("3. Merge to main when ready")
    
    return 0

if __name__ == "__main__":
    exit(main())
