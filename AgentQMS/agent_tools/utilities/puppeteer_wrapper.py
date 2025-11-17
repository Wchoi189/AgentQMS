#!/usr/bin/env python3
"""
Puppeteer Wrapper for AI Agents

This utility allows AI agents to easily use Puppeteer for browser automation.
It handles Node.js version management and provides a simple Python interface.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def get_node_path() -> str | None:
    """Get the path to Node.js using nvm."""
    try:
        # Try to activate nvm and get node path
        result = subprocess.run(
            [
                "bash",
                "-c",
                'export NVM_DIR="$HOME/.nvm" && '
                '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
                "nvm use 20 > /dev/null 2>&1 && which node",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    # Fallback: try system node
    try:
        result = subprocess.run(
            ["which", "node"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return None


def run_puppeteer_script(
    script_path: str,
    *args: str,
    cwd: str | None = None,
    timeout: int = 60,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Run a Puppeteer script using Node.js.

    Args:
        script_path: Path to the Puppeteer JavaScript file
        *args: Additional arguments to pass to the script
        cwd: Working directory for the command
        timeout: Timeout in seconds
        env: Environment variables to set

    Returns:
        Dictionary with 'success', 'stdout', 'stderr', and 'returncode'
    """
    node_path = get_node_path()
    if not node_path:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Node.js not found. Please install Node.js 20+ using nvm.",
            "returncode": 1,
        }

    script_path_obj = Path(script_path)
    if not script_path_obj.exists():
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Script not found: {script_path}",
            "returncode": 1,
        }

    # Build command with nvm activation
    cmd = [
        "bash",
        "-c",
        f'export NVM_DIR="$HOME/.nvm" && '
        f'[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
        f"nvm use 20 > /dev/null 2>&1 && "
        f"{node_path} {script_path} {' '.join(args)}",
    ]

    # Prepare environment
    run_env = None
    if env:
        import os

        run_env = os.environ.copy()
        run_env.update(env)

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or str(script_path_obj.parent),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=run_env,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Script timed out after {timeout} seconds",
            "returncode": 124,
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": 1,
        }


def capture_page(url: str, timeout: int = 30) -> dict[str, Any]:
    """
    Capture a page's content using Puppeteer.

    Args:
        url: URL to capture
        timeout: Timeout in seconds

    Returns:
        Dictionary with page content and status
    """
    script_dir = Path(__file__).parent.parent.parent / "browser-automation"
    script_path = script_dir / "capture_page.js"

    result = run_puppeteer_script(str(script_path), url, timeout=timeout)

    if result["success"]:
        return {
            "success": True,
            "content": result["stdout"],
            "errors": result["stderr"],
        }
    else:
        return {
            "success": False,
            "error": result["stderr"],
            "output": result["stdout"],
        }


def verify_page(url: str, page_name: str = "") -> dict[str, Any]:
    """
    Verify a page for errors using Puppeteer.

    Args:
        url: URL to verify
        page_name: Optional page name for logging

    Returns:
        Dictionary with verification results
    """
    script_dir = Path(__file__).parent.parent.parent / "browser-automation"
    script_path = script_dir / "verify_fixes.js"

    args = [url]
    if page_name:
        args.append(page_name)

    result = run_puppeteer_script(str(script_path), *args, timeout=60)

    return {
        "success": result["success"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "returncode": result["returncode"],
    }


def main():
    """CLI interface for the Puppeteer wrapper."""
    if len(sys.argv) < 2:
        print("Usage: puppeteer_wrapper.py <command> [args...]")
        print("\nCommands:")
        print("  capture <url>           - Capture page content")
        print("  verify <url> [name]     - Verify page for errors")
        print("  run <script> [args...]  - Run a Puppeteer script")
        sys.exit(1)

    command = sys.argv[1]

    if command == "capture":
        if len(sys.argv) < 3:
            print("Error: URL required")
            sys.exit(1)
        result = capture_page(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == "verify":
        if len(sys.argv) < 3:
            print("Error: URL required")
            sys.exit(1)
        page_name = sys.argv[3] if len(sys.argv) > 3 else ""
        result = verify_page(sys.argv[2], page_name)
        print(json.dumps(result, indent=2))

    elif command == "run":
        if len(sys.argv) < 3:
            print("Error: Script path required")
            sys.exit(1)
        script_path = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        result = run_puppeteer_script(script_path, *args)
        print(json.dumps(result, indent=2))

    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)

    sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    main()
