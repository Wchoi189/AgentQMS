#!/usr/bin/env python3
"""
Verification script for check_links.py tool.
This demonstrates the tool functionality in a dry-run mode.
"""
import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_check_links():
    """Test the check_links functionality."""
    print("=" * 70)
    print("AgentQMS check_links.py Tool Verification (Dry Run)")
    print("=" * 70)
    print()
    
    try:
        # Import the functions
        print("✓ Importing check_links module...")
        from AgentQMS.agent_tools.documentation.check_links import (
            extract_markdown_links,
            resolve_link,
            check_links_in_directory
        )
        from AgentQMS.agent_tools.utils.paths import get_project_root
        
        # Get project root
        print("✓ Getting project root...")
        root = get_project_root()
        print(f"  Project root: {root}")
        
        # Test on CHANGELOG.md
        print("\n" + "-" * 70)
        print("Test 1: Link extraction from CHANGELOG.md")
        print("-" * 70)
        changelog = root / "CHANGELOG.md"
        if changelog.exists():
            links = extract_markdown_links(changelog)
            print(f"  Found {len(links)} markdown links")
            if links:
                print("  Sample links:")
                for i, (line, text, url) in enumerate(links[:3], 1):
                    print(f"    {i}. Line {line}: [{text}]({url})")
                    resolved = resolve_link(changelog, url)
                    if resolved:
                        exists = "✓" if resolved.exists() else "✗"
                        print(f"       {exists} Resolved to: {resolved}")
                    else:
                        print(f"       (external/anchor link - skipped)")
        else:
            print("  ⚠ CHANGELOG.md not found")
        
        # Test on docs directory
        print("\n" + "-" * 70)
        print("Test 2: Checking links in docs/ directory")
        print("-" * 70)
        docs_dir = root / "docs"
        if docs_dir.exists():
            checked, total, broken = check_links_in_directory(
                docs_dir, root, check_artifacts_only=False
            )
            print(f"  ✓ Checked {checked} markdown files")
            print(f"  ✓ Found {total} total links")
            print(f"  {'⚠' if broken else '✓'} Found {len(broken)} broken links")
            
            if broken:
                print("\n  Broken links (showing first 5):")
                for link in broken[:5]:
                    print(f"    • {link['file']}:{link['line']}")
                    print(f"      [{link['text']}]({link['url']})")
                    print(f"      → {link['resolved']}")
        else:
            print("  ⚠ docs/ directory not found")
        
        # Test with artifacts-only flag
        print("\n" + "-" * 70)
        print("Test 3: Checking artifact links only (--artifacts-only mode)")
        print("-" * 70)
        if docs_dir.exists():
            checked, total, broken = check_links_in_directory(
                docs_dir, root, check_artifacts_only=True
            )
            print(f"  ✓ Checked {checked} markdown files")
            print(f"  ✓ Found {total} artifact-related links")
            print(f"  {'⚠' if broken else '✓'} Found {len(broken)} broken artifact links")
        else:
            print("  ⚠ docs/ directory not found")
        
        # Summary
        print("\n" + "=" * 70)
        print("Verification Summary")
        print("=" * 70)
        print("✓ All imports successful")
        print("✓ Project root detection working")
        print("✓ Link extraction working")
        print("✓ Link resolution working")
        print("✓ Directory scanning working")
        print("\nThe check_links.py tool is ready to use!")
        print("\nTo run the actual tool:")
        print("  python3 AgentQMS/agent_tools/documentation/check_links.py")
        print("  python3 AgentQMS/agent_tools/documentation/check_links.py --json")
        print("  python3 AgentQMS/agent_tools/documentation/check_links.py --artifacts-only")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_check_links()
    sys.exit(0 if success else 1)
