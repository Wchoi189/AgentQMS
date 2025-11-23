#!/usr/bin/env python3
"""
Compliance check workflow - Python version of compliance.sh
"""
import sys
from pathlib import Path

# Add agent_tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_tools.compliance.monitor_artifacts import main

if __name__ == "__main__":
    main()

