#!/usr/bin/env python3
"""
Test script for compliance pipeline
Runs the validation and compliance checks
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🧪 Testing Compliance Pipeline")
print("=" * 60)
print(f"📁 Project root: {project_root}")
print(f"🐍 Python: {sys.version}")
print(f"📦 Python path: {sys.path[:3]}")
print()

# Test 1: Validate all artifacts
print("🔍 Test 1: Running artifact validation...")
print("-" * 60)
try:
    from AgentQMS.agent_tools.compliance.validate_artifacts import main as validate_main
    # Set up args for validation
    sys.argv = ['validate_artifacts.py', '--all']
    validate_main()
    print("✅ Validation completed")
except Exception as e:
    print(f"❌ Validation failed: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 2: Check compliance status
print("📊 Test 2: Checking compliance status...")
print("-" * 60)
try:
    from AgentQMS.agent_tools.compliance.monitor_artifacts import main as monitor_main
    # Set up args for compliance check
    sys.argv = ['monitor_artifacts.py', '--check']
    monitor_main()
    print("✅ Compliance check completed")
except Exception as e:
    print(f"❌ Compliance check failed: {e}")
    import traceback
    traceback.print_exc()
print()

# Check violations history
print("📄 Checking violations history...")
print("-" * 60)
history_file = project_root / "AgentQMS" / "interface" / "artifacts_violations_history.json"
if history_file.exists():
    import json
    with open(history_file) as f:
        history = json.load(f)
    print(f"✅ History file exists: {len(history)} entries")
    if history:
        print(f"   Latest entry: {history[-1].get('timestamp', 'N/A')}")
        print(f"   Compliance rate: {history[-1].get('compliance_rate', 'N/A')}%")
    else:
        print("   History is empty (reset successfully)")
else:
    print("⚠️  History file not found")

print()
print("✅ Pipeline test completed!")
