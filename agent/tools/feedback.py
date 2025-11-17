#!/usr/bin/env python3
"""
Agent Feedback System (Agent-Only Version)
Allows AI agents to report issues and suggest improvements
"""

import sys


def agent_feedback():
    """Agent feedback interface."""
    print("🤖 Agent Feedback System (AGENT-ONLY)")
    print("======================================")
    print()
    print("⚠️  WARNING: This tool is for AI agents only!")
    print("   Humans should use the main project tools.")
    print()

    # Setup project paths
    from streamlit_app.utils.path_utils import setup_project_paths

    setup_project_paths()

    # Import and run the main feedback tool
    try:
        from scripts.agent_tools.utilities.agent_feedback import main

        main()
    except ImportError as e:
        print(f"❌ Error importing feedback tool: {e}")
        print("   Make sure you're running from the agent directory")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(agent_feedback())
