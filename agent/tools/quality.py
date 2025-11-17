#!/usr/bin/env python3
"""
Agent Quality Monitor (Agent-Only Version)
Checks documentation quality and reports issues
"""

import sys


def agent_quality_check():
    """Agent quality monitoring interface."""
    print("🤖 Agent Quality Monitor (AGENT-ONLY)")
    print("====================================")
    print()
    print("⚠️  WARNING: This tool is for AI agents only!")
    print("   Humans should use the main project tools.")
    print()

    # Setup project paths
    from streamlit_app.utils.path_utils import setup_project_paths

    setup_project_paths()

    # Import and run the main quality tool
    try:
        from scripts.agent_tools.compliance.documentation_quality_monitor import main

        main()
    except ImportError as e:
        print(f"❌ Error importing quality monitor: {e}")
        print("   Make sure you're running from the agent directory")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(agent_quality_check())
