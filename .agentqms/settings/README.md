# Settings

This directory contains **all configuration** for AgentQMS. The framework ships with default settings, and you can edit these files directly to customize behavior.

## Structure

```
.agentqms/settings/
├── framework.yaml      # Framework-level settings (name, version, validation rules)
├── interface.yaml      # Agent interface settings (tools, workflows, logging)
├── paths.yaml          # Path mappings for project directories
├── tool_mappings.json  # Tool path mappings
├── environments/      # Environment-specific overrides (optional)
│   └── *.yaml
└── overrides/          # Additional overrides (optional)
    └── *.yaml
```

## Configuration Precedence

Configuration is merged in this order (later overrides earlier):

1. **Base Settings** (`.agentqms/settings/*.yaml`) - Main configuration files
2. **Environment Overrides** (`.agentqms/settings/environments/*.yaml`) - Environment-specific
3. **Additional Overrides** (`.agentqms/settings/overrides/*.yaml`) - Final overrides
4. **Environment Variables** - Runtime overrides (e.g., `AGENTQMS_PATHS_ARTIFACTS`)

The final merged configuration is written to `.agentqms/effective.yaml` (read-only, generated).

## Editing Settings

**Just edit the files in this directory!** The framework ships with sensible defaults, and you can customize them as needed.

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

## No Separate Defaults

Unlike the old architecture, there's no separate `config_defaults/` directory. The framework ships with default settings in this directory, and you edit them directly. Much simpler!

## Migration from Old Structure

If you had configuration in:
- `config_defaults/` - These are now in `.agentqms/settings/`
- `config/` - These are now in `.agentqms/settings/`
- `settings/` - These have been moved to `.agentqms/settings/`

The old directories are no longer used.

