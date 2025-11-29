#!/usr/bin/env python3
"""Direct extraction script."""
import os
import subprocess
import tarfile
import sys
from datetime import datetime
from pathlib import Path

workspace = Path("/workspaces/agent_qms")
os.chdir(workspace)

# Verify tar
tar_path = workspace / "agentqms-export.tar.gz"
if not tar_path.exists():
    print(f"ERROR: {tar_path} not found!", file=sys.stderr)
    sys.exit(1)

print(f"Tar file: {tar_path.stat().st_size:,} bytes")

# Git operations
def git_cmd(cmd_list, check=True):
    """Run git command."""
    try:
        result = subprocess.run(
            ["git"] + cmd_list,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30
        )
        if check and result.returncode != 0:
            print(f"Git error: {result.stderr}", file=sys.stderr)
            return None
        return result
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

# Get current branch
result = git_cmd(["branch", "--show-current"], check=False)
current_branch = result.stdout.strip() if result and result.returncode == 0 else "unknown"
print(f"Current branch: {current_branch}")

# Create backup
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_branch = f"backup-before-refactor-merge-{timestamp}"
result = git_cmd(["branch", backup_branch], check=False)
if result and result.returncode == 0:
    print(f"Created backup: {backup_branch}")
elif result and "already exists" in result.stderr:
    print(f"Backup exists: {backup_branch}")

# Create/checkout refactor/main
result = git_cmd(["show-ref", "--verify", "--quiet", "refs/heads/refactor/main"], check=False)
if result and result.returncode == 0:
    result = git_cmd(["checkout", "refactor/main"])
    if result:
        print("Checked out existing refactor/main")
else:
    result = git_cmd(["checkout", "-b", "refactor/main"])
    if result:
        print("Created and checked out refactor/main")

# Extract tar
print("Extracting tar file...")
try:
    with tarfile.open(tar_path, 'r:gz') as t:
        t.extractall(path=workspace)
    print("Extraction complete")
except Exception as e:
    print(f"Extraction error: {e}", file=sys.stderr)
    sys.exit(1)

# Verify
result = git_cmd(["status", "--short"], check=False)
if result and result.returncode == 0:
    changed = [l for l in result.stdout.split('\n') if l.strip()]
    print(f"Files changed: {len(changed)}")

# Stage and commit
git_cmd(["add", "-A"])
result = git_cmd(["commit", "-m", "Extract integration test updates from agentqms-export.tar.gz"], check=False)
if result and result.returncode == 0:
    print("Committed changes")
elif result and "nothing to commit" in result.stderr:
    print("No changes to commit")

print(f"\nDone! Backup: {backup_branch}, Branch: refactor/main")
