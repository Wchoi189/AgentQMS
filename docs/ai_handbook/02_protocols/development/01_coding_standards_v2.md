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
- **ALWAYS** use `setup_project_paths()` from `path_utils` for path setup
- **NEVER** manually manipulate `sys.path` (use `setup_project_paths()` instead)
- See: `docs/ai_handbook/03_references/development/path_utils_migration_quickstart.md`

```python
# ✅ CORRECT
from streamlit_app.utils.path_utils import setup_project_paths
setup_project_paths()

# ❌ WRONG
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
