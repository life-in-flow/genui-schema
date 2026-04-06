"""Tests for the design system loader."""

from genui_graph_schema.design import load_design_system, DesignSystem


def test_design_system_loads():
    ds = load_design_system()
    assert isinstance(ds, DesignSystem)


def test_spacing_tokens():
    ds = load_design_system()
    assert ds.tokens.spacing["xs"]["value"] == 2
    assert ds.tokens.spacing["sm"]["value"] == 4
    assert ds.tokens.spacing["md"]["value"] == 8
    assert ds.tokens.spacing["lg"]["value"] == 12
    assert ds.tokens.spacing["xl"]["value"] == 16
    assert ds.tokens.spacing["3xl"]["value"] == 24
    assert ds.tokens.spacing["4xl"]["value"] == 32
    assert len(ds.tokens.spacing) == 15


def test_radius_tokens():
    ds = load_design_system()
    assert ds.tokens.radius["sm"]["value"] == 4
    assert ds.tokens.radius["md"]["value"] == 8
    assert ds.tokens.radius["full"]["value"] == 9999
    assert len(ds.tokens.radius) == 7


def test_stroke_tokens():
    ds = load_design_system()
    assert ds.tokens.stroke["sm"]["value"] == 1
    assert ds.tokens.stroke["hairline"]["value"] == 0.5
    assert len(ds.tokens.stroke) == 5


def test_color_palettes():
    ds = load_design_system()
    expected_palettes = {
        "defaults", "heart", "jade", "lavender", "midnight", "moonlight",
        "oceanSwell", "olive", "roots", "rose", "sunlight", "accent",
    }
    assert set(ds.tokens.color_palettes.keys()) == expected_palettes


def test_semantic_colors_have_themes():
    ds = load_design_system()
    bg_primary = ds.tokens.semantic_colors["bg"]["primary"]
    assert "light" in bg_primary
    assert "dark" in bg_primary


def test_chart_colors():
    ds = load_design_system()
    chart = ds.tokens.semantic_colors["chart"]
    assert len(chart) == 10
    assert "a" in chart
    assert "j" in chart


def test_typography_families():
    ds = load_design_system()
    families = ds.tokens.typography["families"]
    assert set(families.keys()) == {"heading", "display", "title", "body"}


def test_typography_scale():
    ds = load_design_system()
    scale = ds.tokens.typography["scale"]
    assert len(scale) == 17
    assert "heading-xl" in scale
    assert "body-sm-semibold" in scale
    assert scale["heading-xl"]["size"] == 32


def test_composition_loads():
    ds = load_design_system()
    assert "card" in ds.composition.containers
    assert len([x for x in ds.composition.surface_hierarchy if isinstance(x, dict) and "level" in x]) == 5
    assert "gap_only" in ds.composition.separation


def test_gen_ui_loads():
    ds = load_design_system()
    assert len(ds.gen_ui.principles) == 4
    assert len(ds.gen_ui.constraint_layers) == 3
    assert ds.gen_ui.themes == ["light", "dark"]
