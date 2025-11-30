#!/usr/bin/env python3
"""Direct test of check_links functions."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing check_links.py functions directly...")
print("=" * 60)

try:
    # Test importing the module
    print("\n1. Testing imports...")
    from AgentQMS.agent_tools.documentation.check_links import (
        extract_markdown_links,
        resolve_link,
        check_links_in_directory
    )
    from AgentQMS.agent_tools.utils.paths import get_project_root
    print("   ✓ Imports successful")
    
    # Test getting project root
    print("\n2. Testing project root detection...")
    root = get_project_root()
    print(f"   ✓ Project root: {root}")
    
    # Test extracting links from a sample file
    print("\n3. Testing link extraction...")
    changelog = project_root / "CHANGELOG.md"
    if changelog.exists():
        links = extract_markdown_links(changelog)
        print(f"   ✓ Found {len(links)} links in CHANGELOG.md")
        if links:
            print(f"   Sample link: {links[0]}")
    else:
        print("   ⚠ CHANGELOG.md not found")
    
    # Test checking a small directory
    print("\n4. Testing directory link checking (docs only)...")
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        checked, total, broken = check_links_in_directory(
            docs_dir, 
            project_root,
            check_artifacts_only=False
        )
        print(f"   ✓ Checked {checked} files")
        print(f"   ✓ Found {total} total links")
        print(f"   {'⚠' if broken else '✓'} Found {len(broken)} broken links")
        if broken and len(broken) <= 5:
            for link in broken:
                print(f"      - {link['file']}:{link['line']} -> {link['url']}")
        elif broken:
            print(f"      (showing first 5 of {len(broken)} broken links)")
            for link in broken[:5]:
                print(f"      - {link['file']}:{link['line']} -> {link['url']}")
    else:
        print("   ⚠ docs/ directory not found")
    
    print("\n" + "=" * 60)
    print("Direct function test completed successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
