from __future__ import annotations

from build.colors import to_rgb
from build.tokens import Tokens

SCHEME_NAME = "UI Kit Graphite"

# Shared by Colors:Window and Colors:Complementary.
WINDOW = {
    "BackgroundNormal": "surface.panel",
    "BackgroundAlternate": "surface.raised",
    "ForegroundNormal": "text.primary",
    "ForegroundInactive": "text.secondary",
    "ForegroundActive": "text.strong",
    "ForegroundLink": "accent.hover",
    "ForegroundVisited": "text.secondary",
    "ForegroundNegative": "status.danger",
    "ForegroundNeutral": "status.warning",
    "ForegroundPositive": "status.success",
    "DecorationFocus": "accent.base",
    "DecorationHover": "accent.hover",
}

# Section -> {key: role}.
SECTIONS = {
    "Colors:Window": WINDOW,
    "Colors:Complementary": WINDOW,
    "Colors:Button": {
        **WINDOW,
        "BackgroundNormal": "surface.control",
        "BackgroundAlternate": "surface.raised",
    },
    "Colors:View": {
        **WINDOW,
        "BackgroundNormal": "surface.background",
        "BackgroundAlternate": "surface.panel",
    },
    "Colors:Tooltip": {
        **WINDOW,
        "BackgroundNormal": "surface.raised",
        "BackgroundAlternate": "surface.control",
    },
    "Colors:Selection": {
        **WINDOW,
        # Krita paints sliders, selected layers, and brush presets with this color,
        # so it uses the muted accent. The bright accent stays on focus rings.
        "BackgroundNormal": "accent.muted",
        "BackgroundAlternate": "accent.pressed",
        "ForegroundNormal": "text.strong",
        "ForegroundActive": "text.strong",
        "ForegroundInactive": "text.strong",
        "ForegroundLink": "text.strong",
        "ForegroundVisited": "text.strong",
        "DecorationFocus": "accent.hover",
        "DecorationHover": "accent.hover",
    },
    "WM": {
        "activeBackground": "surface.background",
        "activeForeground": "text.primary",
        "inactiveBackground": "surface.panel",
        "inactiveForeground": "text.secondary",
    },
}


def _rgb(tokens: Tokens, role: str) -> str:
    return ",".join(str(channel) for channel in to_rgb(tokens.color(role)))


def generate_scheme(base_text: str, tokens: Tokens) -> str:
    seen = {name: set() for name in SECTIONS}
    lines = []
    section = None
    for line in base_text.splitlines():
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
        elif "=" in line and section is not None:
            key = line.split("=", 1)[0]
            if section in SECTIONS and key in SECTIONS[section]:
                line = f"{key}={_rgb(tokens, SECTIONS[section][key])}"
                seen[section].add(key)
            elif section == "General" and key in ("ColorScheme", "Name"):
                line = f"{key}={SCHEME_NAME}"
        lines.append(line)

    missing = [
        f"{name}/{key}" for name, rules in SECTIONS.items() for key in rules if key not in seen[name]
    ]
    if missing:
        raise KeyError(f"base scheme is missing: {', '.join(missing)}")
    return "\n".join(lines) + "\n"
