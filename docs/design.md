# Flowmingo Design System

genui-graph-schema integrates the Flowmingo design system to ensure
agent-generated UI is on-brand and visually consistent with hand-crafted
products.

## Overview

The design system lives in three YAML files under `design/`:

| File | Contents |
|------|----------|
| `tokens.yaml` | Colors, spacing, radius, stroke, typography |
| `composition.yaml` | Container anatomy, spacing rhythm, surface hierarchy, stroke rules |
| `gen-ui.yaml` | Generation principles, constraint layers, guidelines |

## Python API

```python
from genui_graph_schema import (
    load_design_system,   # Returns DesignSystem with tokens, composition, gen_ui
    build_system_context,  # Returns prompt-ready string for LLM system prompts
)
```

### `build_system_context()`

The primary integration point. Returns a structured text string combining
the component catalog, design tokens, and composition rules in a format
optimized for LLM consumption.

```python
context = build_system_context(
    include_tokens=True,       # Include token reference
    include_composition=True,  # Include composition rules
    include_catalog=True,      # Include component catalog
    theme="light",             # Filter to specific theme (optional)
)
# Add to your agent's system prompt
```

### `load_design_system()`

Returns the full DesignSystem for programmatic access:

```python
ds = load_design_system()
ds.tokens.spacing["xl"]["value"]  # 16
ds.tokens.semantic_colors["bg"]["primary"]  # {"light": "moonlight/300", "dark": "midnight/950"}
ds.composition.containers["card"]  # Card container anatomy
ds.gen_ui.principles  # 4 generation principles
```

## Token Reference

### Spacing

| Token | Value | Use |
|-------|-------|-----|
| `flow/spacing/sm` | 4px | Tight element gaps (icon + label) |
| `flow/spacing/md` | 8px | Standard inner padding |
| `flow/spacing/lg` | 12px | List item gaps |
| `flow/spacing/xl` | 16px | Card padding |
| `flow/spacing/3xl` | 24px | Large card padding |
| `flow/spacing/4xl` | 32px | Section gaps |

### Radius

| Token | Value | Use |
|-------|-------|-----|
| `flow/radius/sm` | 4px | Chips, tags, buttons |
| `flow/radius/md` | 8px | Standard inputs |
| `flow/radius/lg` | 12px | Cards |
| `flow/radius/xl` | 16px | Primary cards, modals |
| `flow/radius/full` | 9999px | Pills, avatars |

### Typography

- **Generation 1970 Light** (weight 300) -- headings only
- **Poppins** (weight 500) -- display text and UI emphasis
- **Inter** (weight 400/600) -- titles, body text, data

### Themes

Two themes: light and dark. All semantic tokens resolve per-theme
automatically. Agents reference semantic tokens (e.g., `flow/color/bg/primary`)
and the renderer resolves to the appropriate palette value.

## Composition Rules

### Container Defaults

- **Card**: bg/primary + stroke/sm border + radius/md + spacing/3xl padding
- **SectionContainer**: header (bg/secondary) + content (bg/primary) + stroke border
- **FilterCard**: bg/tertiary default, bg/primary + stroke/accent when selected

### Surface Hierarchy

1. bg/primary (canvas)
2. bg/secondary (headers, elevated)
3. bg/tertiary (nested)
4. bg/quaternary (deep nested)
5. bg/quinary (deepest)

Never skip levels.

### The Stroke Rule

Use strokes for structural containers and data separators.
Use tonal surface shifts for spatial separation between elements.

## Integration

When an agent platform adopts this package:

1. Replace inline A2UI catalog with `from genui_graph_schema import STANDARD_CATALOG`
2. Add `build_system_context()` output to the reasoner system prompt
3. Frontend renderers can consume `design/tokens.yaml` for token resolution
