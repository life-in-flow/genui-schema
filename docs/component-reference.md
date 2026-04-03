# Component Reference

The A2UI component catalog defines all renderable components available to the Operator agent. Each component has a type name, category, properties, and selection hints.

The canonical source is `catalog/components.yaml`. This document provides a human-readable reference.

## How Components Work

The agent uses `compose_ui` to declare a nested component tree:

```json
{
  "type": "Row",
  "props": { "gap": "md" },
  "children": [
    { "type": "KPI", "props": { "label": "Occupancy", "value": "92%", "status": "good" } },
    { "type": "LineChart", "props": { "title": "Trend", "data": {"path": "occ_data"}, "x_key": "month", "y_keys": ["rate"] } }
  ]
}
```

The tree is flattened to a flat adjacency list (each component has an `id` and `children` list of IDs) and sent over the wire as a `surface_update` message.

Properties can be **literal values** or **data bindings** (`{"path": "key"}`) resolved against the Surface's `data_model` at render time.

## Categories

### Display (10 components)

Simple visual elements for text, metrics, and cards.

| Type | Required Props | Best For |
|------|---------------|----------|
| **Text** | `content` | Simple text output, labels |
| **KPI** | `label`, `value` | Single headline metric, status indicators |
| **MetricGroup** | `metrics` | At-a-glance overviews, related metrics |
| **Scorecard** | `title`, `value` | Goal tracking, target comparison |
| **ProgressBar** | `label`, `value` | Completion tracking, capacity utilization |
| **StatCard** | `label`, `value` | Dashboard stat tiles, change indicators |
| **Card** | `title` | Grouping related info, detail panels |
| **Image** | `src` | Photos, diagrams, logos |
| **Markdown** | `content` | Rich text, formatted explanations |
| **Badge** | `label` | Status tags, category labels |

### Charts (20 components)

Data visualization components. All chart types accept a `title` property and require data-related properties.

| Type | Required Props | Best For |
|------|---------------|----------|
| **LineChart** | `data`, `x_key`, `y_keys` | Time-series trends, multi-series comparison |
| **AreaChart** | `data`, `x_key`, `y_keys` | Cumulative metrics, volume over time |
| **BarChart** | `data`, `x_key`, `y_keys` | Category comparison, rankings |
| **PieChart** | `data`, `name_key`, `value_key` | Proportional breakdown, composition |
| **ComboChart** | `data`, `x_key` | Actual vs budget, magnitude + rate |
| **Histogram** | `data`, `value_key` | Distribution analysis, spread |
| **ScatterChart** | `data`, `x_key`, `y_key` | Correlation, outlier detection |
| **GraphChart** | `nodes`, `edges` | Entity relationships, dependency graphs |
| **Heatmap** | `data`, `x_key`, `y_key`, `value_key` | Time-of-day patterns, cross-tabulation |
| **TreeMap** | `data`, `name_key`, `value_key` | Space allocation, hierarchical composition |
| **Sunburst** | `data`, `name_key`, `value_key` | Hierarchical drill-down |
| **Sankey** | `nodes`, `links` | Flow analysis, pipeline stages |
| **Funnel** | `data`, `name_key`, `value_key` | Conversion funnels, pipeline attrition |
| **Radar** | `indicators`, `series` | Multi-attribute comparison |
| **Waterfall** | `data`, `name_key`, `value_key` | Financial bridges, P&L breakdown |
| **Candlestick** | `data`, `date_key`, `open_key`, `close_key`, `high_key`, `low_key` | Financial OHLC |
| **BoxPlot** | `data`, `value_key` | Distribution comparison, outliers |
| **GaugeChart** | `value` | Single metric against target |
| **BubbleChart** | `data`, `x_key`, `y_key`, `size_key` | Three-variable comparison |
| **ParallelCoordinates** | `data`, `dimensions` | High-dimensional filtering |

### Maps (4 components)

| Type | Required Props | Best For |
|------|---------------|----------|
| **Choropleth** | `data`, `region_key`, `value_key` | Regional comparison |
| **PointMap** | `data`, `lat_key`, `lng_key` | Location plotting |
| **GeoHeatMap** | `data`, `lat_key`, `lng_key` | Density, activity hotspots |
| **FlowMap** | `flows`, `origin_key`, `dest_key` | Migration, logistics flows |

### Data (5 components)

| Type | Required Props | Best For |
|------|---------------|----------|
| **DataTable** | `columns`, `rows` | Structured data, detailed records |
| **PivotTable** | `data`, `rows`, `values` | Cross-tabulation, aggregation |
| **KeyValueList** | `items` | Property details, metadata |
| **Timeline** | `events` | Event sequences, activity logs |
| **TreeList** | `data`, `label_key` | Hierarchical data, nested categories |

### Layout (8 components)

Container components for arranging children.

| Type | Required Props | Best For |
|------|---------------|----------|
| **Row** | *(none)* | Horizontal grouping |
| **Column** | *(none)* | Vertical stacking |
| **Grid** | *(none)* | Dashboard grids |
| **Stack** | *(none)* | Flexible direction |
| **Divider** | *(none)* | Section separation |
| **Tabs** | `labels` | Multi-view content |
| **Accordion** | `title` | Progressive disclosure |
| **Modal** | `title` | Confirmations, detail views |

### Input (8 components)

Interactive form elements. These trigger `user_action` messages when the user interacts.

| Type | Required Props | Best For |
|------|---------------|----------|
| **Button** | `label` | Actions, confirmations |
| **TextField** | `label` | Text entry, search |
| **Select** | `label`, `options` | Dropdown selection |
| **DatePicker** | `label` | Date selection |
| **Slider** | `label`, `min`, `max` | Numeric range |
| **Toggle** | `label` | Boolean settings |
| **MultipleChoice** | `label`, `options` | Multi-select |
| **FilterBar** | `filters` | Data filtering |

### Interactive (3 components)

Workflow components that combine display and action.

| Type | Required Props | Best For |
|------|---------------|----------|
| **ApprovalCard** | `title`, `description` | Approval workflows |
| **ConfirmDialog** | `title`, `message` | Destructive action confirmation |
| **ActionMenu** | `items` | Contextual actions |
