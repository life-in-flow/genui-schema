# genui-schema

The **single source of truth** for the GenUI component catalog, wire protocol, and display tool spec.

This package defines what UI components an agent can render, what properties each component accepts, and how surfaces are communicated between agent and frontend. It replaces the deprecated `tool-graph-display` plugin.

## Who uses this

| Consumer | What they get |
|----------|---------------|
| **Agent worker** (Python) | Pydantic models, `STANDARD_CATALOG`, `validate_surface()` |
| **Frontend** (React/TypeScript) | Wire protocol spec, component type list for renderer registry |
| **Mobile / Waves** (Swift) | Component catalog for building a native renderer |
| **Any new renderer** | Language-neutral YAML schemas for codegen |

## Install

```bash
pip install "genui-schema @ git+https://github.com/life-in-flow/genui-schema.git"
```

## Quick start

```python
from genui_schema import (
    STANDARD_CATALOG,      # Legacy dict: {type: {properties, required}}
    load_catalog,          # Rich catalog: {type: CatalogEntry}
    BoundValue,            # Literal or data-bound value
    Component,             # Single UI component
    Surface,               # Complete renderable surface
    UserAction,            # User interaction event
    validate_surface,      # Validate surface against catalog
)

# Check what components are available
print(len(STANDARD_CATALOG))  # 58

# Get rich metadata
catalog = load_catalog()
line_chart = catalog["LineChart"]
print(line_chart.best_for)      # ["time-series trends", "multi-series comparison"]
print(line_chart.data_shape)    # "array of {x_key: category, y_keys: number[]}"

# Build and validate a surface
surface = Surface(
    surface_id="demo",
    components=[
        Component(id="root", type="KPI", properties={
            "label": BoundValue(literal_string="Occupancy"),
            "value": BoundValue(literal_string="92%"),
        }),
    ],
    root_id="root",
)
errors = validate_surface(surface)
assert errors == []
```

## What's in the box

```
catalog/components.yaml     # 58 component types (language-neutral YAML)
schema/wire_protocol.yaml   # A2UI message types (surface_update, data_model_update, ...)
schema/compose_ui_tool.yaml # The compose_ui tool spec
src/genui_schema/
  models.py                 # BoundValue, Component, Surface, UserAction (Pydantic)
  catalog.py                # YAML loader, STANDARD_CATALOG, CatalogEntry
  validation.py             # validate_surface()
```

## Component categories

| Category | Count | Examples |
|----------|-------|---------|
| Display | 10 | Text, KPI, MetricGroup, Card, Badge |
| Charts | 20 | LineChart, BarChart, PieChart, Heatmap, Sankey |
| Maps | 4 | Choropleth, PointMap, GeoHeatMap, FlowMap |
| Data | 5 | DataTable, PivotTable, KeyValueList, Timeline |
| Layout | 8 | Row, Column, Grid, Tabs, Accordion, Modal |
| Input | 8 | Button, TextField, Select, Slider, Toggle |
| Interactive | 3 | ApprovalCard, ConfirmDialog, ActionMenu |

See [docs/component-reference.md](docs/component-reference.md) for full details.

## Wire protocol

The agent communicates surfaces to the frontend via 4 message types over the LiveKit data channel:

| Message | Direction | Purpose |
|---------|-----------|---------|
| `surface_update` | Agent -> Frontend | Full surface state (create/replace) |
| `data_model_update` | Agent -> Frontend | Incremental data via RFC 6902 JSON Patch |
| `begin_rendering` | Agent -> Frontend | Signal to start rendering |
| `delete_surface` | Agent -> Frontend | Remove a surface |
| `user_action` | Frontend -> Agent | User interaction (click, change, submit) |

See [docs/wire-protocol.md](docs/wire-protocol.md) for full details.

## For renderer implementers

To build a renderer for a new platform:

1. Install this package (or read `catalog/components.yaml` directly)
2. Map each component type to a native widget
3. Implement `BoundValue` resolution: resolve `path` fields against the surface's `dataModel`
4. Handle `surface_update` messages to create/replace surfaces
5. Handle `data_model_update` messages to apply JSON Patches to `dataModel`
6. Send `user_action` messages when the user interacts with input/interactive components

The React web renderer (`apps/web/src/components/a2ui/`) is the reference implementation.
