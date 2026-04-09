"""Build prompt-ready system context combining catalog + design system.

The primary integration point for operator's reasoner system prompt.
``build_system_context()`` returns a structured text string the LLM uses
when generating ``compose_ui`` calls.
"""

from __future__ import annotations

from .catalog import load_catalog
from .design import load_design_system


def build_system_context(
    *,
    include_tokens: bool = True,
    include_composition: bool = True,
    include_catalog: bool = True,
    include_suggestions: bool = True,
    theme: str | None = None,
) -> str:
    """Return a prompt-ready string combining catalog + design system.

    Args:
        include_tokens: Include token reference (colors, spacing, typography).
        include_composition: Include composition rules (containers, rhythm).
        include_catalog: Include component catalog with style_defaults.
        include_suggestions: Include follow-up suggestions guidance.
        theme: If set, filter semantic colors to this theme only.
    """
    ds = load_design_system()
    sections: list[str] = []

    # Gen UI Principles (always included)
    sections.append(_build_principles(ds, include_guidelines=include_catalog))

    if include_catalog:
        sections.append(_build_catalog())

    if include_tokens:
        sections.append(_build_tokens(ds, theme=theme))

    if include_composition:
        sections.append(_build_composition(ds))

    if include_suggestions:
        sections.append(_build_suggestions_guidance())

    return "\n\n".join(sections)


def _build_principles(ds, *, include_guidelines: bool = True) -> str:
    lines = ["## Generation Principles"]
    for p in ds.gen_ui.principles:
        lines.append(f"- **{p['name']}**: {p['rule'].strip()}")
    if include_guidelines:
        lines.append("")
        lines.append("## Generation Guidelines")
        for g in ds.gen_ui.guidelines:
            lines.append(f"- {g}")
    return "\n".join(lines)


def _build_catalog() -> str:
    entries = load_catalog()
    lines = ["## Available Components"]

    by_category: dict[str, list] = {}
    for entry in entries.values():
        by_category.setdefault(entry.category, []).append(entry)

    category_order = ["display", "charts", "maps", "data", "layout", "input", "interactive"]
    for cat in category_order:
        cat_entries = by_category.get(cat, [])
        if not cat_entries:
            continue
        lines.append(f"\n### {cat.title()}")
        for e in cat_entries:
            req = ", ".join(f"{p} (required)" for p in e.required_properties)
            opt = ", ".join(
                p.name for p in e.properties if not p.required
            )
            parts = []
            if req:
                parts.append(req)
            if opt:
                parts.append(opt)
            prop_str = "; ".join(parts) if parts else "no properties"
            line = f"- **{e.type}**: {e.description} Props: {prop_str}"
            if e.style_defaults:
                defaults_str = ", ".join(
                    f"{k}={v}" for k, v in e.style_defaults.items()
                )
                line += f"\n  Defaults: {defaults_str}"
            lines.append(line)

    return "\n".join(lines)


def _build_tokens(ds, *, theme: str | None = None) -> str:
    lines = ["## Design Tokens"]

    # Spacing
    lines.append("\n### Spacing (use flow/spacing/{name})")
    parts = []
    for name, info in ds.tokens.spacing.items():
        val = info["value"]
        use = info.get("use", "")
        label = f"flow/spacing/{name}={val}px"
        if use:
            label += f" ({use})"
        parts.append(label)
    lines.append(" | ".join(parts))

    # Radius
    lines.append("\n### Radius (use flow/radius/{name})")
    parts = []
    for name, info in ds.tokens.radius.items():
        val = info["value"]
        use = info.get("use", "")
        label = f"flow/radius/{name}={val}px"
        if use:
            label += f" ({use})"
        parts.append(label)
    lines.append(" | ".join(parts))

    # Stroke
    lines.append("\n### Stroke (use flow/stroke/{name})")
    parts = []
    for name, info in ds.tokens.stroke.items():
        val = info["value"]
        parts.append(f"flow/stroke/{name}={val}px")
    lines.append(" | ".join(parts))

    # Semantic colors
    lines.append("\n### Colors")
    for role, tokens in ds.tokens.semantic_colors.items():
        if role == "utility":
            continue
        names = []
        for name, theme_vals in tokens.items():
            if theme and isinstance(theme_vals, dict):
                resolved = theme_vals.get(theme, "")
                names.append(f"{name} ({resolved})")
            else:
                names.append(name)
        lines.append(f"**{role}**: {', '.join(names)}")

    # Chart colors
    lines.append("\n### Chart Colors (sequential assignment)")
    chart = ds.tokens.semantic_colors.get("chart", {})
    parts = []
    for slot, theme_vals in chart.items():
        if theme and isinstance(theme_vals, dict):
            parts.append(f"chart/{slot} ({theme_vals.get(theme, '')})")
        else:
            parts.append(f"chart/{slot}")
    lines.append(" | ".join(parts))

    # Typography
    lines.append("\n### Typography")
    families = ds.tokens.typography["families"]
    for fam_id, fam in families.items():
        lines.append(f"- **{fam_id}**: {fam['name']} (weight {fam['weight']}) -- {fam['role']}")
    lines.append("\nType scale:")
    for style_name, style in ds.tokens.typography["scale"].items():
        fam = style["family"]
        size = style["size"]
        lines.append(f"- {style_name}: {fam}, {size}px")

    return "\n".join(lines)


def _build_suggestions_guidance() -> str:
    lines = ["## Follow-Up Suggestions"]
    lines.append(
        "You can include `suggestions` in your compose_ui call to offer "
        "follow-up actions the user can take. These render as action buttons "
        "below the conversation."
    )
    lines.append("")
    lines.append("Guidelines:")
    lines.append("- Offer 2-4 suggestions that naturally follow from the current response")
    lines.append("- Labels should be concise action phrases (e.g. 'View Leasing Pipeline')")
    lines.append("- Use `prompt` when the message to send differs from the display label")
    lines.append("- Icons are optional; use Flowmingo icon names (e.g. 'Key01', 'CalendarHeart02')")
    lines.append("- Suggestions replace previous ones -- each response sets a fresh list")
    lines.append("- Omit suggestions when no natural follow-ups exist")
    return "\n".join(lines)


def _build_composition(ds) -> str:
    lines = ["## Composition Rules"]

    # Container defaults
    lines.append("\n### Container Defaults")
    for name, spec in ds.composition.containers.items():
        desc = spec.get("description", name)
        details = []
        for key in ("background", "border", "borderRadius", "padding", "childGap"):
            if key in spec:
                details.append(f"{key}={spec[key]}")
        if details:
            lines.append(f"- **{name}**: {desc}. {', '.join(details)}")
        else:
            lines.append(f"- **{name}**: {desc}")

    # Spacing rhythm
    lines.append("\n### Spacing Rhythm")
    for name, info in ds.composition.spacing_rhythm.items():
        token = info["token"]
        use = info.get("use", name)
        lines.append(f"- {use}: {token}")

    # Surface hierarchy
    lines.append("\n### Surface Hierarchy")
    for level in ds.composition.surface_hierarchy:
        if isinstance(level, dict) and "level" in level:
            lines.append(f"- Level {level['level']}: {level['token']} -- {level['use']}")

    rule = ds.composition.surface_hierarchy
    for item in rule:
        if isinstance(item, dict) and "rule" in item:
            lines.append(f"\nRule: {item['rule']}")

    # Stroke rules
    lines.append("\n### Stroke Rules")
    lines.append(ds.composition.stroke_rules.get("rule", ""))
    lines.append("Use strokes for: " + ", ".join(ds.composition.stroke_rules.get("use_strokes_for", [])))
    lines.append("Do not use strokes for: " + ", ".join(ds.composition.stroke_rules.get("do_not_use_strokes_for", [])))

    # Button rules
    lines.append("\n### Button Variants")
    for variant, desc in ds.composition.buttons.get("variants", {}).items():
        lines.append(f"- **{variant}**: {desc}")

    return "\n".join(lines)
