from __future__ import annotations

# ThemeUserInterface attribute -> role, or (role, alpha hex) to set the alpha explicitly.
USER_INTERFACE = {
    "editor_border": "surface.background",
    "panel_back": "surface.panel",
    "panel_header": "surface.raised",
    "panel_title": "text.primary",
    "panel_text": "text.primary",
    "panel_active": "accent.base",
    "widget_text_cursor": "accent.hover",
    "link": "accent.hover",
    "axis_x": "axis.x",
    "axis_y": "axis.y",
    "axis_z": "axis.z",
    # Muted outlines: strong text color at low alpha.
    "editor_outline": ("text.strong", "10"),
    "panel_outline": ("text.strong", "0d"),
}

# ThemeView3D attribute -> role.
VIEW_3D = {"grid": "border.default", "grid_major": "border.default"}

# Applied to every wcol_* ThemeWidgetColors element.
WIDGET = {
    "outline": "border.default",
    "outline_sel": "accent.base",
    "inner": "surface.control",
    "inner_sel": "accent.base",
    "text": "text.primary",
    "text_sel": "text.strong",
}

# Flat widgets: no gradient shading.
WIDGET_FLAT = {"show_shaded": "FALSE", "shadetop": "0", "shadedown": "0"}

# Per-widget overrides applied after WIDGET, keyed by wcol_* slot name.
WIDGET_OVERRIDES = {
    "wcol_menu_back": {"inner": "surface.raised"},
    "wcol_tooltip": {"inner": "surface.raised"},
    "wcol_numslider": {"item": "accent.base"},
    "wcol_progress": {"item": "accent.base"},
}

# ThemeWidgetStateColors fills. Blender's animation-state colors are left alone.
WIDGET_STATE = {
    "error": "status.danger",
    "warning": "status.warning",
    "success": "status.success",
    "info": "accent.pressed",
}

# Attributes present on every editor's space element.
SPACE = {
    "title": "text.primary",
    "text": "text.primary",
    "text_hi": "text.strong",
    "header": "surface.background",
    "header_text": "text.primary",
    "header_text_hi": "text.strong",
}

# Editors whose main area is a canvas, not a panel.
VIEWPORT_EDITORS = frozenset({"view_3d", "image_editor", "node_editor"})

# ThemeRegionsSidebars attributes. Alpha from the base theme is preserved.
SIDEBARS = {"back": "surface.panel", "tab_back": "surface.background"}
