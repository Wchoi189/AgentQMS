#!/usr/bin/env python3
"""
Agent Tool Discovery Helper (Agent-Only Version)
Shows available tools and their locations for AI agents
"""

import sys


def show_agent_tools():
    """Show tools available to agents."""
    print("🤖 Agent Tools Discovery (AGENT-ONLY)")
    print("=====================================")
    print()
    print("⚠️  WARNING: These tools are for AI agents only!")
    print("   Humans should use the main project tools.")
    print()

    # Setup project paths
    from streamlit_app.utils.path_utils import setup_project_paths

    setup_project_paths()

    # Import and run the main discovery tool
    try:
        from scripts.agent_tools.core.discover import show_tools

        show_tools()
    except ImportError as e:
        print(f"❌ Error importing discovery tool: {e}")
        print("   Make sure you're running from the agent directory")
        return 1

    print()
    print("💡 Agent Usage:")
    print("   make help          - Show all agent commands")
    print("   make discover      - List all tools")
    print("   make status        - Check system status")
    print("   make validate      - Validate all artifacts")
    print("   make compliance    - Check compliance status")

    return 0


if __name__ == "__main__":
    sys.exit(show_agent_tools())
