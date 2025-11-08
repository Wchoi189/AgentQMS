#!/usr/bin/env python3
"""
Initialize agent tools for the Korean Grammar Correction project.
Sets up the documentation index and initializes the agent tools system.
"""

import json
import subprocess
import sys
from datetime import UTC, datetime
from typing import Any

from project_config import (
    CONTEXT_BUNDLES,
    DIRECTORY_STRUCTURE,
    HANDBOOK_DIR,
    INDEX_PATH,
    PROJECT_ROOT,
)


def create_initial_index() -> dict[str, Any]:
    """Create the initial index.json file for the AI handbook."""

    # Create initial entries based on existing files
    entries = []

    # Quick context reference
    entries.append(
        {
            "id": "quick_context_reference",
            "title": "Quick Context Reference for AI Agents",
            "path": "./01_onboarding/quick-context-reference.md",
            "section": "Onboarding (How-To Guides)",
            "tags": ["quick", "context", "onboarding"],
            "priority": "high",
            "summary": "Single-page context summary for rapid agent onboarding",
            "last_reviewed": datetime.now(UTC).strftime("%Y-%m-%d"),
            "owner": "core",
            "bundles": ["quick-start", "development", "debugging"],
        }
    )

    # AI Agent Entry Point
    entries.append(
        {
            "id": "ai_agent_entry_point",
            "title": "AI Agent Entry Point",
            "path": "./ai-agent-entry-point.md",
            "section": "Onboarding (How-To Guides)",
            "tags": ["entry", "point", "onboarding"],
            "priority": "high",
            "summary": "Single source of truth for all AI agents working on the project",
            "last_reviewed": datetime.now(UTC).strftime("%Y-%m-%d"),
            "owner": "core",
            "bundles": ["quick-start"],
        }
    )

    # Architecture Summary
    entries.append(
        {
            "id": "architecture_summary",
            "title": "Architecture Summary for AI Agents",
            "path": "./03_references/architecture-summary.md",
            "section": "References (Factual Information)",
            "tags": ["architecture", "system", "overview"],
            "priority": "high",
            "summary": "High-level system understanding without deep code diving",
            "last_reviewed": datetime.now(UTC).strftime("%Y-%m-%d"),
            "owner": "core",
            "bundles": ["development", "debugging"],
        }
    )

    # Context Optimization Plan
    entries.append(
        {
            "id": "context_optimization_plan",
            "title": "Context Optimization Plan for AI Agents",
            "path": "./03_references/context_optimization/optimization-plan.md",
            "section": "References (Factual Information)",
            "tags": ["optimization", "context", "plan"],
            "priority": "medium",
            "summary": "Reduce agent context-switching time by 70% and improve task completion accuracy",
            "last_reviewed": datetime.now(UTC).strftime("%Y-%m-%d"),
            "owner": "documentation",
            "bundles": ["documentation"],
        }
    )

    # Context Templates
    entries.append(
        {
            "id": "context_templates",
            "title": "Context Templates for AI Agents",
            "path": "./02_protocols/development/context-templates.md",
            "section": "Protocols (How-To Guides)",
            "tags": ["template", "context", "protocol"],
            "priority": "medium",
            "summary": "Standardized context structures for consistent agent understanding",
            "last_reviewed": datetime.now(UTC).strftime("%Y-%m-%d"),
            "owner": "documentation",
            "bundles": ["development", "documentation"],
        }
    )

    # Smart Context Loading
    entries.append(
        {
            "id": "smart_context_loading",
            "title": "Smart Context Loading for AI Agents",
            "path": "./03_references/context_optimization/smart-context-loading.md",
            "section": "References (Factual Information)",
            "tags": ["loading", "context", "optimization"],
            "priority": "medium",
            "summary": "Optimize context delivery based on task type and agent needs",
            "last_reviewed": datetime.now(UTC).strftime("%Y-%m-%d"),
            "owner": "documentation",
            "bundles": ["documentation"],
        }
    )

    # Create the index structure
    index_data = {
        "source": "docs/ai_handbook/index.md",
        "version": "1.0 (2025-01-27)",
        "generated_at": datetime.now(UTC).isoformat(),
        "schema": DIRECTORY_STRUCTURE,
        "entries": entries,
        "bundles": CONTEXT_BUNDLES,
    }

    return index_data


def create_quick_fixes_file() -> None:
    """Create the initial QUICK_FIXES.md file."""
    quick_fixes_content = """# Quick Fixes Log

This log tracks quick fixes, patches, and hotfixes applied to the Korean Grammar Correction codebase.
Format follows the [Quick Fixes Protocol](docs/ai_handbook/02_protocols/development/context-templates.md).

## Recent Fixes

---

## 2025-01-27 14:30 LINT - Resolved 31 linting errors

**Issue**: Multiple linting errors preventing clean codebase
**Fix**: Fixed import issues, type annotations, unreachable statements, and call overloads
**Files**: prompt_formatter.py, metrics.py, data_tables.py, error_distribution_search.py, evaluate.py, compare_prompts.py, data_service_backup.py, process_manager.py, pyproject.toml
**Impact**: minimal
**Test**: make lint

---

## 2025-01-27 15:00 DOC - Relocated documentation to proper schema

**Issue**: Documentation files created in wrong locations
**Fix**: Moved files to conform to organization schema with proper naming
**Files**: docs/ai_handbook/ (multiple files relocated)
**Impact**: minimal
**Test**: manual

---

## 2025-01-27 15:15 TOOL - Initialized agent tools system

**Issue**: Agent tools from previous project needed repurposing
**Fix**: Created project-specific configuration and initialized index system
**Files**: scripts/agent_tools/project_config.py, scripts/agent_tools/init_project.py, docs/ai_handbook/index.json
**Impact**: minimal
**Test**: manual

---

"""

    quick_fixes_path = PROJECT_ROOT / "docs" / "QUICK_FIXES.md"
    quick_fixes_path.write_text(quick_fixes_content, encoding="utf-8")
    print(f"✅ Created {quick_fixes_path}")


def run_auto_generate_index() -> bool:
    """Run the auto-generate index script."""
    try:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/agent_tools/auto_generate_index.py",
                "--handbook-dir",
                str(HANDBOOK_DIR),
                "--output",
                str(INDEX_PATH),
                "--validate",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Auto-generated index successfully")
            print(result.stdout)
        else:
            print("❌ Auto-generate index failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running auto-generate index: {e}")
        return False

    return True


def main() -> None:
    """Initialize the agent tools system for this project."""
    print("🚀 Initializing Agent Tools for Korean Grammar Correction Project")
    print()

    # Ensure directories exist
    HANDBOOK_DIR.mkdir(parents=True, exist_ok=True)
    (HANDBOOK_DIR / "03_references" / "context_optimization").mkdir(
        parents=True, exist_ok=True
    )

    print("1. Creating initial index.json...")
    index_data = create_initial_index()

    # Write initial index
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Created {INDEX_PATH}")

    print("\n2. Creating QUICK_FIXES.md...")
    create_quick_fixes_file()

    print("\n3. Running auto-generate index to update with all files...")
    if run_auto_generate_index():
        print("✅ Agent tools initialization complete!")
        print()
        print("📋 Next steps:")
        print("  - Run: python scripts/agent_tools/get_context.py --list-bundles")
        print("  - Run: python scripts/agent_tools/get_context.py --bundle quick-start")
        print(
            "  - Use: python scripts/agent_tools/quick_fix_log.py <type> <title> --issue <issue> --fix <fix> --files <files>"
        )
    else:
        print("❌ Initialization completed with warnings")
        print("   Check the output above for details")


if __name__ == "__main__":
    main()
