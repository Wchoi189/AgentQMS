#!/usr/bin/env python3
"""
Ultra-concise CLI for AgentQMS tools.

Usage:
    python -m agent_tools.cli discover
    python -m agent_tools.cli create-plan --name my-plan --title "My Plan"
    python -m agent_tools.cli validate
    python -m agent_tools.cli compliance
    python -m agent_tools.cli help

Or install and use as:
    agentqms discover
    agentqms create-plan --name my-plan --title "My Plan"
"""
import sys
from pathlib import Path

# Add agent_tools to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from agent_tools.core.discover import main as discover_main
    from agent_tools.core.artifact_workflow import main as artifact_main
    from agent_tools.compliance.validate_artifacts import main as validate_main
    from agent_tools.compliance.monitor_artifacts import main as compliance_main
    from agent_tools.utilities.agent_feedback import main as feedback_main
    from agent_tools.compliance.documentation_quality_monitor import main as quality_main
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root")
    sys.exit(1)


def show_help():
    """Show available commands."""
    print("AgentQMS - Ultra-Concise CLI")
    print("=" * 40)
    print()
    print("Commands:")
    print("  discover              Show available tools")
    print("  create-plan           Create implementation plan")
    print("  create-assessment     Create assessment")
    print("  validate              Validate artifacts")
    print("  compliance            Check compliance")
    print("  feedback              Agent feedback system")
    print("  quality               Documentation quality monitor")
    print("  help                  Show this help")
    print()
    print("Examples:")
    print("  python -m agent_tools.cli discover")
    print("  python -m agent_tools.cli create-plan --name my-plan --title 'My Plan'")
    print("  python -m agent_tools.cli validate")
    print("  python -m agent_tools.cli feedback")
    print()
    print("Note: Install as 'agentqms' command for even simpler usage")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "help" or command == "--help" or command == "-h":
        show_help()
    elif command == "discover":
        discover_main()
    elif command == "create-plan":
        # Convert to artifact_workflow format
        artifact_args = ["create", "--type", "implementation_plan"] + args
        artifact_main(artifact_args)
    elif command == "create-assessment":
        artifact_args = ["create", "--type", "assessment"] + args
        artifact_main(artifact_args)
    elif command == "validate":
        validate_main(args)
    elif command == "compliance":
        compliance_main(args)
    elif command == "feedback":
        feedback_main()
    elif command == "quality":
        quality_main()
    else:
        print(f"❌ Unknown command: {command}")
        print()
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

