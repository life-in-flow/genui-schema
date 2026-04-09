"""Tests for surface validation."""

from genui_schema import (
    BoundValue,
    Component,
    FollowUpSuggestion,
    Surface,
    validate_suggestions,
    validate_surface,
)


def test_valid_surface():
    surface = Surface(
        surface_id="s1",
        components=[
            Component(
                id="root",
                type="Row",
                children=["kpi-1"],
            ),
            Component(
                id="kpi-1",
                type="KPI",
                properties={
                    "label": BoundValue(literal_string="Occupancy"),
                    "value": BoundValue(literal_string="92%"),
                },
            ),
        ],
        root_id="root",
    )
    errors = validate_surface(surface)
    assert errors == []


def test_missing_surface_id():
    surface = Surface(
        surface_id="",
        components=[Component(id="root", type="Text", properties={"content": BoundValue(literal_string="hi")})],
        root_id="root",
    )
    errors = validate_surface(surface)
    assert any("missing surface_id" in e for e in errors)


def test_no_components():
    surface = Surface(surface_id="s1")
    errors = validate_surface(surface)
    assert any("no components" in e for e in errors)


def test_unknown_type():
    surface = Surface(
        surface_id="s1",
        components=[Component(id="x", type="FakeWidget")],
        root_id="x",
    )
    errors = validate_surface(surface)
    assert any("unknown type" in e for e in errors)


def test_missing_required_property():
    surface = Surface(
        surface_id="s1",
        components=[Component(id="kpi", type="KPI", properties={})],
        root_id="kpi",
    )
    errors = validate_surface(surface)
    assert any("missing required property 'label'" in e for e in errors)
    assert any("missing required property 'value'" in e for e in errors)


def test_bad_child_reference():
    surface = Surface(
        surface_id="s1",
        components=[
            Component(id="root", type="Row", children=["nonexistent"]),
        ],
        root_id="root",
    )
    errors = validate_surface(surface)
    assert any("'nonexistent' not found" in e for e in errors)


def test_bad_root_id():
    surface = Surface(
        surface_id="s1",
        components=[Component(id="x", type="Text", properties={"content": BoundValue(literal_string="hi")})],
        root_id="missing-root",
    )
    errors = validate_surface(surface)
    assert any("root_id" in e for e in errors)


# ── Follow-up suggestion validation ─────────────────────────────────


def test_valid_suggestions():
    suggestions = [
        FollowUpSuggestion(id="1", label="View Pipeline"),
        FollowUpSuggestion(id="2", label="Schedule Tours", icon="CalendarHeart02"),
    ]
    errors = validate_suggestions(suggestions)
    assert errors == []


def test_empty_suggestions_valid():
    errors = validate_suggestions([])
    assert errors == []


def test_duplicate_suggestion_ids():
    suggestions = [
        FollowUpSuggestion(id="1", label="A"),
        FollowUpSuggestion(id="1", label="B"),
    ]
    errors = validate_suggestions(suggestions)
    assert any("duplicate" in e for e in errors)


def test_suggestion_missing_label():
    suggestions = [FollowUpSuggestion(id="1", label="")]
    errors = validate_suggestions(suggestions)
    assert any("missing label" in e for e in errors)
