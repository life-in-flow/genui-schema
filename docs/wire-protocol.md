# Wire Protocol Reference

The A2UI wire protocol defines how the agent communicates UI state to the frontend over the LiveKit data channel. All messages are JSON objects with a `type` discriminator.

The canonical source is `schema/wire_protocol.yaml`.

## Core Models

### BoundValue

A value that is either a literal or a JSONPath binding into the data model. Exactly one field should be set.

| Field | Type | Description |
|-------|------|-------------|
| `literalString` | `string?` | Literal string value |
| `literalNumber` | `number?` | Literal numeric value |
| `literalBoolean` | `boolean?` | Literal boolean value |
| `path` | `string?` | JSONPath into data_model (e.g. `"metrics.occupancy"`) |

### Component

A single UI component in the flat adjacency list.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | Yes | Unique component identifier |
| `type` | `string` | Yes | Catalog component type (e.g. `"LineChart"`) |
| `properties` | `Record<string, BoundValue>` | No | Component properties |
| `children` | `string[]` | No | Child component IDs |
| `style` | `Record<string, string>` | No | CSS-like style overrides |

### Surface

The top-level renderable unit. Contains a flat component list and a data model.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `surfaceId` | `string` | Yes | Unique surface identifier |
| `components` | `Component[]` | Yes | Flat adjacency list of components |
| `dataModel` | `object` | Yes | Data for BoundValue path bindings |
| `rootId` | `string` | Yes | ID of the root component |
| `catalog` | `string` | No | Catalog version (default: `"operator-v1"`) |

## Agent-to-Frontend Messages

### `surface_update`

Full surface state. Creates or replaces the surface on the frontend.

```json
{
  "type": "surface_update",
  "surface_id": "abc-123",
  "components": [
    {"id": "root", "type": "Row", "properties": {}, "children": ["kpi-1"]},
    {"id": "kpi-1", "type": "KPI", "properties": {"label": {"literalString": "Occupancy"}, "value": {"path": "occ"}}}
  ],
  "data_model": {"occ": "92%"},
  "root_id": "root",
  "catalog": "operator-v1",
  "ts": 1712179200.0
}
```

Optional fields:
- `slideGroup` — groups surfaces into a slide deck for presentation mode
- `title` — surface title shown in presentation mode

### `data_model_update`

Incremental data update via [RFC 6902 JSON Patch](https://tools.ietf.org/html/rfc6902). Updates displayed data without resending the component tree.

```json
{
  "type": "data_model_update",
  "surface_id": "abc-123",
  "patches": [
    {"op": "replace", "path": "/occ", "value": "93%"}
  ],
  "ts": 1712179260.0
}
```

### `begin_rendering`

Signal to the frontend to start rendering a surface. Sent after `surface_update`.

```json
{
  "type": "begin_rendering",
  "surface_id": "abc-123",
  "root_id": "root",
  "catalog": "operator-v1",
  "ts": 1712179200.1
}
```

### `delete_surface`

Remove a surface from the frontend.

```json
{
  "type": "delete_surface",
  "surface_id": "abc-123",
  "ts": 1712179300.0
}
```

## Frontend-to-Agent Messages

### `user_action`

Sent when the user interacts with a surface component (click, change, submit).

```json
{
  "type": "user_action",
  "surface_id": "abc-123",
  "component_id": "btn-1",
  "action_type": "click",
  "value": {"confirmed": true}
}
```

## Design Principles

1. **Flat adjacency list** — components reference children by ID, not nesting. Enables efficient lookup and update.
2. **BoundValue union** — separates literal values from data bindings. Renderers resolve paths against `dataModel` at render time.
3. **RFC 6902 JSON Patch** — incremental data updates without resending the full surface.
4. **Single tool** — `compose_ui` is the only display tool. It produces `surface_update` + `begin_rendering` messages.
5. **Catalog-driven** — component types are validated against the catalog before sending.
