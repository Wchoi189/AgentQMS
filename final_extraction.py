#!/usr/bin/env python3
"""Final extraction script with file logging."""
import os
import subprocess
import tarfile
import sys
from datetime import datetime
from pathlib import Path

log_file = Path("/workspaces/agent_qms/extraction_results.txt")
workspace = Path("/workspaces/agent_qms")
os.chdir(workspace)

def log(msg):
    """Log message to both stdout and file."""
    print(msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')

log("=" * 60)
log("Starting Extraction Process")
log("=" * 60)

# Step 1: Verify tar
tar_path = workspace / "agentqms-export.tar.gz"
if not tar_path.exists():
    log(f"ERROR: {tar_path} not found!")
    sys.exit(1)
log(f"✓ Tar file: {tar_path.stat().st_size:,} bytes")

# Step 2: Git status
log("\nChecking git status...")
try:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.stdout.strip():
        log(f"⚠ Uncommitted: {result.stdout.strip()[:200]}")
    else:
        log("✓ Working directory clean")
except Exception as e:
    log(f"⚠ Status check failed: {e}")

# Step 3: Current branch
log("\nGetting current branch...")
try:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30
    )
    current_branch = result.stdout.strip() if result.returncode == 0 else "unknown"
    log(f"✓ Current branch: {current_branch}")
except Exception as e:
    log(f"⚠ Error: {e}")
    current_branch = "unknown"

# Step 4: Create backup
log("\nCreating backup branch...")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_branch = f"backup-before-refactor-merge-{timestamp}"
try:
    result = subprocess.run(
        ["git", "branch", backup_branch],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode == 0:
        log(f"✓ Backup created: {backup_branch}")
    elif "already exists" in result.stderr:
        log(f"⚠ Backup exists: {backup_branch}")
    else:
        log(f"⚠ Backup creation: {result.stderr}")
except Exception as e:
    log(f"⚠ Backup error: {e}")

# Step 5: Create/checkout refactor/main
log("\nCreating refactor/main branch...")
try:
    # Check if exists
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", "refs/heads/refactor/main"],
        cwd=workspace,
        timeout=30
    )
    exists = result.returncode == 0
    
    if exists:
        result = subprocess.run(
            ["git", "checkout", "refactor/main"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            log("✓ Checked out existing refactor/main")
        else:
            log(f"ERROR: {result.stderr}")
            sys.exit(1)
    else:
        result = subprocess.run(
            ["git", "checkout", "-b", "refactor/main"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            log("✓ Created and checked out refactor/main")
        else:
            log(f"ERROR: {result.stderr}")
            sys.exit(1)
except Exception as e:
    log(f"ERROR: {e}")
    sys.exit(1)

# Step 6: Extract tar
log("\nExtracting tar file...")
try:
    with tarfile.open(tar_path, 'r:gz') as t:
        files = t.getnames()
        log(f"  Total files: {len(files)}")
        t.extractall(path=workspace)
    log("✓ Extraction complete")
except Exception as e:
    log(f"ERROR: {e}")
    sys.exit(1)

# Step 7: Verify
log("\nVerifying extraction...")
try:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode == 0:
        changed = [l for l in result.stdout.split('\n') if l.strip()]
        log(f"✓ Files changed: {len(changed)}")
        if changed:
            log(f"  Sample: {changed[:5]}")
except Exception as e:
    log(f"⚠ Verification error: {e}")

# Step 8: Key files
log("\nChecking key files...")
key_files = [
    "AgentQMS/agent_tools/compliance/validate_artifacts.py",
    ".agentqms/plugins/validators.yaml",
]
for kf in key_files:
    if (workspace / kf).exists():
        log(f"  ✓ {kf}")
    else:
        log(f"  ⚠ {kf} missing")

# Step 9: Stage
log("\nStaging changes...")
try:
    result = subprocess.run(
        ["git", "add", "-A"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode == 0:
        log("✓ Staged")
    else:
        log(f"⚠ Stage error: {result.stderr}")
except Exception as e:
    log(f"⚠ Error: {e}")

# Step 10: Commit
log("\nCommitting...")
try:
    result = subprocess.run(
        ["git", "commit", "-m", "Extract integration test updates from agentqms-export.tar.gz"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode == 0:
        log("✓ Committed")
    elif "nothing to commit" in result.stderr:
        log("⚠ Nothing to commit")
    else:
        log(f"⚠ Commit error: {result.stderr}")
except Exception as e:
    log(f"⚠ Error: {e}")

log("\n" + "=" * 60)
log("Extraction Complete!")
log("=" * 60)
log(f"Backup: {backup_branch}")
log(f"Branch: refactor/main")
