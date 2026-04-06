"""Tests for Pydantic models."""

from genui_schema import BoundValue, Component, Surface, UserAction


def test_bound_value_literal_string():
    bv = BoundValue(literal_string="hello")
    assert bv.literal_value() == "hello"
    assert not bv.is_bound()


def test_bound_value_literal_number():
    bv = BoundValue(literal_number=42.0)
    assert bv.literal_value() == 42.0
    assert not bv.is_bound()


def test_bound_value_literal_boolean():
    bv = BoundValue(literal_boolean=True)
    assert bv.literal_value() is True
    assert not bv.is_bound()


def test_bound_value_path():
    bv = BoundValue(path="metrics.occupancy")
    assert bv.is_bound()
    assert bv.literal_value() is None


def test_bound_value_camel_case_serialization():
    bv = BoundValue(literal_string="hello")
    data = bv.model_dump(by_alias=True, exclude_none=True)
    assert "literalString" in data
    assert "literal_string" not in data


def test_component_basic():
    comp = Component(
        id="kpi-1",
        type="KPI",
        properties={
            "label": BoundValue(literal_string="Occupancy"),
            "value": BoundValue(path="metrics.occ"),
        },
    )
    assert comp.id == "kpi-1"
    assert comp.type == "KPI"
    assert comp.properties["label"].literal_value() == "Occupancy"
    assert comp.properties["value"].is_bound()


def test_component_defaults():
    comp = Component(id="x", type="Text")
    assert comp.properties == {}
    assert comp.children == []
    assert comp.style == {}


def test_surface_get_component():
    comp = Component(id="root", type="Row")
    surface = Surface(
        surface_id="s1",
        components=[comp],
        root_id="root",
    )
    assert surface.get_component("root") is comp
    assert surface.get_component("missing") is None


def test_surface_defaults():
    surface = Surface(surface_id="s1")
    assert surface.components == []
    assert surface.data_model == {}
    assert surface.root_id == ""
    assert surface.catalog == "operator-v1"


def test_user_action():
    action = UserAction(
        surface_id="s1",
        component_id="btn-1",
        action="click",
        value={"confirmed": True},
    )
    assert action.surface_id == "s1"
    assert action.action == "click"
    assert action.value == {"confirmed": True}
