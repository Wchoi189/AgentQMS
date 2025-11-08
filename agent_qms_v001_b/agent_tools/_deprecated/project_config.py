#!/usr/bin/env python3
"""
Project-specific configuration for agent tools.
Adapts the generic agent tools for the Korean Grammar Correction project.
"""

from pathlib import Path

# Project-specific paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
HANDBOOK_DIR = PROJECT_ROOT / "docs" / "ai_handbook"
INDEX_PATH = HANDBOOK_DIR / "index.json"
QUICK_FIXES_PATH = PROJECT_ROOT / "docs" / "QUICK_FIXES.md"

# Project-specific directory structure mapping
DIRECTORY_STRUCTURE = {
    "01_onboarding": {
        "purpose": "Contains introductory documents for new contributors (human or AI).",
        "naming_convention": "NN_descriptive_topic.md",
        "allowed_content": "Only Markdown (.md) documents.",
        "prohibited_content": "Code, outputs, logs, experimental notes.",
    },
    "02_protocols": {
        "purpose": "Actionable, step-by-step instructions for recurring tasks, organized by category.",
        "naming_convention": "NN_protocol_name.md",
        "allowed_content": "Only Markdown (.md) documents defining a process.",
        "prohibited_content": "Generated outputs, work-in-progress notes. Outputs from protocol execution belong in the root /outputs directory.",
        "subdirectories": {
            "development": "Core development practices and workflows",
            "governance": "Documentation and maintenance protocols",
        },
    },
    "03_references": {
        "purpose": "Factual, descriptive information about the project's architecture, tools, and data, organized by category.",
        "naming_convention": "NN_reference_topic.md",
        "allowed_content": "Only Markdown (.md) documents.",
        "prohibited_content": "Tutorials, step-by-step guides (these are protocols).",
        "subdirectories": {
            "architecture": "Core system architecture documentation",
            "context_optimization": "Context optimization and agent efficiency documentation",
        },
    },
}

# Project-specific priority mapping
PRIORITY_MAP = {
    "high": ["quick", "context", "architecture", "entry", "point"],
    "medium": ["optimization", "template", "reference", "protocol"],
    "low": ["plan", "summary", "loading"],
}

# Project-specific ownership mapping
OWNERSHIP_MAP = {
    "streamlit": ["ui", "streamlit", "interface", "app"],
    "inference": ["inference", "api", "model", "prompt"],
    "data": ["data", "analysis", "metrics", "evaluation"],
    "documentation": ["context", "template", "optimization", "handbook"],
    "core": ["architecture", "entry", "point", "quick"],
}

# Project-specific clutter patterns
CLUTTER_PATTERNS = [
    "*.log",  # Log files
    "*.tmp",  # Temporary files
    "*.bak",  # Backup files
    "*.swp",  # Vim swap files
    "*.pyc",  # Python bytecode
    "__pycache__",  # Python cache directories
    ".DS_Store",  # macOS files
    "Thumbs.db",  # Windows files
    "lightning_logs",  # PyTorch Lightning logs
    "wandb",  # Weights & Biases logs
    ".pytest_cache",  # Pytest cache
    ".mypy_cache",  # MyPy cache
    ".ruff_cache",  # Ruff cache
]

# Project-specific gitignore entries
GITIGNORE_ENTRIES = [
    "\n# Korean Grammar Correction Project - Agent Tools",
    "# Logs and temporary files",
    "*.log",
    "*.tmp",
    "*.bak",
    "*.swp",
    "*.pyc",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "\n# IDE and OS files",
    ".DS_Store",
    "Thumbs.db",
    ".vscode/settings.json",
    "\n# ML/AI specific",
    "lightning_logs/",
    "wandb/",
    "outputs/",
    "\n# Agent tools temporary files",
    "tmp/",
    "docs/QUICK_FIXES.md",
]

# Project-specific context bundles
CONTEXT_BUNDLES = {
    "quick-start": {
        "title": "Quick Start Bundle",
        "description": "Essential files for rapid agent onboarding",
        "entries": [
            "quick_context_reference",
            "ai_agent_entry_point",
            "project_overview",
        ],
    },
    "development": {
        "title": "Development Bundle",
        "description": "Core development context for coding tasks",
        "entries": [
            "quick_context_reference",
            "architecture_summary",
            "context_templates",
        ],
    },
    "documentation": {
        "title": "Documentation Bundle",
        "description": "Context for documentation and maintenance tasks",
        "entries": [
            "context_optimization_plan",
            "context_templates",
            "smart_context_loading",
        ],
    },
    "debugging": {
        "title": "Debugging Bundle",
        "description": "Context for troubleshooting and debugging",
        "entries": [
            "quick_context_reference",
            "architecture_summary",
        ],
    },
}

# Project-specific tags
TAG_MAPPINGS = {
    "streamlit": ["ui", "streamlit", "interface", "app"],
    "inference": ["inference", "api", "model", "prompt", "llm"],
    "data": ["data", "analysis", "metrics", "evaluation"],
    "documentation": ["context", "template", "optimization", "handbook"],
    "architecture": ["architecture", "system", "design", "overview"],
    "quick": ["quick", "fast", "rapid", "start"],
    "protocol": ["protocol", "process", "workflow", "procedure"],
}
