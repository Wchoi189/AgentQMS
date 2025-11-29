# Manual Extraction Steps

Since automated execution is having issues, here are the manual steps to complete the extraction:

## Scripts Created

1. `_extract_now.py` - Simple extraction script
2. `extract_tar.py` - Comprehensive extraction script  
3. `step_by_step_extract.py` - Step-by-step with verification
4. `final_extraction.py` - Final version with logging
5. `extract.mk` - Makefile version

## Manual Execution

Run one of these commands:

```bash
# Option 1: Simple script
python3 _extract_now.py

# Option 2: Comprehensive script
python3 extract_tar.py

# Option 3: Makefile
make -f extract.mk extract-tar
```

## What the Scripts Do

1. Verify tar file exists
2. Create backup branch: `backup-before-refactor-merge-{timestamp}`
3. Create and checkout `refactor/main` branch
4. Extract `agentqms-export.tar.gz` to workspace root
5. Stage all changes: `git add -A`
6. Commit: `git commit -m "Extract integration test updates from agentqms-export.tar.gz"`

## Verification

After running, verify:
- `git branch` should show `refactor/main`
- `git status` should show extracted files
- Key files like `AgentQMS/agent_tools/compliance/validate_artifacts.py` should be updated
