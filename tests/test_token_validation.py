"""Tests for token validation in validate_surface()."""

from operator_display_schema.models import BoundValue, Component, Surface
from operator_display_schema.validation import validate_surface


def _surface_with_style(style: dict[str, str]) -> Surface:
    """Helper to build a minimal surface with one styled component."""
    return Surface(
        surface_id="test-1",
        components=[
            Component(
                id="root",
                type="Card",
                properties={"title": BoundValue(literal_string="Test")},
                children=[],
                style=style,
            ),
        ],
        root_id="root",
    )


def test_valid_token_passes():
    surface = _surface_with_style({"background": "flow/color/bg/primary"})
    errors = validate_surface(surface)
    assert not errors


def test_multiple_valid_tokens():
    surface = _surface_with_style({
        "background": "flow/color/bg/primary",
        "padding": "flow/spacing/xl",
        "borderRadius": "flow/radius/md",
    })
    errors = validate_surface(surface)
    assert not errors


def test_invalid_token_fails():
    surface = _surface_with_style({"background": "#F7F3EA"})
    errors = validate_surface(surface)
    assert any("flow/" in e and "background" in e for e in errors)


def test_invalid_token_name_fails():
    surface = _surface_with_style({"background": "flow/color/bg/fancy"})
    errors = validate_surface(surface)
    assert any("fancy" in e or "unknown token" in e.lower() for e in errors)


def test_empty_style_passes():
    surface = _surface_with_style({})
    errors = validate_surface(surface)
    assert not errors


def test_compound_token_value_passes():
    surface = _surface_with_style({
        "border": "flow/stroke/sm solid flow/color/stroke/primary",
    })
    errors = validate_surface(surface)
    assert not errors


def test_non_token_literal_fails():
    surface = _surface_with_style({"padding": "16px"})
    errors = validate_surface(surface)
    assert any("padding" in e for e in errors)


def test_transparent_passes():
    surface = _surface_with_style({"background": "transparent"})
    errors = validate_surface(surface)
    assert not errors
