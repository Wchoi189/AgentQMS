#!/usr/bin/env python3
"""
Validate artifacts workflow - Python version of validate.sh
"""
import sys
from pathlib import Path

# Add agent_tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_tools.compliance.validate_artifacts import main

if __name__ == "__main__":
    main()

