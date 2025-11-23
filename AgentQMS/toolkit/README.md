---
 title: "Agent Tools Quick Pointer"
 date: "2025-11-06 00:00 (KST)"
 type: "documentation"
 category: "usage"
 status: "active"
 version: "1.1"
 tags: ["agent-tools", "pointer"]
---

# Agent Tools (Ultra-Concise)

This directory holds implementation code. For documentation, see the central guide:

- Central Guide: `docs/ai_handbook/04_agent_system/automation/tooling_overview.md`

Minimal quick commands:

```bash
# Discover tools
python scripts/agent_tools/core/discover.py

# Create artifact (always use workflow)
python scripts/agent_tools/core/artifact_workflow.py create --type implementation_plan --name my-plan --title "My Plan"

# Tracking (DB init, CLI, export)
make -C agent track-init
python scripts/agent_tools/utilities/tracking/cli.py plan status --concise
make -C agent exp-export OUT=data/ops/experiment_runs.csv
```

No long-form docs here to keep this directory clean for AI agents.
