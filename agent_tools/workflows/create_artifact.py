#!/usr/bin/env python3
"""
Create artifact workflow - Python version of create-artifact.sh
"""
import sys
from pathlib import Path

# Add agent_tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_tools.core.artifact_workflow import main

if __name__ == "__main__":
    main()

