---
type: "implementation_plan"
category: "architecture"
status: "completed"
version: "0.1"
tags: ["architecture", "separation-of-concerns", "refactoring"]
title: "Implementation Plan: Separation of Concerns Reorganization"
date: "2025-11-21 05:20 (KST)"
author: "Project Maintainers"
---

# Implementation Plan: Separation of Concerns Reorganization

## Objective

Reorganize `agent_interface/` and `agent_tools/` with clear separation of concerns, removing the inappropriate `tools/` directory and eliminating duplication.

## Problem

1. **Inappropriate `tools/` directory** - Mixed wrappers and implementations
2. **Duplication** - `agent_interface/tools/` and `agent_tools/wrappers/` were duplicates
3. **Unclear separation** - Wrappers vs implementations vs MCP servers
4. **Mixed concerns** - Thin wrappers mixed with actual MCP server implementations

## Solution

### Proper Separation of Concerns

1. **Core Tools** (`agent_tools/core/`) - Essential automation tools
2. **Domain Tools** - Compliance, audit, documentation, maintenance, migration
3. **Integrations** (`agent_tools/integrations/`) - MCP servers and external integrations
4. **Utilities** (`agent_tools/utilities/`) - Helper functions
5. **CLI** (`agent_tools/cli.py`) - Single entry point, no wrappers needed

## Implementation Steps

### ✅ Completed

1. **Removed `wrappers/` directory** - Inappropriate directory eliminated
2. **Created `integrations/` directory** - Proper home for MCP servers
3. **Moved MCP servers** - `agent_interface/tools/audio/` → `agent_tools/integrations/mcp/audio/`
4. **Moved MCP servers** - `agent_interface/tools/puppeteer/` → `agent_tools/integrations/mcp/puppeteer/`
5. **Moved semantic_search** - `agent_interface/tools/semantic_search/` → `agent_tools/integrations/semantic_search/`
6. **Updated CLI** - Added feedback and quality commands, calls implementations directly
7. **Updated documentation** - Removed references to wrappers and agent_interface

## New Structure

```
agent_tools/
├── cli.py                    # Single CLI entry point
├── core/                     # Core tools
├── compliance/               # Compliance tools
├── audit/                    # Audit tools
├── documentation/            # Documentation tools
├── maintenance/              # Maintenance tools
├── migration/                # Migration tools
├── integrations/             # External integrations
│   ├── mcp/                  # MCP servers
│   │   ├── audio/
│   │   └── puppeteer/
│   └── semantic_search/
├── utilities/                # Utilities
├── workflows/                # Workflow scripts
└── utils/                    # Framework utilities
```

## Benefits

- ✅ **Clear separation** - Core, domain, integrations, utilities
- ✅ **No duplication** - Single source of truth
- ✅ **No inappropriate `tools/`** - Proper categorization
- ✅ **Simple CLI** - Direct calls to implementations
- ✅ **Maintainable** - Clear structure

## Next Steps

1. **Remove `agent_interface/`** - After verification (contains only docs and thin wrappers)
2. **Update remaining references** - Fix any code that still references agent_interface
3. **Update documentation** - Remove all references to agent_interface

## Verification

- [x] `wrappers/` directory removed
- [x] `integrations/` directory created
- [x] MCP servers moved to `integrations/mcp/`
- [x] Semantic search moved to `integrations/`
- [x] CLI updated with feedback and quality commands
- [x] Documentation updated

