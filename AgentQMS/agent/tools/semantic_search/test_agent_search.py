#!/usr/bin/env python3
"""
Test script for AI Agent Semantic Search Tool
"""

import sys

from AgentQMS.agent_tools.utils.runtime import ensure_project_root_on_sys_path

ensure_project_root_on_sys_path()


def test_import():
    """Test that the module can be imported."""
    try:
        from agent.tools.semantic_search.agent_semantic_search import (
            AgentSemanticSearch,  # noqa: F401
            search_codebase,  # noqa: F401
        )

        print("✅ Import successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_connection():
    """Test Elasticsearch connection."""
    try:
        from agent.tools.semantic_search.agent_semantic_search import (
            AgentSemanticSearch,
        )

        AgentSemanticSearch()
        print("✅ Elasticsearch connection successful")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(
            "   Make sure Elasticsearch is running on http://host.docker.internal:9201 (or set ELASTICSEARCH_URL env var)"
        )
        return False


def test_basic_search():
    """Test basic search functionality."""
    try:
        from agent.tools.semantic_search.agent_semantic_search import search_codebase

        # Test search
        result = search_codebase("semantic search", content_type="code")
        print("✅ Basic search successful")
        print(f"   Result preview: {result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False


def main():
    print("🧪 Testing AI Agent Semantic Search Tool")
    print("=" * 50)

    tests = [
        ("Module Import", test_import),
        ("Elasticsearch Connection", test_connection),
        ("Basic Search", test_basic_search),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1

    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The semantic search tool is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
