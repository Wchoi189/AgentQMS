# Coding Standards & Naming Conventions V2

**Document ID**: `PROTO-DEV-001`
**Status**: ACTIVE
**Created**: 2025-10-25
**Last Updated**: 2025-10-25
**Type**: Development Protocol

## Standards

### Code Formatting
- Use Ruff Formatter (line length 88)
- Auto-format: `uv run ruff check . --fix && uv run ruff format .`

### Import Organization
- Three groups: standard library, third-party, local
- One import per line, alphabetical within groups

### Path Management
- **ALWAYS** use framework path utilities for path setup
- **NEVER** manually manipulate `sys.path`
- See: [Import Handling Protocol](23_import_handling_protocol.md) for framework patterns

```python
# ✅ CORRECT - Use framework utilities
from AgentQMS.agent_tools.utils.runtime import ensure_project_root_on_sys_path
ensure_project_root_on_sys_path()

# ❌ WRONG - Manual path manipulation
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
```

### Pydantic V2 Patterns
```python
from pydantic import BaseModel, Field, field_validator, model_validator

class Model(BaseModel):
    field: str = Field(..., constraints...)

    @field_validator('field')
    @classmethod
    def validate_field(cls, v): return v

    @model_validator(mode='after')
    def validate_cross_fields(self): return self
```

### Serialization
- `model.model_dump()` for dict
- `model.model_dump_json()` for JSON
- `ModelClass.model_validate(data)` for dict
- `ModelClass.model_validate_json(json_data)` for JSON

### Naming Conventions
- **Modules/Packages**: snake_case
- **Classes**: PascalCase
- **Functions/Methods**: snake_case
- **Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE

### Validation
```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict .
```
