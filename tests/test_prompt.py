"""Tests for the system context prompt builder."""

from genui_graph_schema.prompt import build_system_context


def test_returns_non_empty_string():
    result = build_system_context()
    assert isinstance(result, str)
    assert len(result) > 100


def test_includes_component_types():
    result = build_system_context()
    assert "LineChart" in result
    assert "Card" in result
    assert "DataTable" in result
    assert "Button" in result


def test_includes_token_names():
    result = build_system_context()
    assert "flow/spacing/" in result
    assert "flow/color/bg/" in result
    assert "flow/radius/" in result


def test_includes_composition_rules():
    result = build_system_context()
    assert "spacing" in result.lower()
    assert "hierarchy" in result.lower()


def test_exclude_tokens():
    with_tokens = build_system_context(include_tokens=True)
    without_tokens = build_system_context(include_tokens=False)
    assert len(without_tokens) < len(with_tokens)
    assert "flow/spacing/xs" in with_tokens
    assert "flow/spacing/xs" not in without_tokens


def test_exclude_composition():
    with_comp = build_system_context(include_composition=True)
    without_comp = build_system_context(include_composition=False)
    assert len(without_comp) < len(with_comp)


def test_exclude_catalog():
    with_cat = build_system_context(include_catalog=True)
    without_cat = build_system_context(include_catalog=False)
    assert len(without_cat) < len(with_cat)
    assert "LineChart" not in without_cat


def test_theme_filter():
    result = build_system_context(theme="light")
    assert "moonlight/300" in result
    assert "midnight/950" not in result


def test_includes_style_defaults():
    result = build_system_context()
    assert "flow/color/bg/primary" in result
    assert "flow/radius/sm" in result


def test_includes_guidelines():
    result = build_system_context()
    assert "token" in result.lower()
