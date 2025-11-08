---
title: "Component Creation Template"
date: "2025-10-25T12:00:00Z"
type: "template"
category: "development"
status: "active"
version: "1.0"
tags: ["template", "component", "streamlit", "ai-agent", "development"]
---

# Component Creation Template

## For AI Agents: Creating New Streamlit Components

### Step 1: Identify Component Type
**MANDATORY**: Determine the exact component type (e.g., `text_input`, `selectbox`, `button`)

### Step 2: Create Strategy File
**MANDATORY**: Create `strategies/{component_type}_strategy.py`

```python
"""
{ComponentType} Strategy

Strategy for rendering {component_type} components.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import streamlit as st

from .base_strategy import BaseRenderStrategy

if TYPE_CHECKING:
    from ..models import ComponentSchema
    from .render_context import RenderContext


class {ComponentType}Strategy(BaseRenderStrategy):
    """
    Strategy for rendering {component_type} components.

    This strategy handles the rendering of {component_type} components
    with proper data binding, validation, and error handling.
    """

    def can_handle(self, component_type: str) -> bool:
        """Check if this strategy handles the component type."""
        return component_type == "{component_type}"

    def render(self, component: ComponentSchema, context: RenderContext) -> Any:
        """
        Render {component_type} component.

        Args:
            component: Component schema definition
            context: Render context with data and configuration

        Returns:
            Component render result
        """
        # Extract component properties (MAX 10 lines)
        label = self._extract_label(component)
        value = self._extract_value(component, context)
        key = self._extract_key(component)

        # Render component (MAX 5 lines)
        return st.{streamlit_function}(
            label=label,
            value=value,
            key=key,
            # Add other streamlit parameters
        )

    def validate_schema(self, component: ComponentSchema) -> list[str]:
        """
        Validate component schema.

        Args:
            component: Component schema to validate

        Returns:
            List of validation error messages
        """
        errors = []

        # Add validation logic (MAX 10 lines)
        if not component.label and not component.key:
            errors.append("{ComponentType} must have label or key")

        return errors

    # Private helper methods (alphabetical order)

    def _extract_key(self, component: ComponentSchema) -> str | None:
        """Extract key from component."""
        return getattr(component, 'key', None)

    def _extract_label(self, component: ComponentSchema) -> str:
        """Extract label from component."""
        return getattr(component, 'label', '{Default Label}')

    def _extract_value(self, component: ComponentSchema, context: RenderContext) -> Any:
        """Extract value from component and context."""
        return context.get('value', getattr(component, 'value', {default_value}))
```

### Step 3: Create Test File
**MANDATORY**: Create `tests/schema_engine/renderers/strategies/test_{component_type}_strategy.py`

```python
"""
Tests for {ComponentType}Strategy.
"""

from unittest.mock import patch

import pytest

from streamlit_app.schema_engine.models import ComponentSchema
from streamlit_app.schema_engine.renderers.strategies.{component_type}_strategy import (
    {ComponentType}Strategy,
)
from streamlit_app.schema_engine.renderers.strategies.render_context import RenderContext


class Test{ComponentType}Strategy:
    """Test cases for {ComponentType}Strategy."""

    def test_can_handle_{component_type}(self):
        """Test strategy can handle {component_type}."""
        strategy = {ComponentType}Strategy()
        assert strategy.can_handle("{component_type}")
        assert not strategy.can_handle("other_type")

    def test_render_{component_type}_basic(self):
        """Test basic {component_type} rendering."""
        strategy = {ComponentType}Strategy()
        component = ComponentSchema(
            type="{component_type}",
            label="Test {ComponentType}",
            key="test_key"
        )
        context = RenderContext()

        with patch('streamlit.{streamlit_function}') as mock_func:
            mock_func.return_value = "test_result"
            result = strategy.render(component, context)

            assert result == "test_result"
            mock_func.assert_called_once()

    def test_validate_schema_valid(self):
        """Test schema validation with valid component."""
        strategy = {ComponentType}Strategy()
        component = ComponentSchema(
            type="{component_type}",
            label="Valid Label"
        )

        errors = strategy.validate_schema(component)
        assert errors == []

    def test_validate_schema_missing_label_and_key(self):
        """Test schema validation fails without label or key."""
        strategy = {ComponentType}Strategy()
        component = ComponentSchema(type="{component_type}")

        errors = strategy.validate_schema(component)
        assert len(errors) > 0
        assert "must have label or key" in errors[0].lower()
```

### Step 4: Register Strategy
**MANDATORY**: Add to `StrategyRegistry`

```python
# In strategy_registry.py
from .strategies.{component_type}_strategy import {ComponentType}Strategy

# Add to registry
self._strategies["{component_type}"] = {ComponentType}Strategy()
```

### Step 5: Validate Implementation
**MANDATORY**: Run these checks before committing:

```bash
# Check file sizes
wc -l streamlit_app/schema_engine/renderers/strategies/{component_type}_strategy.py
# Should be ≤ 80 lines

# Run tests
uv run pytest tests/schema_engine/renderers/strategies/test_{component_type}_strategy.py

# Check imports
python -c "import streamlit_app.schema_engine.renderers.strategies.{component_type}_strategy"
```

---

**Template Variables to Replace:**
- `{ComponentType}`: PascalCase (e.g., `TextInput`, `Selectbox`)
- `{component_type}`: snake_case (e.g., `text_input`, `selectbox`)
- `{streamlit_function}`: Streamlit function name (e.g., `text_input`, `selectbox`)
- `{Default Label}`: Default label text
- `{default_value}`: Default value for the component type

**Remember**: If any file exceeds size limits, split it immediately. Never create monolithic code.
