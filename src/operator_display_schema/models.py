"""Pydantic models for the A2UI declarative component protocol.

Components are stored as a flat adjacency list (each Component has children IDs).
BoundValue supports both literal values and JSONPath data bindings so the
frontend can reactively update when the data model changes.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BoundValue(BaseModel):
    """A value that is either a literal or a JSONPath binding into the data model.

    Exactly one of (literal_string, literal_number, literal_boolean) or path
    should be set. If path is set, the frontend resolves it against the
    Surface's data_model at render time.

    Serializes to camelCase (literalString, literalNumber, etc.) to match
    the frontend TypeScript interface. Null fields are excluded.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda s: "".join(
            word.capitalize() if i else word
            for i, word in enumerate(s.split("_"))
        ),
    )

    literal_string: str | None = None
    literal_number: float | None = None
    literal_boolean: bool | None = None
    path: str | None = None  # JSONPath, e.g. "metrics.occupancy"

    def is_bound(self) -> bool:
        """True if this value is a data-bound path rather than a literal."""
        return self.path is not None

    def literal_value(self) -> str | float | bool | None:
        """Return the literal value, or None if data-bound."""
        if self.literal_string is not None:
            return self.literal_string
        if self.literal_number is not None:
            return self.literal_number
        if self.literal_boolean is not None:
            return self.literal_boolean
        return None


class Component(BaseModel):
    """A single UI component in the flat adjacency list.

    The ``type`` field maps to a catalog entry (e.g. "Text", "LineChart",
    "Button"). Properties are typed as BoundValue so they can be either
    literal or data-bound. Children are referenced by ID.
    """

    id: str
    type: str
    properties: dict[str, BoundValue] = Field(default_factory=dict)
    children: list[str] = Field(default_factory=list)
    style: dict[str, str] = Field(default_factory=dict)


class Surface(BaseModel):
    """A complete renderable surface — the top-level A2UI unit.

    Contains a flat list of components (adjacency list), a data model for
    bindings, and a root component ID. The catalog field tells the frontend
    which component set to use for rendering.
    """

    surface_id: str
    components: list[Component] = Field(default_factory=list)
    data_model: dict[str, Any] = Field(default_factory=dict)
    root_id: str = ""
    catalog: str = "operator-v1"

    def get_component(self, component_id: str) -> Component | None:
        """Look up a component by ID."""
        for c in self.components:
            if c.id == component_id:
                return c
        return None


class UserAction(BaseModel):
    """An action triggered by user interaction with a surface component."""

    surface_id: str
    component_id: str
    action: str  # "click", "change", "submit"
    value: Any = None
