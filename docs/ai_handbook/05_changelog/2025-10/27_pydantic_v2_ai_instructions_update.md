# Pydantic V2 AI Instructions Update

**Date**: 2025-10-27
**Type**: Documentation Update
**Status**: Completed
**Priority**: High

## Overview

Updated AI instructions and relevant documentation to reflect that this project now uses **Pydantic V2** for all data validation, serialization, and type safety. This ensures AI agents understand the modern data validation patterns and use them consistently.

## Changes Made

### 1. **Main AI Instructions** (`.github/copilot-instructions.md`)

**Updated Architecture Section:**
- Added Pydantic V2 data validation to architecture description
- Updated data validation patterns to show Pydantic V2 syntax
- Marked legacy validators as deprecated

**Key Changes:**
```markdown
## Architecture
- **Dual Components**: Baseline batch processing + Interactive Streamlit app
- **Service Architecture**: `streamlit_app/services/` contains business logic
- **Data Validation**: **Pydantic V2** models in `streamlit_app/models/` for type-safe data validation and serialization
- **Core Files**: `prompts.py`, `metrics.py`, `evaluate.py`
```

**Updated Data Validation Patterns:**
- Replaced legacy validator examples with Pydantic V2 patterns
- Added comprehensive Pydantic V2 usage examples
- Marked old `Validators` class as deprecated

### 2. **AI Handbook Index** (`docs/ai_handbook/index.md`)

**Updated Project Structure:**
- Added Pydantic V2 models to project structure description
- Updated technology stack references

### 3. **Project Overview** (`docs/ai_handbook/01_onboarding/01_project_overview.md`)

**Updated Technology Stack:**
```markdown
### **Core Technologies**
- **Python 3.x**: Primary development language
- **Solar Pro API**: LLM for grammar correction
- **Streamlit**: Web application framework
- **Pydantic V2**: Type-safe data validation and serialization
- **Pandas**: Data processing and analysis
- **Pytest**: Testing framework
```

**Updated Streamlit Application Description:**
- Added Pydantic V2 models location
- Updated status from "Design phase" to "Active development"

### 4. **New Coding Standards** (`docs/ai_handbook/02_protocols/development/01_coding_standards_v2.md`)

**Created comprehensive Pydantic V2 standards:**
- Modern Pydantic V2 syntax patterns
- Field validator patterns with `@field_validator` and `@classmethod`
- Model validator patterns with `@model_validator(mode='after')`
- Serialization patterns with `model_dump()` and `model_validate()`
- Best practices for model design and validation
- Error handling patterns
- Performance optimization guidelines

**Key Patterns Documented:**
```python
# Field Validation
@field_validator('field_name')
@classmethod
def validate_field(cls, v: str) -> str:
    return v

# Model Validation
@model_validator(mode='after')
def validate_model(self) -> 'ModelClass':
    return self

# Serialization
data = model.model_dump()
json_data = model.model_dump_json()
model = ModelClass.model_validate(data)
```

### 5. **Archived Documentation** (`docs/ai_handbook/ARCHIVE/03_references/preprocessing/data-contracts-pydantic-standards.md`)

**Updated to Pydantic V2:**
- Changed title to include "Pydantic V2"
- Updated all code examples to use V2 syntax
- Added warning about V2 syntax requirement
- Updated validator patterns from `@validator` to `@field_validator`

## Impact

### **For AI Agents**
- Clear understanding of Pydantic V2 patterns to use
- Consistent data validation approach across the project
- Modern, type-safe development practices
- Better error handling and validation

### **For Development**
- Standardized data validation patterns
- Improved type safety and IDE support
- Better performance with Pydantic V2's Rust-based validation
- Future-proof codebase using modern patterns

### **For Documentation**
- Single source of truth for Pydantic V2 patterns
- Clear migration path from legacy validators
- Comprehensive examples and best practices
- Consistent documentation across all files

## Files Updated

1. `.github/copilot-instructions.md` - Main AI instructions
2. `docs/ai_handbook/index.md` - AI handbook index
3. `docs/ai_handbook/01_onboarding/01_project_overview.md` - Project overview
4. `docs/ai_handbook/02_protocols/development/01_coding_standards_v2.md` - New coding standards
5. `docs/ai_handbook/ARCHIVE/03_references/preprocessing/data-contracts-pydantic-standards.md` - Archived standards

## Verification

- ✅ All AI instructions updated with Pydantic V2 patterns
- ✅ Documentation consistency maintained
- ✅ Legacy patterns marked as deprecated
- ✅ Modern V2 syntax examples provided
- ✅ Best practices documented
- ✅ Cross-references updated

## Next Steps

1. **AI Agents** should now use Pydantic V2 patterns for all new data validation
2. **Legacy validators** should be gradually replaced with Pydantic V2 models
3. **New features** should follow the documented Pydantic V2 standards
4. **Code reviews** should check for Pydantic V2 compliance

---

**Status**: ✅ **COMPLETED** - All AI instructions and documentation updated to reflect Pydantic V2 usage
