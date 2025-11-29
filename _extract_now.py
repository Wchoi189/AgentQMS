#!/usr/bin/env python3
import tarfile
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ws = Path("/workspaces/agent_qms")
tar = ws / "agentqms-export.tar.gz"

# Extract
print("Extracting...", file=sys.stderr)
with tarfile.open(tar, 'r:gz') as t:
    files = t.getnames()
    print(f"Files: {len(files)}", file=sys.stderr)
    t.extractall(ws)
print("Done", file=sys.stderr)

# Git: backup branch
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = f"backup-before-refactor-merge-{ts}"
subprocess.run(["git", "branch", backup], cwd=ws, check=False)

# Git: create refactor/main
subprocess.run(["git", "checkout", "-b", "refactor/main"], cwd=ws, check=False)

# Git: stage
subprocess.run(["git", "add", "-A"], cwd=ws, check=False)

# Git: commit
subprocess.run(["git", "commit", "-m", "Extract integration test updates"], cwd=ws, check=False)

print("Complete", file=sys.stderr)
