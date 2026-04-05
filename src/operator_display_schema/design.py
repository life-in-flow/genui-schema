"""Load the Flowmingo design system from YAML files.

Provides ``load_design_system()`` which returns a ``DesignSystem`` instance
combining tokens, composition rules, and gen-ui constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class TokenSet:
    """Complete Flowmingo token inventory."""

    size: dict[str, float]
    spacing: dict[str, dict[str, Any]]
    radius: dict[str, dict[str, Any]]
    stroke: dict[str, dict[str, Any]]
    color_palettes: dict[str, dict[str, str]]
    semantic_colors: dict[str, dict[str, Any]]
    typography: dict[str, Any]


@dataclass(frozen=True)
class Composition:
    """Composition rules for how agents compose UI."""

    containers: dict[str, Any]
    spacing_rhythm: dict[str, Any]
    surface_hierarchy: list[Any]
    separation: dict[str, Any]
    stroke_rules: dict[str, Any]
    typography_roles: dict[str, Any]
    buttons: dict[str, Any]
    charts: dict[str, Any]
    interactive_states: dict[str, Any]
    table: dict[str, Any]


@dataclass(frozen=True)
class GenUIConstraints:
    """LLM-facing generation principles and constraints."""

    principles: list[dict[str, str]]
    constraint_layers: list[dict[str, str]]
    themes: list[str]
    guidelines: list[str]


@dataclass(frozen=True)
class DesignSystem:
    """Complete Flowmingo design system."""

    tokens: TokenSet
    composition: Composition
    gen_ui: GenUIConstraints


def _find_design_path(filename: str) -> Path:
    """Locate a design YAML file, checking installed and dev layouts."""
    pkg_path = Path(__file__).parent / "design" / filename
    if pkg_path.exists():
        return pkg_path
    repo_path = Path(__file__).parent.parent.parent / "design" / filename
    if repo_path.exists():
        return repo_path
    raise FileNotFoundError(
        f"Cannot find design/{filename}. "
        "Ensure the package is installed correctly."
    )


def _load_yaml(filename: str) -> dict[str, Any]:
    path = _find_design_path(filename)
    with open(path) as f:
        return yaml.safe_load(f)


def load_design_system() -> DesignSystem:
    """Load all design YAML files into a DesignSystem instance."""
    tokens_raw = _load_yaml("tokens.yaml")
    comp_raw = _load_yaml("composition.yaml")
    genui_raw = _load_yaml("gen-ui.yaml")

    tokens = TokenSet(
        size=tokens_raw["size"],
        spacing=tokens_raw["spacing"],
        radius=tokens_raw["radius"],
        stroke=tokens_raw["stroke"],
        color_palettes=tokens_raw["color_palettes"],
        semantic_colors=tokens_raw["semantic_colors"],
        typography=tokens_raw["typography"],
    )

    composition = Composition(
        containers=comp_raw["containers"],
        spacing_rhythm=comp_raw["spacing_rhythm"],
        surface_hierarchy=comp_raw["surface_hierarchy"],
        separation=comp_raw["separation"],
        stroke_rules=comp_raw["stroke_rules"],
        typography_roles=comp_raw["typography_roles"],
        buttons=comp_raw["buttons"],
        charts=comp_raw["charts"],
        interactive_states=comp_raw["interactive_states"],
        table=comp_raw["table"],
    )

    gen_ui = GenUIConstraints(
        principles=genui_raw["principles"],
        constraint_layers=genui_raw["constraint_layers"],
        themes=genui_raw["themes"]["supported"],
        guidelines=genui_raw["guidelines"],
    )

    return DesignSystem(tokens=tokens, composition=composition, gen_ui=gen_ui)
