"""Tests for the component catalog loader."""

from genui_graph_schema import STANDARD_CATALOG, load_catalog


def test_catalog_loads():
    """Catalog YAML loads without error."""
    entries = load_catalog()
    assert len(entries) > 0


def test_all_58_components():
    """All 58 component types are present."""
    assert len(STANDARD_CATALOG) == 58


def test_standard_catalog_format():
    """Legacy STANDARD_CATALOG has expected structure."""
    for name, schema in STANDARD_CATALOG.items():
        assert "properties" in schema, f"{name} missing 'properties'"
        assert "required" in schema, f"{name} missing 'required'"
        assert isinstance(schema["properties"], dict)
        assert isinstance(schema["required"], list)


def test_chart_components_have_data():
    """Chart components require data-related properties."""
    charts_needing_data = [
        "LineChart", "AreaChart", "BarChart", "PieChart", "ScatterChart",
        "Histogram", "Heatmap", "TreeMap", "Sunburst", "Funnel",
        "Waterfall", "Candlestick", "BoxPlot", "BubbleChart",
        "ParallelCoordinates",
    ]
    for name in charts_needing_data:
        schema = STANDARD_CATALOG[name]
        assert "data" in schema["required"], f"{name} should require 'data'"


def test_rich_catalog_entries():
    """load_catalog() returns CatalogEntry objects with metadata."""
    entries = load_catalog()
    line_chart = entries["LineChart"]
    assert line_chart.category == "charts"
    assert line_chart.description != ""
    assert len(line_chart.best_for) > 0
    assert line_chart.data_shape is not None


def test_categories_present():
    """All 7 categories are represented."""
    entries = load_catalog()
    categories = {e.category for e in entries.values()}
    expected = {"display", "charts", "maps", "data", "layout", "input", "interactive"}
    assert categories == expected


def test_required_properties_match():
    """CatalogEntry.required_properties matches legacy required list."""
    entries = load_catalog()
    for name, entry in entries.items():
        legacy = STANDARD_CATALOG[name]
        assert sorted(entry.required_properties) == sorted(legacy["required"]), (
            f"{name}: mismatch between rich and legacy required fields"
        )
