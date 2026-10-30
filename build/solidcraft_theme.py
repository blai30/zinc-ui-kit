from __future__ import annotations

import json
from pathlib import Path

from build.colors import to_hex
from build.tokens import Tokens

OUTPUT = Path("solidcraft") / "Zinc.json"

# Theme key -> role or palette entry, (color, alpha hex), or a list of colors.
# Workspace families (form violet, mesh yellow, render pink, sheet cyan, surface orange,
# sketch blue) and the blue additive preview keep their Tailwind colors; the accent is rose.
# The viewport stays one step lighter than the chrome (a black one hid bodies), and axes and
# status colors use 400 shades, which read better on dark gray than the 500s.
COLORS = {
    "accent": "accent.base",
    "accent_soft": "rose-950",
    "agent_busy": "accent.hover",
    "agent_ok": "green-400",
    "app_bar": "surface.background",
    # Hover tints: strong text at low alpha.
    "app_bar_hover": ("text.strong", "14"),
    "app_bar_hover_button": ("text.strong", "1f"),
    "app_bar_hover_strong": ("text.strong", "29"),
    "app_bar_hover_subtle": ("text.strong", "0d"),
    "app_bar_separator": "surface.control",
    "app_bar_tab_active": "surface.control",
    "app_bar_text": "text.primary",
    "axis_x": "red-400",
    "axis_y": "green-400",
    "axis_z": "blue-400",
    "bend_down": "amber-400",
    "bend_up": "green-400",
    "body": "zinc-600",
    "body_edge": "zinc-900",
    "body_selected": "accent.muted",
    "border": "border.default",
    "box_crossing": "green-400",
    "box_window": "accent.hover",
    "chip": "accent.base",
    "construction_geom": "amber-400",
    "construction_plane": ("amber-400", "22"),
    "continuity": ["green-400", "blue-400", "amber-400", "pink-400"],
    "control_border": "border.default",
    "control_fill": "surface.control",
    "cube_border": "zinc-600",
    "cube_face": "zinc-700",
    "cube_hover": "accent.pressed",
    "cube_text": "text.strong",
    "dialog_bg": "surface.panel",
    "dialog_body": "surface.panel",
    "dialog_border": "border.default",
    "dialog_footer": "surface.panel",
    "dialog_label": "text.primary",
    "dialog_rule": "surface.control",
    "dimension": "text.strong",
    "dimension_driven": "text.secondary",
    "error": "red-400",
    "field": "surface.raised",
    "file_background": "surface.background",
    "file_border": "border.default",
    "file_dim": "text.secondary",
    # White leaves Start screen thumbnails untinted.
    "file_image_tint": "#ffffff",
    "file_primary": "rose-950",
    "file_primary_border": "accent.base",
    "file_primary_ink": "rose-300",
    "file_rail": "surface.panel",
    "file_rail_hover": "surface.control",
    "file_rail_ink": "text.primary",
    "file_recovery": "amber-950",
    "file_recovery_border": "amber-800",
    "file_recovery_ink": "amber-300",
    "file_recovery_well": "amber-900",
    "file_surface": "surface.raised",
    "form_accent": "violet-400",
    "form_dim": "text.secondary",
    "form_error": "red-400",
    "form_error_fill": "red-950",
    "form_fill": "violet-500",
    "form_ink": "text.strong",
    "form_primary": "accent.base",
    "form_soft": "violet-950",
    "form_success": "green-400",
    "form_success_fill": "green-950",
    "form_tab_ink": "violet-300",
    "gizmo": ["red-400", "green-400", "blue-400"],
    "glyph_bg": "surface.control",
    "glyph_edge": "red-400",
    "glyph_text": "red-400",
    "grid": "surface.control",
    "grid_major": "border.default",
    "hover": "surface.control",
    "hover_edge": "rose-300",
    "hover_edge_halo": "zinc-950",
    "hover_profile": ("accent.base", "33"),
    "hover_profile_edge": "rose-300",
    "icon": "text.strong",
    "icons.agent": "violet-400",
    "icons.highlight": "text.strong",
    "icons.marker_halo": ("zinc-950", "cc"),
    "interference": "red-400",
    "logo": ["accent.hover", "accent.pressed", "zinc-500", "text.strong"],
    "manipulator": "accent.hover",
    "mesh_accent": "yellow-400",
    "mesh_fill": "yellow-500",
    "mesh_ink": "yellow-300",
    "mesh_soft": "yellow-950",
    "on_accent": "text.strong",
    "origin_plane": ("amber-400", "28"),
    "origin_plane_edge": ("amber-400", "88"),
    "origin_plane_hover": ("accent.base", "40"),
    "origin_point": "zinc-300",
    "overlay": "surface.panel",
    "panel": "surface.panel",
    "panel_header": "surface.raised",
    # Blue, not the accent, so additions stay distinct from red cuts.
    "preview_add": "blue-500",
    "preview_cut": ("red-400", "66"),
    "preview_new": "amber-400",
    "preview_sketch": "green-400",
    "profile_fill": ("accent.base", "22"),
    "render_accent": "pink-400",
    "render_fill": "pink-500",
    "render_ink": "pink-300",
    "render_soft": "pink-950",
    "rubber_band": "accent.hover",
    "section_cap": "amber-400",
    "sel_edge": "rose-300",
    "sel_edge_rim": "accent.hover",
    "sel_face": "accent.muted",
    "sel_profile": "rose-800",
    "sel_profile_edge": "rose-300",
    "sel_vertex": "rose-300",
    "selected_bg": "zinc-700",
    "selected_ink": "text.strong",
    "sheet_fill": "cyan-500",
    "sheet_ink": "cyan-300",
    "sheet_soft": "cyan-950",
    "sketch": "blue-300",
    "sketch_accent": "blue-400",
    "sketch_centerline": "amber-300",
    "sketch_construction": "amber-300",
    "sketch_fixed": "text.strong",
    "sketch_ink": "text.strong",
    "sketch_locked": "green-400",
    "sketch_lost": "red-400",
    "sketch_point": "text.strong",
    "sketch_point_free": "blue-300",
    "sketch_projected": "violet-300",
    "sketch_soft": "blue-950",
    "surface_accent": "orange-400",
    "surface_fill": "orange-500",
    "surface_ink": "orange-300",
    "surface_soft": "orange-950",
    "tab_on_fill_dark": "zinc-950",
    "text": "text.primary",
    "text_dim": "text.secondary",
    "timeline": "surface.panel",
    "timeline_item": "surface.control",
    "timeline_item_error": "red-900",
    "timeline_marker": "text.secondary",
    "toolbar": "surface.background",
    "triad": ["red-400", "green-400", "blue-400"],
    "viewport_bottom": "surface.raised",
    "viewport_top": "surface.raised",
    "warning": "amber-400",
}


def _color(tokens: Tokens, value: str | tuple[str, str] | list[str]) -> str | list[str]:
    if isinstance(value, list):
        return [_color(tokens, item) for item in value]
    if isinstance(value, tuple):
        name, alpha = value
        return _color(tokens, name) + alpha
    return value if value.startswith("#") else to_hex(tokens.resolve(value))


def generate_theme(tokens: Tokens) -> str:
    theme = {
        "base": "dark",
        "colors": {key: _color(tokens, value) for key, value in COLORS.items()},
        "format": "solidcraft-theme/1",
        "name": "Zinc",
    }
    return json.dumps(theme, indent=2, sort_keys=True) + "\n"


def build_solidcraft_theme(root: Path, tokens: Tokens) -> Path:
    path = root / OUTPUT
    path.write_text(generate_theme(tokens), encoding="utf-8", newline="\n")
    return path
