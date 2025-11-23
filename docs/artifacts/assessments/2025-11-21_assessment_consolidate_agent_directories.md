---
type: "assessment"
category: "architecture"
status: "active"
version: "0.1"
tags: ["architecture", "consolidation", "refactoring"]
title: "Assessment: Consolidating agent_interface/ and agent_tools/"
date: "2025-11-21 05:00 (KST)"
author: "Project Maintainers"
---

# Assessment: Consolidating agent_interface/ and agent_tools/

## Problem

The current architecture has two separate directories that create confusion:

1. **`agent_interface/`** - Thin wrapper layer with:
   - Makefile for agent commands
   - Wrapper Python scripts
   - Bash workflow scripts
   - Some specialized tools (semantic_search, puppeteer, audio)
   - Documentation artifacts

2. **`agent_tools/`** - Implementation layer with:
   - Core tool implementations
   - Utilities, compliance, audit tools
   - Documentation, maintenance tools
   - All actual functionality

**Issues:**
- ❌ Confusing separation - unclear which directory to use
- ❌ Duplication - wrapper scripts that just call implementations
- ❌ Complex entry points - Makefile + bash scripts + Python wrappers
- ❌ Maintenance burden - changes needed in multiple places
- ❌ Hard to discover - agents don't know where to look

## Proposed Solution

### Consolidate into `agent_tools/` with Simple CLI

**Single Directory Structure:**
```
agent_tools/
├── __init__.py
├── cli.py              # Ultra-concise CLI wrapper (NEW)
├── core/               # Core tools (existing)
├── utilities/          # Utilities (existing)
├── compliance/         # Compliance tools (existing)
├── audit/              # Audit tools (existing)
├── documentation/      # Documentation tools (existing)
├── maintenance/        # Maintenance tools (existing)
├── migration/          # Migration tools (existing)
├── wrappers/           # Simple wrappers for specialized tools (NEW)
│   ├── semantic_search.py
│   ├── puppeteer.py
│   └── audio.py
└── workflows/          # Workflow scripts (moved from agent_interface)
    ├── create_artifact.py
    ├── validate.py
    └── compliance.py
```

### Ultra-Concise CLI Design

**Simple Python CLI:** `agentqms <command> [args]`

```python
# agent_tools/cli.py
"""
Ultra-concise CLI for AgentQMS tools.

Usage:
    agentqms discover
    agentqms create-plan --name my-plan --title "My Plan"
    agentqms validate
    agentqms compliance
    agentqms help
"""
```

**Benefits:**
- ✅ Single entry point - `agentqms` command
- ✅ No Makefile needed - pure Python
- ✅ No bash scripts - all Python
- ✅ Easy to discover - `agentqms help` shows all commands
- ✅ Simple to use - `agentqms <command>`
- ✅ Easy to extend - just add new commands

### Migration Plan

1. **Create `agent_tools/cli.py`** - Simple CLI wrapper
2. **Move useful tools** from `agent_interface/tools/` to `agent_tools/wrappers/`
3. **Convert workflows** from bash to Python in `agent_tools/workflows/`
4. **Update documentation** - single source of truth
5. **Remove `agent_interface/`** - no longer needed
6. **Update path references** - remove `agent_interface` from config

## Benefits

- ✅ **Simpler**: One directory, one CLI
- ✅ **Clearer**: No confusion about which directory to use
- ✅ **Easier**: `agentqms <command>` is ultra-concise
- ✅ **Maintainable**: Single source of truth
- ✅ **Discoverable**: `agentqms help` shows everything

## Implementation Steps

1. Create `agent_tools/cli.py` with basic command structure
2. Move specialized tools to `agent_tools/wrappers/`
3. Convert bash workflows to Python
4. Update all imports and references
5. Remove `agent_interface/` directory
6. Update documentation

