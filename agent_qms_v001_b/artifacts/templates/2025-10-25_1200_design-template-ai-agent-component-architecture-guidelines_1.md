---
title: "AI Agent Component Architecture Guidelines"
date: "2025-10-25T12:00:00Z"
type: "template"
category: "architecture"
status: "active"
version: "1.0"
tags: ["ai-agent", "architecture", "streamlit", "component", "guidelines"]
---

# AI Agent Component Architecture Guidelines

## Overview

This document provides specific instructions for AI agents to follow the Strategy Pattern + Composition architecture for Streamlit components from the very beginning. Following these guidelines prevents monolithic code and ensures scalable, maintainable architecture.

## Core Architecture Principles

### 1. Strategy Pattern Implementation
**MANDATORY**: Every component type MUST have its own strategy class.

```python
# ✅ GOOD: One strategy per component type
class TextInputStrategy(BaseRenderStrategy):
    def render(self, component: ComponentSchema, context: RenderContext) -> Any:
        return st.text_input(...)

# ❌ BAD: Multiple component types in one class
class InputRenderer(BaseRenderer):
    def render_text_input(self, component): ...
    def render_text_area(self, component): ...
    def render_number_input(self, component): ...
```

### 2. File Size Limits
**MANDATORY**: Never exceed these limits.

- **Strategy Classes**: 50-80 lines maximum
- **Behavior Classes**: 40-60 lines maximum
- **Base Classes**: 80-120 lines maximum
- **Factory Classes**: 100-150 lines maximum

**If a file exceeds these limits, you MUST split it into smaller files.**

### 3. Single Responsibility Principle
**MANDATORY**: Each class/file must have exactly one reason to change.

- **Strategies**: Handle exactly one component type
- **Behaviors**: Handle exactly one cross-cutting concern
- **Factories**: Handle exactly one type of object creation

## Directory Structure Enforcement

### Required Structure
```
streamlit_app/schema_engine/renderers/
├── strategies/           # ✅ MANDATORY: One strategy per component type
│   ├── base_strategy.py              # Abstract base class
│   ├── text_input_strategy.py        # Text input only
│   ├── text_area_strategy.py         # Text area only
│   ├── number_input_strategy.py      # Number input only
│   └── ...
├── behaviors/           # ✅ MANDATORY: Pluggable behaviors
│   ├── data_binding_behavior.py      # Data resolution only
│   ├── validation_behavior.py        # Validation only
│   ├── error_handling_behavior.py    # Error handling only
│   └── formatting_behavior.py        # Formatting only
├── base_renderer.py     # ✅ MANDATORY: Composition orchestrator
└── component_renderer.py # ✅ MANDATORY: Main renderer
```

### Forbidden Patterns
- ❌ No monolithic renderer files > 400 lines
- ❌ No mixed responsibility classes
- ❌ No direct Streamlit calls in base classes
- ❌ No business logic in UI rendering code

## Implementation Rules

### Strategy Implementation Rules

#### 1. Strategy Interface
**MANDATORY**: All strategies must implement this exact interface:

```python
class BaseRenderStrategy(ABC):
    @abstractmethod
    def can_handle(self, component_type: str) -> bool:
        """Check if this strategy handles the component type."""
        pass

    @abstractmethod
    def render(self, component: ComponentSchema, context: RenderContext) -> Any:
        """Render the component. MAX 20 lines."""
        pass

    @abstractmethod
    def validate_schema(self, component: ComponentSchema) -> List[str]:
        """Validate component schema. MAX 10 lines."""
        pass
```

#### 2. Strategy Size Limits
**MANDATORY**: Each strategy method must be ≤ 20 lines.

```python
# ✅ GOOD: Focused implementation
def render(self, component: ComponentSchema, context: RenderContext) -> Any:
    """Render text input component."""
    label = component.label or "Text Input"
    value = context.get('value', '')
    return st.text_input(label=label, value=value, key=component.key)

# ❌ BAD: Too many responsibilities
def render(self, component: ComponentSchema, context: RenderContext) -> Any:
    # Data binding, validation, formatting, rendering all mixed
    data = self.data_binder.bind(component.data_source, context)
    validated = self.validator.validate(data, component.schema)
    formatted = self.formatter.format(validated, component.format)
    return st.text_input(label=formatted.label, value=formatted.value)
```

### Behavior Implementation Rules

#### 1. Behavior Interface
**MANDATORY**: Behaviors must be small, focused interfaces:

```python
class DataBindingBehavior(Protocol):
    def bind_data(self, component: ComponentSchema, context: dict) -> dict:
        """Bind data sources to component. MAX 15 lines."""
        pass

class ValidationBehavior(Protocol):
    def validate_input(self, value: Any, schema: dict) -> List[str]:
        """Validate input against schema. MAX 10 lines."""
        pass
```

#### 2. Composition in Renderer
**MANDATORY**: Use composition, not inheritance:

```python
# ✅ GOOD: Composition
class ComponentRenderer:
    def __init__(self,
                 data_binder: DataBindingBehavior,
                 validator: ValidationBehavior,
                 strategy_registry: StrategyRegistry):
        self.data_binder = data_binder
        self.validator = validator
        self.strategies = strategy_registry

# ❌ BAD: Inheritance
class ComponentRenderer(BaseRenderer, DataBinderMixin, ValidatorMixin):
    pass
```

## Code Organization Rules

### Import Rules
**MANDATORY**: Follow strict import organization.

```python
# ✅ GOOD: Clear import sections
from __future__ import annotations

# Standard library
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

# Third-party
import streamlit as st

# Local imports
from ..behaviors import DataBindingBehavior
from .base_strategy import BaseRenderStrategy

if TYPE_CHECKING:
    from ..models import ComponentSchema
```

### Method Organization
**MANDATORY**: Methods must be organized by responsibility.

```python
class TextInputStrategy(BaseRenderStrategy):
    # Public interface (alphabetical)
    def can_handle(self, component_type: str) -> bool: ...

    def render(self, component: ComponentSchema, context: RenderContext) -> Any: ...

    def validate_schema(self, component: ComponentSchema) -> List[str]: ...

    # Private helpers (alphabetical)
    def _extract_label(self, component: ComponentSchema) -> str: ...

    def _extract_value(self, context: RenderContext) -> str: ...
```

## Testing Rules

### Test Structure
**MANDATORY**: Tests must mirror the architecture.

```
tests/schema_engine/renderers/
├── strategies/
│   ├── test_text_input_strategy.py      # 20-30 lines
│   ├── test_text_area_strategy.py       # 20-30 lines
│   └── ...
├── behaviors/
│   ├── test_data_binding_behavior.py    # 15-25 lines
│   └── ...
└── integration/
    └── test_component_rendering.py      # End-to-end tests
```

### Test Patterns
**MANDATORY**: Use these testing patterns.

```python
# ✅ GOOD: Focused strategy testing
def test_text_input_renders_correctly():
    """Test text input strategy renders correctly."""
    strategy = TextInputStrategy()
    component = ComponentSchema(type="text_input", label="Test")

    with patch('streamlit.text_input') as mock_input:
        mock_input.return_value = "test value"
        result = strategy.render(component, RenderContext())

        assert result == "test value"
        mock_input.assert_called_once_with(label="Test", value="", key=None)

# ❌ BAD: Monolithic testing
def test_input_renderer_handles_all_types():
    """Test input renderer handles text, number, file inputs."""
    # Tests too many things at once
```

## Error Prevention Rules

### Monolithic Code Detection
**MANDATORY**: If you write code that violates these rules, STOP and refactor immediately.

**Red Flags:**
- File exceeds 100 lines → Split into multiple files
- Class has > 5 methods → Split into multiple classes
- Method exceeds 20 lines → Extract helper methods
- Class handles multiple component types → Create separate strategies

### Architecture Validation
**MANDATORY**: Before committing, validate:

1. **File sizes**: Run `wc -l` on all renderer files
2. **Import structure**: Check imports follow the pattern
3. **Class responsibilities**: Each class should have one reason to change
4. **Test coverage**: Each strategy/behavior must have focused tests

## Implementation Workflow

### When Creating New Components

1. **Identify Component Type**: `text_input`, `selectbox`, etc.
2. **Create Strategy**: `TextInputStrategy` in `strategies/text_input_strategy.py`
3. **Register Strategy**: Add to `StrategyRegistry`
4. **Create Tests**: `test_text_input_strategy.py` (20-30 lines)
5. **Update Documentation**: Add to component registry

### When Modifying Existing Components

1. **Check File Size**: If > 80 lines, split before modifying
2. **Identify Responsibility**: Ensure change affects only one concern
3. **Update Tests**: Modify corresponding test file
4. **Validate Architecture**: Run size checks and import validation

## Migration Prevention

### Never Allow These Patterns
- ❌ Large renderer files (400+ lines)
- ❌ Mixed responsibility classes
- ❌ Direct Streamlit calls in base classes
- ❌ Business logic in UI code
- ❌ Large test files (100+ lines)

### Always Enforce These Patterns
- ✅ One strategy per component type
- ✅ Small, focused behavior classes
- ✅ Composition over inheritance
- ✅ Clear separation of concerns
- ✅ Focused unit tests

## AI Agent Checklist

**Before implementing any component code:**

1. ✅ Have I identified the exact component type?
2. ✅ Have I created a separate strategy class?
3. ✅ Is the strategy file < 80 lines?
4. ✅ Does the strategy implement the exact interface?
5. ✅ Have I created focused unit tests?
6. ✅ Have I validated the file sizes?
7. ✅ Does the code follow composition patterns?

**If any answer is NO, stop and redesign.**

## Examples

### Good Strategy Implementation
```python
class TextInputStrategy(BaseRenderStrategy):
    """Strategy for rendering text input components."""

    def can_handle(self, component_type: str) -> bool:
        return component_type == "text_input"

    def render(self, component: ComponentSchema, context: RenderContext) -> Any:
        label = component.label or "Text Input"
        value = context.get('value', '')
        return st.text_input(label=label, value=value, key=component.key)

    def validate_schema(self, component: ComponentSchema) -> List[str]:
        errors = []
        if not component.label and not component.key:
            errors.append("Text input must have label or key")
        return errors
```

### Bad Implementation (AVOID)
```python
class InputRenderer(BaseRenderer):  # ❌ Too many responsibilities
    def render(self, component):     # ❌ Too many component types
        if component.type == "text_input":
            # 20 lines of text input logic
        elif component.type == "number_input":
            # 20 lines of number input logic
        elif component.type == "file_uploader":
            # 20 lines of file uploader logic
        # ... more types = monolithic class
```

---

*Document Version: 1.0*
*Last Updated: 2025-10-25*
*Purpose: Prevent monolithic architecture by enforcing Strategy Pattern + Composition from day one*
