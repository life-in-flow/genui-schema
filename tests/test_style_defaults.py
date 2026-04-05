"""Tests for style_defaults in catalog entries."""

from operator_display_schema import load_catalog


def test_card_has_style_defaults():
    entries = load_catalog()
    card = entries["Card"]
    assert card.style_defaults is not None
    assert "background" in card.style_defaults
    assert card.style_defaults["background"] == "flow/color/bg/primary"


def test_button_has_style_defaults():
    entries = load_catalog()
    button = entries["Button"]
    assert button.style_defaults is not None
    assert "borderRadius" in button.style_defaults


def test_style_defaults_are_optional():
    entries = load_catalog()
    row = entries["Row"]
    assert row.style_defaults is not None
    assert isinstance(row.style_defaults, dict)


def test_style_defaults_use_tokens():
    entries = load_catalog()
    for name, entry in entries.items():
        for key, value in entry.style_defaults.items():
            assert value.startswith("flow/"), (
                f"{name}.style_defaults[{key}] = {value!r} does not start with 'flow/'"
            )
