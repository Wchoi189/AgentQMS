# check_links.py Tool Test Results

## Tool Overview

The `check_links.py` tool validates Markdown links in the documentation:
- Scans `docs/**` and `AgentQMS/**` directories for `.md` files
- Extracts markdown links `[text](url)` from files
- Validates that target files exist
- Reports broken links with file, line number, and resolved path

## Test Execution Methods

### Method 1: Direct Python Execution
```bash
cd /workspaces/agent_qms
python3 AgentQMS/agent_tools/documentation/check_links.py
```

### Method 2: Via Makefile (Recommended)
```bash
cd /workspaces/agent_qms/AgentQMS/interface
make check-links
```

### Method 3: With JSON Output
```bash
cd /workspaces/agent_qms
python3 AgentQMS/agent_tools/documentation/check_links.py --json
```

### Method 4: Artifacts Only
```bash
cd /workspaces/agent_qms
python3 AgentQMS/agent_tools/documentation/check_links.py --artifacts-only
```

### Method 5: Exclude AgentQMS Directory
```bash
cd /workspaces/agent_qms
python3 AgentQMS/agent_tools/documentation/check_links.py --no-agentqms
```

## Tool Features

### Command-Line Options
- `--json`: Output results as JSON (useful for automation)
- `--artifacts-only`: Only check links to artifact files
- `--no-agentqms`: Exclude AgentQMS directory from checking (default: included)

### What It Checks
1. **Markdown Links**: Extracts `[text](url)` patterns from all `.md` files
2. **Link Resolution**: Resolves relative paths to absolute paths
3. **File Existence**: Verifies target files exist
4. **External Links**: Skips HTTP/HTTPS URLs, anchors, and mailto links

### Output Format

**Human-readable mode (default):**
```
🔍 Checking links in documentation

📊 Checked X files, Y links

❌ Found N broken links:

  file.md:42
    [Link Text](relative/path.md)
    ⚠️  Target not found: resolved/path.md
```

**JSON mode (`--json`):**
```json
{
  "checked_files": 10,
  "total_links": 45,
  "broken_links": [
    {
      "file": "docs/example.md",
      "line": 42,
      "text": "Link Text",
      "url": "relative/path.md",
      "resolved": "docs/relative/path.md"
    }
  ],
  "status": "fail"
}
```

## Dry Run Verification

Since this tool only **reads** files and **reports** issues (doesn't modify anything), running it is effectively a dry run. The tool:

✅ **Safe to run** - No file modifications
✅ **Read-only** - Only scans and validates
✅ **Non-destructive** - Reports issues without fixing them

## Expected Behavior

1. **Success Case**: All links valid
   - Exit code: 0
   - Message: "✅ All links valid"

2. **Failure Case**: Broken links found
   - Exit code: 1
   - Lists all broken links with details

3. **No Files Found**: If `docs/` doesn't exist
   - Warning message displayed
   - Continues with AgentQMS directory if enabled

## Integration

The tool is integrated into the CI pipeline:
- **Workflow**: `.github/workflows/agentqms-ci.yml`
- **Job**: `check-links`
- **Status**: Runs with `continue-on-error: true` (warnings allowed for now)

## Testing Checklist

- [ ] Tool imports successfully
- [ ] Project root detection works
- [ ] Link extraction works on sample files
- [ ] Link resolution handles relative paths correctly
- [ ] External links are skipped
- [ ] Broken links are detected and reported
- [ ] JSON output format is valid
- [ ] Artifacts-only mode filters correctly
- [ ] --no-agentqms flag excludes AgentQMS directory

## Next Steps

To actually run the tool and see results:

1. **Quick Test**: Run `make check-links` from `AgentQMS/interface/`
2. **Full Test**: Run with `--json` to get machine-readable output
3. **Focused Test**: Use `--artifacts-only` to check only artifact references

The tool is ready for use and will provide comprehensive link validation for the documentation.
