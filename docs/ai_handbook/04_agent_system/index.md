---
title: "AI Agent Documentation Map"
date: "2025-11-07 00:00 (KST)"
type: "guide"
category: "ai_agent"
status: "active"
version: "1.0"
tags: ["index", "ai_agent", "reference"]
---

AI Agent Documentation Map
==========================

Use this index to choose the right file. Keep docs concise; avoid duplicating content across files.

## Core Rules

- `system.md` → Single source of truth for AI agent behaviour. Read first.
- `index.md` (this file) → Doc map so agents know where to look.

## Tracking

- `tracking/cli_reference.md` → Commands, recipes, and troubleshooting for the tracking CLI.
- `tracking/db_api.md` → SQLite tracking DB schema & CRUD API.

## Automation

- `automation/tooling_overview.md` → Human-curated overview of automation scripts.
- `automation/tool_catalog.md` → Generated catalog of all agent tools (read-only).
- `automation/changelog_process.md` → Semi-automated CHANGELOG workflow.

## Coding Protocols

- `coding_protocols/streamlit.md` → Coding rules when modifying Streamlit app code.

## Reserved Domains

- `docs_governance/` → Reserve for version/deprecation policy docs (create when needed).
- `artifact_workflow/` → Reserve for blueprint/protocol deep dives (create when needed).

## Scaling Guidance

- If any domain folder under `docs/ai_handbook/04_agent_system/` holds >8 active docs or a typical feature update touches 3+ domain files, migrate to the capability-based knowledge base (Option 3). Track counts with `find docs/ai_handbook/04_agent_system -mindepth 2 -maxdepth 2 -name '*.md' | awk -F/ '{print $(NF-1)}' | sort | uniq -c`.

Guidelines
----------
- Add new AI agent docs only if they fill a gap and link them here.
- If content grows beyond a quick reference, move detailed material into `docs/ai_handbook/` and keep a short pointer here.
