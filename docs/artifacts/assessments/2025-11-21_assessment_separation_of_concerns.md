---
type: "assessment"
category: "architecture"
status: "active"
version: "0.1"
tags: ["architecture", "separation-of-concerns", "refactoring"]
title: "Assessment: Separation of Concerns for agent_interface/ and agent_tools/"
date: "2025-11-21 05:15 (KST)"
author: "Project Maintainers"
---

# Assessment: Separation of Concerns for agent_interface/ and agent_tools/

## Current Structure Analysis

### agent_interface/
- **tools/** - Mixed concerns:
  - Thin wrappers (discover.py, feedback.py, quality.py) - just call agent_tools
  - MCP servers (audio, puppeteer) - actual implementations
  - Semantic search - actual implementation
- **workflows/** - Bash scripts (already converted to Python in agent_tools/workflows/)
- **docs/** - Documentation artifacts (should be in main docs/)
- **index.md, README.md** - Documentation

### agent_tools/
- **core/** - Core implementations (discover, artifact_workflow, context_bundle)
- **compliance/** - Compliance tools
- **utilities/** - Utilities (agent_feedback, puppeteer_wrapper, etc.)
- **audit/** - Audit tools
- **documentation/** - Documentation tools
- **maintenance/** - Maintenance tools
- **migration/** - Migration tools
- **wrappers/** - Duplicate of agent_interface/tools/ (inappropriate)
- **workflows/** - Python workflows
- **cli.py** - CLI entry point
- **utils/** - Utility functions

## Problems Identified

1. **❌ `tools/` directory is inappropriate** - Mixes wrappers and implementations
2. **❌ Duplication** - `agent_interface/tools/` and `agent_tools/wrappers/` are duplicates
3. **❌ Unclear separation** - Wrappers vs implementations vs MCP servers
4. **❌ Mixed concerns** - Thin wrappers mixed with actual MCP server implementations
5. **❌ Documentation in wrong place** - `agent_interface/docs/` should be in main `docs/`

## Proper Separation of Concerns

### 1. **Core Tools** (`agent_tools/core/`)
- Essential automation tools
- Artifact workflows
- Discovery tools
- Context bundles

### 2. **Domain Tools** (by function)
- `agent_tools/compliance/` - Compliance and validation
- `agent_tools/audit/` - Audit tools
- `agent_tools/documentation/` - Documentation management
- `agent_tools/maintenance/` - Maintenance scripts
- `agent_tools/migration/` - Migration tools

### 3. **Integrations** (`agent_tools/integrations/`)
- MCP servers (audio, puppeteer)
- External service integrations
- Specialized tools (semantic_search)

### 4. **Utilities** (`agent_tools/utilities/`)
- Helper functions
- Shared utilities
- Common functionality

### 5. **CLI** (`agent_tools/cli.py`)
- Single entry point
- No wrappers needed - CLI calls implementations directly

### 6. **Utils** (`agent_tools/utils/`)
- Framework utilities (config, paths, state)

## Proposed Structure

```
agent_tools/
├── cli.py                    # Single CLI entry point
├── core/                     # Core tools
│   ├── discover.py
│   ├── artifact_workflow.py
│   └── context_bundle.py
├── compliance/               # Compliance tools
├── audit/                    # Audit tools
├── documentation/            # Documentation tools
├── maintenance/              # Maintenance tools
├── migration/                # Migration tools
├── integrations/             # External integrations (NEW)
│   ├── mcp/                  # MCP servers
│   │   ├── audio.py
│   │   └── puppeteer.py
│   └── semantic_search.py
├── utilities/                # Utilities
│   ├── agent_feedback.py
│   └── ...
├── workflows/                # Workflow scripts
└── utils/                    # Framework utilities
    ├── config.py
    ├── paths.py
    └── state_manager.py
```

## Migration Plan

1. **Remove `wrappers/`** - Inappropriate directory
2. **Move MCP servers** - `agent_interface/tools/audio/` → `agent_tools/integrations/mcp/audio.py`
3. **Move semantic_search** - `agent_interface/tools/semantic_search/` → `agent_tools/integrations/semantic_search.py`
4. **Remove thin wrappers** - discover.py, feedback.py, quality.py (CLI calls implementations directly)
5. **Move docs** - `agent_interface/docs/` → `docs/` (if needed)
6. **Remove `agent_interface/`** - No longer needed
7. **Update CLI** - Call implementations directly, no wrappers

## Benefits

- ✅ **Clear separation** - Core, domain, integrations, utilities
- ✅ **No duplication** - Single source of truth
- ✅ **No inappropriate `tools/`** - Proper categorization
- ✅ **Simple CLI** - Direct calls to implementations
- ✅ **Maintainable** - Clear structure

