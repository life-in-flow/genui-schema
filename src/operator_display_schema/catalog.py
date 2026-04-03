"""Load the A2UI component catalog from YAML.

Exposes ``STANDARD_CATALOG`` in the same dict format used by the operator
agent-worker for backward compatibility, plus a richer ``load_catalog()``
that returns full ``CatalogEntry`` objects with descriptions and hints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PropertyDef:
    """Definition of a single component property."""

    name: str
    type: str
    required: bool = False
    description: str = ""
    enum: list[str] | None = None


@dataclass(frozen=True)
class CatalogEntry:
    """Rich component definition with metadata and selection hints."""

    type: str
    category: str
    description: str = ""
    best_for: list[str] = field(default_factory=list)
    data_shape: str | None = None
    properties: list[PropertyDef] = field(default_factory=list)

    @property
    def required_properties(self) -> list[str]:
        return [p.name for p in self.properties if p.required]

    def to_legacy_dict(self) -> dict[str, Any]:
        """Convert to the legacy STANDARD_CATALOG format."""
        return {
            "properties": {p.name: p.type for p in self.properties},
            "required": self.required_properties,
        }


_CATALOG_PATH = Path(__file__).parent / "catalog" / "components.yaml"


def _find_catalog_path() -> Path:
    """Locate the catalog YAML, checking both installed and dev layouts."""
    # When installed as a wheel, force-include puts catalog/ inside the package
    pkg_path = Path(__file__).parent / "catalog" / "components.yaml"
    if pkg_path.exists():
        return pkg_path
    # In development, catalog/ is at the repo root
    repo_path = Path(__file__).parent.parent.parent / "catalog" / "components.yaml"
    if repo_path.exists():
        return repo_path
    raise FileNotFoundError(
        "Cannot find catalog/components.yaml. "
        "Ensure the package is installed correctly."
    )


def load_catalog() -> dict[str, CatalogEntry]:
    """Load and parse the full component catalog.

    Returns a dict mapping component type name to ``CatalogEntry``.
    """
    path = _find_catalog_path()
    with open(path) as f:
        raw = yaml.safe_load(f)

    entries: dict[str, CatalogEntry] = {}
    for category in raw.get("categories", []):
        cat_id = category["id"]
        for comp in category.get("components", []):
            props = []
            for pname, pdef in comp.get("properties", {}).items():
                props.append(
                    PropertyDef(
                        name=pname,
                        type=pdef.get("type", "string"),
                        required=pdef.get("required", False),
                        description=pdef.get("description", ""),
                        enum=pdef.get("enum"),
                    )
                )
            entries[comp["type"]] = CatalogEntry(
                type=comp["type"],
                category=cat_id,
                description=comp.get("description", ""),
                best_for=comp.get("best_for", []),
                data_shape=comp.get("data_shape"),
                properties=props,
            )
    return entries


def _build_standard_catalog() -> dict[str, dict[str, Any]]:
    """Build the legacy STANDARD_CATALOG dict from the YAML catalog."""
    entries = load_catalog()
    return {name: entry.to_legacy_dict() for name, entry in entries.items()}


# Legacy-compatible dict: {type_name: {"properties": {...}, "required": [...]}}
STANDARD_CATALOG: dict[str, dict[str, Any]] = _build_standard_catalog()
