# Settings Architecture

## Overview

AgentQMS uses a **single settings directory** for all configuration. The framework ships with default settings, and you can edit them directly to customize behavior.

## Directory Structure

```
workspace_root/
└── .agentqms/                 # AgentQMS directory
    ├── settings/              # All configuration (user-editable)
    │   ├── framework.yaml     # Framework-level settings
    │   ├── interface.yaml     # Agent interface settings
    │   ├── paths.yaml         # Path mappings
    │   ├── tool_mappings.json # Tool path mappings
    │   ├── environments/      # Environment-specific overrides (optional)
    │   └── overrides/         # Additional overrides (optional)
    ├── effective.yaml         # Generated merged config (read-only)
    └── state/                 # Runtime state
```

## Key Principles

- ✅ **Single Location**: All configuration in one `.agentqms/settings/` directory
- ✅ **No Separate Defaults**: Framework ships with defaults in `.agentqms/settings/`, you edit them directly
- ✅ **Simple**: No complex merge logic or multiple directories
- ✅ **Organized**: All AgentQMS files in one place (`.agentqms/`)

## Configuration Precedence

Configuration is merged in this order (later overrides earlier):

1. **Base Settings** (`.agentqms/settings/*.yaml`) - Main configuration files
2. **Environment Overrides** (`.agentqms/settings/environments/*.yaml`) - Environment-specific
3. **Additional Overrides** (`.agentqms/settings/overrides/*.yaml`) - Final overrides
4. **Environment Variables** - Runtime overrides (e.g., `AGENTQMS_PATHS_ARTIFACTS`)
5. **Effective Config** (`.agentqms/effective.yaml`) - Generated merged result (read-only)

## Editing Settings

**Just edit the files in `.agentqms/settings/` directory!** The framework ships with sensible defaults, and you can customize them as needed.

### Example: Customizing Paths

Edit `.agentqms/settings/paths.yaml`:

```yaml
paths:
  artifacts: my_custom_artifacts_dir
  docs: documentation
```

### Example: Changing Framework Name

Edit `.agentqms/settings/framework.yaml`:

```yaml
framework:
  name: "My Custom Framework Name"
  version: "1.0.0"
```

## Migration from Old Structure

The old architecture had:
- `config_defaults/` - Framework defaults
- `config/` - Project overrides
- `settings/` - Unified settings (moved to `.agentqms/settings/`)

All are now in `.agentqms/settings/`. The old directories are no longer used.

## Benefits

- ✅ **Simpler**: One directory, one set of files
- ✅ **Clearer**: No confusion about defaults vs overrides
- ✅ **Easier**: Just edit the files you need
- ✅ **Maintainable**: Less complex merge logic

