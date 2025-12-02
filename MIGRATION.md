# AgentQMS Migration Guide

This guide explains how to migrate an existing project to use AgentQMS for quality management and artifact generation.

## Prerequisites

- Python 3.8+
- Existing project to migrate

## Migration Steps

1. **Prepare the source**
   - Ensure AgentQMS is set up with the migration script at `AgentQMS/scripts/migration_package.py`

2. **Run the migration script**
   ```bash
   python AgentQMS/scripts/migration_package.py --source /path/to/agentqms/source --target /path/to/your/project
   ```

3. **Verify setup**
   - Check that `AgentQMS/` and `.agentqms/` directories are copied
   - Run `cd AgentQMS/interface && make status` to verify

4. **Create initial artifacts**
   - The script creates empty artifact directories in `AgentQMS/docs/artifacts/`
   - Move them to your project root: `mv AgentQMS/docs/artifacts docs/`

5. **Start using AgentQMS**
   - Create plans: `cd AgentQMS/interface && make create-plan NAME=my-plan TITLE="My Plan"`
   - Run compliance: `make compliance`

## What Gets Migrated

- AgentQMS framework code
- Configuration files
- Empty artifact structure
- Automation tools

## Troubleshooting

- If paths need adjustment, edit configs in `AgentQMS/interface/config/`
- For bundle-related issues, ensure `.copilot/` is set up
- Run `make validate` to check for issues