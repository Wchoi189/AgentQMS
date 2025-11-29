#!/usr/bin/env python3
"""Step-by-step extraction with verification."""
import os
import subprocess
import tarfile
import sys
from datetime import datetime
from pathlib import Path

workspace = Path("/workspaces/agent_qms")
os.chdir(workspace)

# Step 1: Verify tar file
print("Step 1: Verifying tar file...")
tar_path = workspace / "agentqms-export.tar.gz"
if not tar_path.exists():
    print(f"ERROR: {tar_path} not found!")
    sys.exit(1)
print(f"✓ Tar file exists: {tar_path.stat().st_size:,} bytes")

# Step 2: Check git status
print("\nStep 2: Checking git status...")
try:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        if result.stdout.strip():
            print(f"⚠ Uncommitted changes:\n{result.stdout}")
        else:
            print("✓ Working directory is clean")
    else:
        print(f"⚠ Git status check failed: {result.stderr}")
except Exception as e:
    print(f"⚠ Could not check git status: {e}")

# Step 3: Get current branch
print("\nStep 3: Getting current branch...")
try:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        current_branch = result.stdout.strip()
        print(f"✓ Current branch: {current_branch}")
    else:
        print(f"⚠ Could not get branch: {result.stderr}")
        current_branch = "unknown"
except Exception as e:
    print(f"⚠ Error: {e}")
    current_branch = "unknown"

# Step 4: List tar contents
print("\nStep 4: Listing tar contents...")
try:
    with tarfile.open(tar_path, 'r:gz') as t:
        files = t.getnames()
        print(f"✓ Total files in tar: {len(files)}")
        print(f"  Sample files: {files[:5]}")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# Step 5: Create backup branch
print("\nStep 5: Creating backup branch...")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_branch = f"backup-before-refactor-merge-{timestamp}"
try:
    result = subprocess.run(
        ["git", "branch", backup_branch],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print(f"✓ Created backup branch: {backup_branch}")
    else:
        if "already exists" in result.stderr.lower():
            print(f"⚠ Backup branch already exists: {backup_branch}")
        else:
            print(f"⚠ Could not create backup: {result.stderr}")
except Exception as e:
    print(f"⚠ Error creating backup: {e}")

# Step 6: Create refactor/main branch
print("\nStep 6: Creating refactor/main branch...")
try:
    # Check if branch exists
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", "refs/heads/refactor/main"],
        cwd=workspace,
        capture_output=True,
        timeout=10
    )
    branch_exists = result.returncode == 0
    
    if branch_exists:
        print("⚠ Branch refactor/main exists, checking it out...")
        result = subprocess.run(
            ["git", "checkout", "refactor/main"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Checked out existing refactor/main branch")
        else:
            print(f"ERROR: Could not checkout: {result.stderr}")
            sys.exit(1)
    else:
        result = subprocess.run(
            ["git", "checkout", "-b", "refactor/main"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Created and checked out refactor/main branch")
        else:
            print(f"ERROR: Could not create branch: {result.stderr}")
            sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# Step 7: Extract tar file
print("\nStep 7: Extracting tar file...")
try:
    with tarfile.open(tar_path, 'r:gz') as t:
        t.extractall(path=workspace)
    print("✓ Tar file extracted successfully")
except Exception as e:
    print(f"ERROR extracting tar: {e}")
    sys.exit(1)

# Step 8: Verify extraction
print("\nStep 8: Verifying extraction...")
try:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        changed = [l for l in result.stdout.split('\n') if l.strip()]
        print(f"✓ Files changed: {len(changed)}")
        if changed:
            print(f"  Sample: {changed[:3]}")
    else:
        print(f"⚠ Could not check status: {result.stderr}")
except Exception as e:
    print(f"⚠ Error: {e}")

# Step 9: Check key files
print("\nStep 9: Checking key files...")
key_files = [
    "AgentQMS/agent_tools/compliance/validate_artifacts.py",
    ".agentqms/plugins/validators.yaml",
]
for key_file in key_files:
    if (workspace / key_file).exists():
        print(f"  ✓ {key_file}")
    else:
        print(f"  ⚠ {key_file} (not found)")

# Step 10: Stage and commit
print("\nStep 10: Staging changes...")
try:
    result = subprocess.run(
        ["git", "add", "-A"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print("✓ Staged all changes")
    else:
        print(f"⚠ Could not stage: {result.stderr}")
except Exception as e:
    print(f"⚠ Error staging: {e}")

print("\nStep 11: Committing changes...")
try:
    result = subprocess.run(
        ["git", "commit", "-m", "Extract integration test updates from agentqms-export.tar.gz"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print("✓ Committed changes")
    else:
        if "nothing to commit" in result.stderr.lower():
            print("⚠ No changes to commit")
        else:
            print(f"⚠ Could not commit: {result.stderr}")
except Exception as e:
    print(f"⚠ Error committing: {e}")

print("\n" + "=" * 60)
print("Extraction Complete!")
print("=" * 60)
print(f"Backup branch: {backup_branch}")
print(f"Current branch: refactor/main")
