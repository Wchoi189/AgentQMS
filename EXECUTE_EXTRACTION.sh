#!/bin/bash
# Execute the tar extraction and branch setup
# This script performs all steps from the plan

set -e

cd /workspaces/agent_qms

echo "=========================================="
echo "Extracting Integration Test Updates"
echo "=========================================="

# Step 1: Verify tar file
if [ ! -f "agentqms-export.tar.gz" ]; then
    echo "ERROR: agentqms-export.tar.gz not found!"
    exit 1
fi
echo "✓ Tar file found: $(du -h agentqms-export.tar.gz | cut -f1)"

# Step 2: Create backup branch
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_BRANCH="backup-before-refactor-merge-${TIMESTAMP}"
echo "Creating backup branch: ${BACKUP_BRANCH}"
git branch "${BACKUP_BRANCH}" || echo "Backup branch may already exist"

# Step 3: Create/checkout refactor/main
echo "Creating/checking out refactor/main branch..."
if git show-ref --verify --quiet refs/heads/refactor/main; then
    echo "Branch refactor/main exists, checking it out..."
    git checkout refactor/main
else
    echo "Creating new branch refactor/main..."
    git checkout -b refactor/main
fi

# Step 4: Extract tar file
echo "Extracting tar file..."
python3 << 'PYTHON_EOF'
import tarfile
from pathlib import Path

workspace = Path("/workspaces/agent_qms")
tar_path = workspace / "agentqms-export.tar.gz"

with tarfile.open(tar_path, 'r:gz') as t:
    files = t.getnames()
    print(f"  Extracting {len(files)} files...")
    t.extractall(workspace)
    print("  ✓ Extraction complete")
PYTHON_EOF

# Step 5: Stage changes
echo "Staging changes..."
git add -A

# Step 6: Commit
echo "Committing changes..."
git commit -m "Extract integration test updates from agentqms-export.tar.gz" || echo "No changes to commit or commit failed"

echo ""
echo "=========================================="
echo "Extraction Complete!"
echo "=========================================="
echo "Backup branch: ${BACKUP_BRANCH}"
echo "Current branch: $(git branch --show-current)"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff ${BACKUP_BRANCH}..refactor/main"
echo "2. Test the refactored code"
echo "3. Merge to main when ready"
