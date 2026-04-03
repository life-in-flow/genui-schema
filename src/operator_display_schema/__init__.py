"""operator-display-schema — A2UI component catalog and wire protocol schema.

This package is the single source of truth for what UI components the Operator
can render, their property schemas, and the wire protocol for agent-to-frontend
communication.

Downstream renderers (React web, Swift, Waves) import this package to know
what components exist and what properties they accept.
"""

from .catalog import STANDARD_CATALOG, CatalogEntry, PropertyDef, load_catalog
from .models import BoundValue, Component, Surface, UserAction
from .validation import validate_surface

__all__ = [
    "BoundValue",
    "CatalogEntry",
    "Component",
    "PropertyDef",
    "STANDARD_CATALOG",
    "Surface",
    "UserAction",
    "load_catalog",
    "validate_surface",
]
