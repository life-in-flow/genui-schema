"""genui-schema -- declarative component catalog and wire protocol for agent-driven UI.

This package is the single source of truth for what UI components an agent
can render, their property schemas, and the wire protocol for agent-to-frontend
communication.

Downstream renderers (React web, Swift, Waves) import this package to know
what components exist and what properties they accept.
"""

from .catalog import STANDARD_CATALOG, CatalogEntry, PropertyDef, load_catalog
from .design import DesignSystem, load_design_system
from .models import BoundValue, Component, FollowUpSuggestion, Surface, UserAction
from .prompt import build_system_context
from .validation import validate_suggestions, validate_surface

__all__ = [
    "BoundValue",
    "CatalogEntry",
    "Component",
    "DesignSystem",
    "FollowUpSuggestion",
    "PropertyDef",
    "STANDARD_CATALOG",
    "Surface",
    "UserAction",
    "build_system_context",
    "load_catalog",
    "load_design_system",
    "validate_suggestions",
    "validate_surface",
]
