#!/bin/bash
# Test script for compliance pipeline
# This script tests the entire compliance validation pipeline

set -e  # Exit on error

echo "🧪 Testing Compliance Pipeline"
echo "=============================="
echo ""

# Set up environment
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd):$PYTHONPATH"

echo "📁 Current directory: $(pwd)"
echo "🐍 Python path: $PYTHONPATH"
echo ""

# Test 1: Validate all artifacts
echo "🔍 Test 1: Running artifact validation..."
echo "----------------------------------------"
cd AgentQMS/interface
python ../agent_tools/compliance/validate_artifacts.py --all
VALIDATE_EXIT=$?
echo ""

# Test 2: Check compliance status
echo "📊 Test 2: Checking compliance status..."
echo "----------------------------------------"
python ../agent_tools/compliance/monitor_artifacts.py --check
COMPLIANCE_EXIT=$?
echo ""

# Test 3: Run workflow validation
echo "🔄 Test 3: Running workflow validation..."
echo "----------------------------------------"
cd /workspaces/agent_qms/AgentQMS/interface
make workflow-validate || true
WORKFLOW_EXIT=$?
echo ""

# Summary
echo "📋 Test Summary"
echo "==============="
echo "Validation: $([ $VALIDATE_EXIT -eq 0 ] && echo '✅ PASSED' || echo '❌ FAILED')"
echo "Compliance: $([ $COMPLIANCE_EXIT -eq 0 ] && echo '✅ PASSED' || echo '❌ FAILED')"
echo "Workflow:   $([ $WORKFLOW_EXIT -eq 0 ] && echo '✅ PASSED' || echo '❌ FAILED')"
echo ""

# Check violations history
if [ -f "artifacts_violations_history.json" ]; then
    echo "📄 Violations history file exists"
    HISTORY_SIZE=$(wc -l < artifacts_violations_history.json)
    echo "   History entries: $HISTORY_SIZE lines"
else
    echo "⚠️  Violations history file not found"
fi

echo ""
echo "✅ Pipeline test completed!"
