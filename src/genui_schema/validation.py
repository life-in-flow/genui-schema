"""Validate A2UI surfaces against the component catalog."""

from __future__ import annotations

from functools import lru_cache

from .catalog import STANDARD_CATALOG
from .models import FollowUpSuggestion, Surface


_ALLOWED_LITERALS = {"transparent", "inherit", "none", "auto"}


@lru_cache(maxsize=1)
def _build_token_registry() -> frozenset[str]:
    """Build a set of all valid flow/ token paths from the design system."""
    from .design import load_design_system

    ds = load_design_system()
    tokens: set[str] = set()

    # Spacing: flow/spacing/{name}
    for name in ds.tokens.spacing:
        tokens.add(f"flow/spacing/{name}")

    # Radius: flow/radius/{name}
    for name in ds.tokens.radius:
        tokens.add(f"flow/radius/{name}")

    # Stroke widths: flow/stroke/{name}
    for name in ds.tokens.stroke:
        tokens.add(f"flow/stroke/{name}")

    # Size: flow/size/{name}
    for name in ds.tokens.size:
        tokens.add(f"flow/size/{name}")

    # Semantic colors: flow/color/{role}/{name}
    for role, entries in ds.tokens.semantic_colors.items():
        for name in entries:
            tokens.add(f"flow/color/{role}/{name}")

    # Palette colors: flow/color/{palette}/{step}
    for palette, steps in ds.tokens.color_palettes.items():
        for step in steps:
            tokens.add(f"flow/color/{palette}/{step}")

    # Typography: flow/font/{style-name}
    for style_name in ds.tokens.typography.get("scale", {}):
        tokens.add(f"flow/font/{style_name}")

    return frozenset(tokens)


def _validate_style_value(comp_id: str, key: str, value: str) -> list[str]:
    """Validate a single style value against the token registry."""
    registry = _build_token_registry()
    errors: list[str] = []

    # Split compound values (e.g., "flow/stroke/sm solid flow/color/stroke/primary")
    parts = value.split()
    flow_refs = [p for p in parts if p.startswith("flow/")]
    non_flow_parts = [p for p in parts if not p.startswith("flow/")]

    if not flow_refs:
        # No flow/ references -- must be an allowed literal
        if value.lower() not in _ALLOWED_LITERALS:
            errors.append(
                f"Component '{comp_id}': style '{key}' = {value!r} "
                f"is not a flow/ token or allowed literal"
            )
    else:
        # Validate each flow/ reference
        for ref in flow_refs:
            if ref not in registry:
                errors.append(
                    f"Component '{comp_id}': style '{key}' references "
                    f"unknown token '{ref}'"
                )

    return errors


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

        # Validate style values against token registry
        for key, value in comp.style.items():
            errors.extend(_validate_style_value(comp.id, key, value))

    return errors


def validate_suggestions(suggestions: list[FollowUpSuggestion]) -> list[str]:
    """Validate a list of follow-up suggestions.

    Returns a list of human-readable error strings. Empty list means valid.
    """
    errors: list[str] = []
    seen_ids: set[str] = set()

    for i, suggestion in enumerate(suggestions):
        if not suggestion.id:
            errors.append(f"Suggestion [{i}]: missing id")
        elif suggestion.id in seen_ids:
            errors.append(f"Suggestion [{i}]: duplicate id '{suggestion.id}'")
        else:
            seen_ids.add(suggestion.id)

        if not suggestion.label:
            errors.append(f"Suggestion [{i}]: missing label")

    return errors
