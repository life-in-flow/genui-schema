"""Validate A2UI surfaces against the component catalog."""

from __future__ import annotations

from .catalog import STANDARD_CATALOG
from .models import Surface


def validate_surface(surface: Surface) -> list[str]:
    """Validate a surface against the standard catalog.

    Returns a list of human-readable error strings. Empty list means valid.
    """
    errors: list[str] = []

    if not surface.surface_id:
        errors.append("Surface missing surface_id")

    if not surface.components:
        errors.append("Surface has no components")
        return errors

    component_ids = {c.id for c in surface.components}

    # Validate root_id
    if surface.root_id and surface.root_id not in component_ids:
        errors.append(f"root_id '{surface.root_id}' not found in components")

    for comp in surface.components:
        if not comp.id:
            errors.append("Component missing id")
            continue

        # Check type is in catalog
        schema = STANDARD_CATALOG.get(comp.type)
        if schema is None:
            errors.append(f"Component '{comp.id}': unknown type '{comp.type}'")
            continue

        # Check required properties
        for req in schema.get("required", []):
            if req not in comp.properties:
                errors.append(
                    f"Component '{comp.id}' ({comp.type}): missing required property '{req}'"
                )

        # Check children reference valid IDs
        for child_id in comp.children:
            if child_id not in component_ids:
                errors.append(
                    f"Component '{comp.id}': child '{child_id}' not found in components"
                )

    return errors
