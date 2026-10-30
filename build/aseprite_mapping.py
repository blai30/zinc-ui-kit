from __future__ import annotations

from build.aseprite_sheet import Part, cursor, custom, frame, hex_color, icon, lucide, paint, rounded_rect
from build.tokens import Tokens

# Small radii and fills only. Borders mark focus and floating windows.
WIDGET_RADIUS = 4
PANEL_RADIUS = 6

# Icon colors: idle, hot or active, and disabled.
IDLE = "text.primary"
ACTIVE = "text.strong"
DISABLED = "zinc-600"
# Tinted icons (styles give them a color) only use alpha.
TINTED = "text.strong"

# Theme color id -> role or palette entry.
COLORS = {
    "text": "text.primary",
    "text_hot": "text.strong",
    "detail_text": "text.secondary",
    "disabled": "zinc-600",
    "face": "surface.panel",
    "hot_face": "surface.control",
    "selected": "accent.base",
    "selected_text": "text.strong",
    "separator_label": "text.secondary",
    "background": "surface.background",
    "textbox_text": "text.primary",
    "textbox_face": "surface.raised",
    "textbox_code_face": "surface.control",
    "entry_suffix": "text.secondary",
    "link_text": "accent.hover",
    "link_hover": "rose-300",
    "button_normal_text": "text.primary",
    "button_hot_text": "text.strong",
    "button_selected_text": "text.strong",
    "check_hot_face": "surface.control",
    "check_focus_face": "surface.raised",
    "radio_hot_face": "surface.control",
    "radio_focus_face": "surface.raised",
    "menuitem_normal_text": "text.primary",
    "menuitem_disabled_text": "zinc-600",
    "menuitem_normal_face": "surface.panel",
    "menuitem_hot_text": "text.strong",
    "menuitem_hot_face": "surface.control",
    "menuitem_highlight_text": "text.strong",
    "menuitem_highlight_face": "accent.muted",
    "window_face": "surface.panel",
    "window_titlebar_text": "text.primary",
    "window_titlebar_face": "surface.background",
    "editor_face": "surface.viewport",
    "editor_sprite_border": "surface.control",
    "editor_sprite_bottom_border": "surface.control",
    "editor_view_face": "surface.viewport",
    "listitem_normal_text": "text.primary",
    "listitem_normal_face": "surface.raised",
    "listitem_selected_text": "text.strong",
    "listitem_selected_face": "accent.muted",
    "slider_empty_text": "text.primary",
    "slider_full_text": "text.strong",
    "tab_normal_text": "text.secondary",
    "tab_active_text": "text.strong",
    "tab_active_face": "surface.panel",
    "popup_window_border": "border.default",
    "tooltip_text": "text.primary",
    "tooltip_face": "surface.raised",
    "filelist_even_row_text": "text.primary",
    "filelist_even_row_face": "surface.raised",
    "filelist_odd_row_text": "text.primary",
    "filelist_odd_row_face": "surface.raised",
    "filelist_selected_row_text": "text.strong",
    "filelist_selected_row_face": "accent.muted",
    "filelist_disabled_row_text": "text.secondary",
    "workspace": "surface.background",
    "workspace_text": "text.primary",
    "workspace_link": "accent.hover",
    "workspace_link_hover": "rose-300",
    "timeline_normal": "surface.panel",
    "timeline_normal_text": "text.secondary",
    "timeline_hover": "surface.control",
    "timeline_hover_text": "text.primary",
    "timeline_active": "surface.raised",
    "timeline_active_text": "text.strong",
    "timeline_active_hover": "zinc-700",
    "timeline_active_hover_text": "text.strong",
    "timeline_clicked": "accent.muted",
    "timeline_clicked_text": "text.strong",
    "timeline_focused_text": "text.strong",
    "timeline_padding": "surface.background",
    "timeline_band_highlight": "surface.control",
    "timeline_band_bg": "surface.raised",
    "status_bar_text": "text.secondary",
    "status_bar_face": "surface.background",
    "flag_normal": "surface.control",
    "flag_active": "accent.base",
    "flag_clicked": "accent.pressed",
    "select_box_ruler": "accent.base",
    "select_box_grid": "green-500",
    "palette_entries_separator": "surface.viewport",
}

FONT_SIZES = {"default": 14, "mini": 12}

# Style id -> attributes set after scaling (values are final pixels).
STYLE_ATTRIBUTES = {
    # Items sit side by side instead of overlapping their stock bevels.
    "buttonset": {"gap-rows": "1", "gap-columns": "1"},
}


# Custom glyphs on the Lucide 24 unit grid.
GLYPHS = {
    "play": '<path d="M7 4.5v15l12.5-7.5z" fill="currentColor"/>',
    "stop": '<rect x="5.5" y="5.5" width="13" height="13" rx="2" fill="currentColor"/>',
    "first": '<path d="M6 5v14"/><path d="M19 5 9 12l10 7z" fill="currentColor"/>',
    "previous": '<path d="M15 5 5 12l10 7z" fill="currentColor"/><path d="M19 5v14"/>',
    "next": '<path d="M5 5v14"/><path d="M9 5l10 7-10 7z" fill="currentColor"/>',
    "last": '<path d="M5 5l10 7-10 7z" fill="currentColor"/><path d="M19 5v14"/>',
    "help": '<path d="M8.5 9a3.5 3.5 0 1 1 5 3.2c-.9.4-1.5 1.2-1.5 2.2V15"/><circle cx="12" cy="19.5" r="1" fill="currentColor"/>',
    "center": '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2" fill="currentColor"/>',
    "dot": '<circle cx="12" cy="12" r="5" fill="currentColor" stroke="none"/>',
    "chevron_down": '<path d="m5 9 7 7 7-7"/>',
    "chevron_up": '<path d="m5 15 7-7 7 7"/>',
    "chevron_left": '<path d="m15 5-7 7 7 7"/>',
    "chevron_right": '<path d="m9 5 7 7-7 7"/>',
    "continuous": '<path d="M2 12h20"/><circle cx="12" cy="12" r="3.5" fill="currentColor"/>',
    "discontinuous": '<path d="M2 12h3M19 12h3"/><circle cx="12" cy="12" r="3.5" fill="currentColor"/>',
    "onionskin": '<circle cx="9" cy="12" r="6"/><circle cx="15" cy="12" r="6" fill="currentColor" fill-opacity=".4"/>',
    "breakpoint": '<circle cx="12" cy="12" r="7" fill="currentColor" stroke="none"/>',
    "zindex": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 16 9 5 9-5"/>',
    "tiles": '<rect x="3" y="3" width="7.5" height="7.5" rx="1"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1"/>',
    "tiles_manual": '<rect x="3" y="3" width="7.5" height="7.5" rx="1" fill="currentColor"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1"/>',
    "tiles_auto": '<rect x="3" y="3" width="7.5" height="7.5" rx="1" fill="currentColor"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1" fill="currentColor"/>',
    "tiles_stack": '<rect x="3" y="9" width="12" height="12" rx="1.5"/><path d="M8 5.5V4.5A1.5 1.5 0 0 1 9.5 3h10A1.5 1.5 0 0 1 21 4.5v10a1.5 1.5 0 0 1-1.5 1.5h-1"/>',
    "symmetry_none": '<rect x="3" y="3" width="18" height="18" rx="3"/>',
    "symmetry_horizontal": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 1v22" stroke-dasharray="2.5 2.5"/>',
    "symmetry_vertical": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M1 12h22" stroke-dasharray="2.5 2.5"/>',
    "symmetry_right": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M1 23 23 1" stroke-dasharray="2.5 2.5"/>',
    "symmetry_left": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M1 1l22 22" stroke-dasharray="2.5 2.5"/>',
    "filled_rectangle": '<rect x="3" y="5" width="18" height="14" rx="2" fill="currentColor" fill-opacity=".5"/>',
    "rectangle": '<rect x="3" y="5" width="18" height="14" rx="2"/>',
    "filled_ellipse": '<ellipse cx="12" cy="12" rx="9.5" ry="7" fill="currentColor" fill-opacity=".5"/>',
    "ellipse": '<ellipse cx="12" cy="12" rx="9.5" ry="7"/>',
    "line": '<path d="M5 19 19 5"/>',
    "gradient": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 3v18M11 3v18" stroke-opacity=".9"/><path d="M15 3v18" stroke-opacity=".5"/><path d="M19 3v18" stroke-opacity=".2"/>',
    "jumble": '<path d="M4 8h3l3 4M4 16h3l10-8h3M14 16h6"/><path d="m18 6 2 2-2 2M18 14l2 2-2 2"/>',
    "opaque": '<rect x="3" y="3" width="18" height="18" rx="2" fill="currentColor" fill-opacity=".5"/>',
    "masked": '<rect x="3" y="3" width="18" height="18" rx="2" stroke-dasharray="3 3"/>',
    "angle": '<path d="M4 20h16M4 20 16 6"/><path d="M10 20a6 6 0 0 0-1.6-4.1"/>',
    "delta": '<path d="M12 4 21 20H3z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "spin_up": '<path d="M5 16 12 8l7 8z" fill="currentColor"/>',
    "spin_down": '<path d="M5 8l7 8 7-8z" fill="currentColor"/>',
    "dynamics": '<path d="M3 18c3-9 5-12 7-12s2 10 4 10 3-4 7-4"/>',
}

# Cursor glyphs. Pointer shapes are filled.
POINTER = '<path d="M4.04 4.69a.5.5 0 0 1 .65-.65l16 6.5a.5.5 0 0 1-.06.95l-6.13 1.58a2 2 0 0 0-1.43 1.43l-1.58 6.13a.5.5 0 0 1-.95.06z" fill="currentColor"/>'
SMALL_POINTER = f'<g transform="scale(.75)">{POINTER}</g>'
ROTATE = '<path d="M6 15.5a7.5 7.5 0 0 1 12 0"/><path d="M3.5 13.5 6 15.5l1.5-3M20.5 13.5 18 15.5l-1.5-3"/>'
SKEW = '<path d="M5 8.5h14M7.5 6 5 8.5 7.5 11M16.5 6 19 8.5 16.5 11"/><path d="M4 15.5h16"/>'
COMPASS = {"n": 0, "ne": 45, "e": 90, "se": 135, "s": 180, "sw": 225, "w": 270, "nw": 315}


def _cursors() -> dict[str, Part]:
    parts = {
        "cursor_normal": cursor(POINTER, (4.5, 4.5)),
        "cursor_normal_add": cursor(SMALL_POINTER + '<path d="M18 13v8M14 17h8"/>', (3.4, 3.4)),
        "cursor_crosshair": cursor('<path d="M12 2v7M12 15v7M2 12h7M15 12h7"/>', (12, 12)),
        "cursor_forbidden": cursor(SMALL_POINTER + '<circle cx="17.5" cy="17.5" r="4.5"/><path d="m14.3 14.3 6.4 6.4"/>', (3.4, 3.4)),
        "cursor_hand": cursor(lucide("pointer"), (8, 2.5)),
        "cursor_scroll": cursor(lucide("hand-grab"), (12, 12)),
        "cursor_move": cursor(SMALL_POINTER + f'<g transform="translate(11 11) scale(.55)">{lucide("move")}</g>', (3.4, 3.4)),
        "cursor_move_selection": cursor(SMALL_POINTER + '<rect x="13" y="13" width="9" height="9" rx="1" stroke-dasharray="2 2"/>', (3.4, 3.4)),
        "cursor_eyedropper": cursor(lucide("pipette"), (2.5, 21.5)),
        "cursor_magnifier": cursor(lucide("search"), (11, 11)),
    }
    for direction, angle in COMPASS.items():
        if direction in ("n", "s"):
            resize = lucide("move-vertical")
        elif direction in ("e", "w"):
            resize = lucide("move-horizontal")
        elif direction in ("ne", "sw"):
            resize = lucide("move-diagonal")
        else:
            resize = lucide("move-diagonal-2")
        parts[f"cursor_size_{direction}"] = cursor(resize, (12, 12))
        parts[f"cursor_rotate_{direction}"] = cursor(ROTATE, (12, 12), rotate=angle)
        parts[f"cursor_skew_{direction}"] = cursor(SKEW, (12, 12), rotate=angle)
    parts["cursor_size_ns"] = parts["cursor_size_n"]
    parts["cursor_size_we"] = parts["cursor_size_e"]
    return parts


def _states(name: str, glyph: str, width: int, height: int | None = None, states=None, **options) -> dict[str, Part]:
    # One icon per state suffix, e.g. {"": IDLE, "_selected": ACTIVE}.
    states = states or {"": IDLE}
    return {f"{name}{suffix}": icon(glyph, width, height, color, **options) for suffix, color in states.items()}


def _ring(width: int, height: int, slices, color: str, radius: float, thickness: float = 2) -> Part:
    return frame(width, height, slices, None, color, radius, thickness)


def _timeline_cell(fill: str | None) -> Part:
    # Flat cell with a 1 px divider on the right and bottom edges.
    def draw(tokens: Tokens) -> str:
        body = f'<rect width="24" height="24" {paint(tokens, fill, "fill")}/>' if fill else ""
        divider = paint(tokens, "surface.background", "fill")
        return body + f'<rect x="23" width="1" height="24" {divider}/><rect y="23" width="24" height="1" {divider}/>'

    return custom(24, 24, draw, (4, 16, 4, 4, 16, 4))


def _cel(color: str, kind: str) -> Part:
    # Timeline cel markers. Continued cels draw as a pill that runs into the neighbors.
    slices = {
        "empty": (10, 6, 8, 10, 6, 8),
        "key": (10, 6, 8, 10, 6, 8),
        "left": (0, 16, 8, 10, 6, 8),
        "right": (10, 14, 0, 10, 6, 8),
        "both": (0, 24, 0, 10, 6, 8),
    }[kind]

    def draw(tokens: Tokens) -> str:
        fill = paint(tokens, color, "fill")
        if kind == "empty":
            return f'<circle cx="12" cy="12" r="4.5" fill="none" {paint(tokens, color, "stroke")} stroke-width="1.5"/>'
        circle = f'<circle cx="12" cy="12" r="5" {fill}/>'
        bar = {"key": "", "left": (0, 12), "right": (12, 24), "both": (0, 24)}[kind]
        if not bar:
            return circle
        start, end = bar
        return circle + f'<rect x="{start}" y="9" width="{end - start}" height="6" {fill}/>'

    return custom(24, 24, draw, slices)


def _link(kind: str) -> Part:
    slices = {"left": (6, 18, 0, 8, 2, 14), "both": (0, 24, 0, 8, 2, 14), "right": (0, 18, 6, 8, 2, 14)}[kind]

    def draw(tokens: Tokens) -> str:
        start = 6 if kind == "left" else 0
        end = 18 if kind == "right" else 24
        return f'<rect x="{start}" y="8" width="{end - start}" height="2" {paint(tokens, "text.secondary", "fill")}/>'

    return custom(24, 24, draw, slices)


def _pivot(index: int) -> Part:
    def draw(tokens: Tokens) -> str:
        dots = []
        for cell in range(9):
            x, y = 2 + cell % 3 * 5, 2 + cell // 3 * 5
            if cell == index:
                dots.append(f'<rect x="{x - 1.5}" y="{y - 1.5}" width="5" height="5" rx="1" {paint(tokens, ACTIVE, "fill")}/>')
            else:
                dots.append(f'<rect x="{x}" y="{y}" width="2" height="2" {paint(tokens, "text.secondary", "fill")}/>')
        return "".join(dots)

    return custom(16, 16, draw)


def _outline(cells: set[int]) -> Part:
    def draw(tokens: Tokens) -> str:
        boxes = []
        for cell in range(9):
            x, y = 2 + cell % 3 * 8, 2 + cell // 3 * 8
            fill = paint(tokens, IDLE, "fill") if cell in cells else 'fill="none"'
            boxes.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="6" height="6" rx="1" {fill} {paint(tokens, "text.secondary", "stroke")}/>')
        return "".join(boxes)

    return custom(26, 26, draw)


def _swatch(kind: str) -> Part:
    # New sprite dialog color mode and background icons.
    def draw(tokens: Tokens) -> str:
        border = paint(tokens, "border.default", "stroke")
        box = f'<path d="{rounded_rect(4.5, 4.5, 23, 23, 4)}"'
        if kind == "rgb":
            circles = [("red-500", 12, 13), ("green-500", 20, 13), ("blue-500", 16, 20)]
            return "".join(f'<circle cx="{x}" cy="{y}" r="7" {paint(tokens, name, "fill")} fill-opacity=".85"/>' for name, x, y in circles)
        if kind == "grayscale":
            stops = "".join(f'<stop offset="{offset}" stop-color="{color}"/>' for offset, color in ((0, "#09090b"), (1, "#fafafa")))
            return f'<defs><linearGradient id="gray">{stops}</linearGradient></defs>{box} fill="url(#gray)" {border}/>'
        if kind == "indexed":
            cells = [("rose-500", 5, 5), ("amber-400", 16, 5), ("sky-400", 5, 16), ("emerald-400", 16, 16)]
            return "".join(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" {paint(tokens, name, "fill")}/>' for name, x, y in cells)
        if kind == "transparent":
            checks = "".join(
                f'<rect x="{5 + column * 5.5}" y="{5 + row * 5.5}" width="5.5" height="5.5" {paint(tokens, "zinc-500", "fill")}/>'
                for row in range(4) for column in range(4) if (row + column) % 2 == 0
            )
            return f'{box} {paint(tokens, "zinc-300", "fill")}/>{checks}{box} fill="none" {border}/>'
        color = "zinc-950" if kind == "black" else "zinc-50"
        return f'{box} {paint(tokens, color, "fill")} {border}/>'

    return custom(32, 32, draw)


def _face(state: str) -> Part:
    # Home tab mascot: a rounded tile with eyes, cheeks on hover, and closed eyes when pressed.
    def draw(tokens: Tokens) -> str:
        tile_color = "zinc-300" if state == "pushed" else "surface.control"
        feature = "surface.control" if state == "pushed" else "text.strong"
        tile = f'<path d="{rounded_rect(2, 2, 52, 56, 12)}" {paint(tokens, tile_color, "fill")} {paint(tokens, "border.default", "stroke")} stroke-width="2"/>'
        if state == "pushed":
            eyes = "".join(f'<rect x="{x}" y="27" width="10" height="4" rx="2" {paint(tokens, feature, "fill")}/>' for x in (14, 32))
        else:
            eyes = "".join(f'<rect x="{x}" y="18" width="5" height="18" rx="2.5" {paint(tokens, feature, "fill")}/>' for x in (17, 34))
        cheeks = ""
        if state == "mouse":
            cheeks = "".join(f'<rect x="{x}" y="40" width="9" height="4" rx="2" {paint(tokens, "accent.hover", "fill")}/>' for x in (10, 37))
        return tile + eyes + cheeks

    return custom(56, 60, draw)


def _gradient(kind: str) -> Part:
    def draw(tokens: Tokens) -> str:
        color = hex_color(tokens, IDLE)
        stops = f'<stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/>'
        if kind == "linear":
            fill = f'<linearGradient id="linear">{stops}</linearGradient>'
        else:
            fill = f'<radialGradient id="radial">{stops}</radialGradient>'
        return f'<defs>{fill}</defs><rect x="1" y="1" width="14" height="14" rx="3" fill="url(#{kind})"/>'

    return custom(16, 16, draw)


def _handle(kind: str) -> Part:
    def draw(tokens: Tokens) -> str:
        light, dark = hex_color(tokens, "zinc-50"), hex_color(tokens, "zinc-950")
        if kind == "transformation":
            return f'<rect x="1.5" y="1.5" width="9" height="9" rx="1.5" fill="{light}" stroke="{dark}"/>'
        return (
            f'<circle cx="9" cy="9" r="6.5" fill="none" stroke="{dark}" stroke-width="3"/>'
            f'<circle cx="9" cy="9" r="6.5" fill="none" stroke="{light}" stroke-width="1.5"/>'
            f'<circle cx="9" cy="9" r="2" fill="{light}" stroke="{dark}"/>'
        )

    size = 12 if kind == "transformation" else 18
    return custom(size, size, draw)


def _color_wheel_indicator() -> Part:
    def draw(tokens: Tokens) -> str:
        return (
            f'<circle cx="5" cy="5" r="3.5" fill="none" stroke="{hex_color(tokens, "zinc-950")}" stroke-width="2.5"/>'
            f'<circle cx="5" cy="5" r="3.5" fill="none" stroke="#ffffff" stroke-width="1"/>'
        )

    return custom(10, 10, draw)


def _line(width: int, height: int, vertical: bool) -> Part:
    def draw(tokens: Tokens) -> str:
        color = paint(tokens, "border.default", "fill")
        if vertical:
            return f'<rect x="{width // 2}" width="1" height="{height}" {color}/>'
        return f'<rect y="{height // 2}" width="{width}" height="1" {color}/>'

    return custom(width, height, draw)


def _window(tokens: Tokens) -> str:
    # Rounded window with a title strip on top (title is 30 px of the 48 px sprite).
    width, height, title = 26, 48, 30
    outer = f'<path d="{rounded_rect(0.5, 0.5, width - 1, height - 1, PANEL_RADIUS - 0.5)}"'
    strip = f'<path d="{rounded_rect(1, 1, width - 2, title - 1, PANEL_RADIUS - 1, "top")}"'
    rule = f'<rect x="1" y="{title - 1}" width="{width - 2}" height="1" {paint(tokens, "border.default", "fill")}/>'
    return (
        f'{outer} {paint(tokens, "surface.panel", "fill")} {paint(tokens, "border.default", "stroke")}/>'
        f'{strip} {paint(tokens, "surface.background", "fill")}/>{rule}'
    )


def _empty(width: int, height: int) -> Part:
    return custom(width, height, lambda tokens: "")


def _parts() -> dict[str, Part]:
    parts: dict[str, Part] = {}
    parts.update(_cursors())

    # Check boxes and radio buttons.
    def check(fill: str, border: str, mark: bool) -> Part:
        def draw(tokens: Tokens) -> str:
            box = f'<path d="{rounded_rect(0.5, 0.5, 15, 15, 3.5)}" {paint(tokens, fill, "fill")} {paint(tokens, border, "stroke")}/>'
            tick = f'<path d="m4.5 8.5 2.5 2.5 4.5-5.5" fill="none" {paint(tokens, ACTIVE, "stroke")} stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
            return box + (tick if mark else "")

        return custom(16, 16, draw)

    def radio(fill: str, border: str, mark: bool) -> Part:
        def draw(tokens: Tokens) -> str:
            ring = f'<circle cx="8" cy="8" r="7.5" {paint(tokens, fill, "fill")} {paint(tokens, border, "stroke")}/>'
            dot = f'<circle cx="8" cy="8" r="3" {paint(tokens, ACTIVE, "fill")}/>'
            return ring + (dot if mark else "")

        return custom(16, 16, draw)

    parts["check_normal"] = check("surface.raised", "zinc-600", False)
    parts["check_disabled"] = check("surface.panel", "zinc-700", False)
    parts["check_selected"] = check("accent.base", "accent.base", True)
    parts["radio_normal"] = radio("surface.raised", "zinc-600", False)
    parts["radio_disabled"] = radio("surface.panel", "zinc-700", False)
    parts["radio_selected"] = radio("accent.base", "accent.base", True)
    parts["check_focus"] = _ring(20, 20, (4, 12, 4, 4, 12, 4), "accent.base", 4, 1)
    parts["radio_focus"] = parts["check_focus"]

    # Buttons. Stock bottom bevels become symmetric padding.
    button = (6, 4, 6, 6, 4, 6)
    parts["button_normal"] = frame(16, 16, button, "surface.control", None, WIDGET_RADIUS)
    parts["button_hot"] = frame(16, 16, button, "zinc-700", None, WIDGET_RADIUS)
    parts["button_focused"] = frame(16, 16, button, "surface.control", "accent.base", WIDGET_RADIUS)
    parts["button_selected"] = frame(16, 16, button, "accent.base", None, WIDGET_RADIUS)

    left, right, right_wide = (6, 4, 6, 6, 4, 6), (4, 2, 6, 6, 4, 6), (4, 4, 6, 6, 4, 6)
    for state, fill, border in (
        ("normal", "surface.control", None),
        ("hot", "zinc-700", None),
        ("focused", "surface.control", "accent.base"),
        ("selected", "accent.base", None),
    ):
        parts[f"drop_down_button_left_{state}"] = frame(16, 16, left, fill, border, WIDGET_RADIUS, corners="left")
        right_slices = right_wide if state in ("focused", "selected") else right
        parts[f"drop_down_button_right_{state}"] = frame(sum(right_slices[:3]), 16, right_slices, fill, border, WIDGET_RADIUS, corners="right")

    # Text fields (and scroll view borders).
    field = (6, 4, 6, 5, 4, 5)
    parts["sunken_normal"] = frame(16, 14, field, "surface.viewport", None, WIDGET_RADIUS)
    parts["sunken_focused"] = frame(16, 14, field, "surface.viewport", "accent.base", WIDGET_RADIUS)
    parts["sunken2_normal"] = frame(16, 14, field, "surface.viewport", None, WIDGET_RADIUS)
    parts["sunken2_focused"] = frame(16, 14, field, "surface.viewport", "accent.base", WIDGET_RADIUS)
    parts["sunken_mini_normal"] = frame(12, 10, (4, 4, 4, 3, 4, 3), "surface.viewport", None, 3)
    parts["sunken_mini_focused"] = frame(12, 10, (4, 4, 4, 3, 4, 3), "surface.viewport", "accent.base", 3)

    # Windows and popups.
    parts["window"] = custom(26, 48, _window, (8, 10, 8, 30, 8, 10))
    parts["menu"] = frame(16, 16, (5, 6, 5, 5, 6, 5), "surface.panel", "border.default", WIDGET_RADIUS)
    parts["tooltip"] = frame(16, 16, (6, 4, 6, 5, 6, 5), "surface.control", None, WIDGET_RADIUS)
    parts["tooltip_arrow"] = parts["tooltip"]
    parts["window_button_normal"] = _empty(18, 22)
    parts["window_button_hot"] = frame(18, 22, None, "surface.control", None, 4)
    parts["window_button_selected"] = frame(18, 22, None, "zinc-700", None, 4)
    for name, glyph in (("close", lucide("x")), ("play", GLYPHS["play"]), ("stop", GLYPHS["stop"]),
                        ("center", GLYPHS["center"]), ("help", GLYPHS["help"])):
        parts[f"window_{name}_icon"] = icon(glyph, 12, 12, TINTED, 1.5)

    # Sliders.
    slider = (6, 4, 6, 5, 4, 5)
    mini = (3, 4, 3, 3, 4, 3)
    for suffix, border in (("", None), ("_focused", "accent.base")):
        parts[f"slider_full{suffix}"] = frame(16, 14, slider, "accent.muted", border, WIDGET_RADIUS)
        parts[f"slider_empty{suffix}"] = frame(16, 14, slider, "surface.viewport", border, WIDGET_RADIUS)
        parts[f"mini_slider_full{suffix}"] = frame(10, 10, mini, "accent.muted", border, 3)
        parts[f"mini_slider_empty{suffix}"] = frame(10, 10, mini, "surface.viewport", border, 3)
    parts["mini_slider_thumb"] = icon(GLYPHS["spin_up"], 10, 8, "text.secondary", 1)
    parts["mini_slider_thumb_focused"] = icon(GLYPHS["spin_up"], 10, 8, "accent.base", 1)

    parts["separator_horz"] = _line(18, 10, False)
    parts["separator_vert"] = _line(10, 18, True)

    # Small navigation icons.
    arrow_states = {"": IDLE, "_selected": ACTIVE, "_disabled": DISABLED}
    for direction in ("down", "up", "left", "right"):
        parts.update(_states(f"combobox_arrow_{direction}", GLYPHS[f"chevron_{direction}"], 18, 16, arrow_states, stroke=1.75))
    parts.update(_states("arrow_circle_cw", lucide("rotate-cw"), 20, 20, {"": IDLE, "_selected": ACTIVE}))
    parts.update(_states("newfolder", lucide("folder-plus"), 18, 18, {"": IDLE, "_selected": ACTIVE}))
    parts["list_view"] = icon(lucide("list"), 18)
    parts["small_icon_view"] = icon(lucide("grid-3x3"), 18)
    parts["big_icon_view"] = icon(lucide("layout-grid"), 18)

    # Tool buttons and button sets.
    tool = (5, 22, 5, 5, 22, 5)
    item = (5, 6, 5, 5, 6, 5)
    parts["toolbutton_normal"] = _empty(32, 32)
    parts["toolbutton_last"] = _empty(32, 32)
    parts["toolbutton_hot"] = frame(32, 32, tool, "accent.muted", None, WIDGET_RADIUS)
    parts["toolbutton_pushed"] = frame(32, 32, tool, "accent.base", None, WIDGET_RADIUS)
    parts["buttonset_item_normal"] = frame(16, 16, item, "surface.control", None, WIDGET_RADIUS)
    parts["buttonset_item_hot"] = frame(16, 16, item, "zinc-700", None, WIDGET_RADIUS)
    parts["buttonset_item_hot_focused"] = frame(16, 16, item, "zinc-700", "accent.base", WIDGET_RADIUS)
    parts["buttonset_item_focused"] = frame(16, 16, item, "surface.control", "accent.base", WIDGET_RADIUS)
    parts["buttonset_item_pushed"] = frame(16, 16, item, "accent.base", None, WIDGET_RADIUS)
    parts["buttonset_item_active"] = frame(16, 16, item, "accent.muted", None, WIDGET_RADIUS)

    # Document tabs. The active tab joins the strip below it.
    parts["tab_normal"] = frame(28, 24, (8, 10, 10, 8, 12, 4), None)
    parts["tab_active"] = frame(32, 24, (8, 14, 10, 8, 12, 4), "surface.background", None, WIDGET_RADIUS, corners="top")
    parts["tab_bottom_active"] = frame(32, 10, (8, 14, 10, 4, 2, 4), "surface.background")
    parts["tab_bottom_normal"] = frame(24, 10, None, "surface.background")
    parts["tab_filler"] = _empty(4, 24)
    parts.update(_states("tab_modified_icon", GLYPHS["dot"], 12, 12, {"_normal": "text.secondary", "_active": ACTIVE}))
    parts.update(_states("tab_close_icon", lucide("x"), 12, 12, {"_normal": "text.secondary", "_active": ACTIVE}, stroke=1.5))
    parts["tab_icon_bg_clicked"] = frame(28, 24, None, "zinc-700", None, 4, inset=2)
    parts["tab_icon_bg_hover"] = frame(28, 24, None, "surface.control", None, 4, inset=2)
    parts.update(_states("tab_home_icon", lucide("house"), 14, 16, {"_normal": "text.secondary", "_active": ACTIVE}))

    # Editor borders.
    editor = (6, 20, 6, 6, 20, 6)
    parts["editor_normal"] = frame(32, 32, editor, None)
    parts["editor_selected"] = frame(32, 32, editor, None, "border.default")

    # Color bar swatch frames and selection rings.
    swatch = (3, 4, 3, 3, 4, 3)
    for index in range(4):
        parts[f"colorbar_{index}"] = _ring(10, 10, swatch, "surface.panel", 0, 1)
    parts["colorbar_selection"] = _ring(10, 10, swatch, "text.strong", 0)
    parts["colorbar_selection_hot"] = _ring(10, 10, swatch, "accent.hover", 0)
    parts["simple_color_border"] = _ring(10, 10, swatch, "surface.panel", 0, 1)
    parts["simple_color_selected"] = _ring(10, 10, swatch, "accent.base", 0)

    # Scroll bars: a thin pill inside the track.
    parts["scrollbar_bg"] = custom(24, 24, lambda tokens: "", (10, 4, 10, 10, 4, 10))
    parts["scrollbar_thumb"] = frame(24, 24, (10, 4, 10, 10, 4, 10), "zinc-700", None, 5, inset=5)
    mini_scroll = (6, 4, 6, 6, 4, 6)
    for prefix, idle, hot in (("mini_", "zinc-700", "zinc-600"), ("transparent_", ("zinc-50", 0.35), ("zinc-50", 0.55))):
        parts[f"{prefix}scrollbar_bg"] = custom(16, 16, lambda tokens: "", mini_scroll)
        parts[f"{prefix}scrollbar_bg_hot"] = custom(16, 16, lambda tokens: "", mini_scroll)
        parts[f"{prefix}scrollbar_thumb"] = frame(16, 16, mini_scroll, idle, None, 3, inset=3)
        parts[f"{prefix}scrollbar_thumb_hot"] = frame(16, 16, mini_scroll, hot, None, 3, inset=3)

    # Animation, palette, and debugger buttons.
    for name in ("first", "previous", "play", "stop", "next", "last"):
        parts[f"ani_{name}"] = icon(GLYPHS[name], 12, 12, IDLE, 1.5)
    parts["pal_sort"] = icon(lucide("arrow-down-wide-narrow"), 12, 12, IDLE, 1.25)
    parts["pal_presets"] = icon(lucide("library"), 12, 12, IDLE, 1.25)
    parts["pal_options"] = icon(lucide("menu"), 12, 12, IDLE, 1.25)
    parts["pal_resize"] = icon(lucide("move-horizontal"), 12, 12, IDLE, 1.25)
    parts["debug_continue"] = icon(GLYPHS["play"], 14)
    parts["debug_pause"] = icon(lucide("pause"), 14)
    parts["debug_step_into"] = icon(lucide("arrow-down-to-dot"), 14)
    parts["debug_step_over"] = icon(lucide("redo-dot"), 14)
    parts["debug_step_out"] = icon(lucide("arrow-up-from-dot"), 14)
    parts["debug_breakpoint"] = icon(GLYPHS["breakpoint"], 14, color="red-500")

    parts["selection_replace"] = icon(lucide("square"), 14)
    parts["selection_add"] = icon(lucide("square-plus"), 14)
    parts["selection_subtract"] = icon(lucide("square-minus"), 14)
    parts["selection_intersect"] = icon(lucide("squares-intersect"), 14)
    parts["unpinned"] = icon(lucide("pin"), 16, color=TINTED, rotate=45)
    parts["pinned"] = icon(lucide("pin"), 16, color=TINTED)

    # Canvas handles.
    parts["transformation_handle"] = _handle("transformation")
    parts["pivot_handle"] = _handle("pivot")

    # Timeline.
    parts["timeline_none"] = custom(24, 24, lambda tokens: "", (4, 16, 4, 4, 16, 4))
    for name, color in (("normal", "surface.panel"), ("active", "surface.raised"), ("hover", "surface.control"),
                        ("active_hover", "zinc-700"), ("clicked", "accent.muted")):
        parts[f"timeline_{name}"] = _timeline_cell(color)
    parts["timeline_focused"] = _ring(24, 24, (4, 16, 4, 4, 16, 4), "accent.base", 2)
    timeline_states = {"_normal": "text.secondary", "_active": ACTIVE}
    for name, glyph in (("open_eye", lucide("eye")), ("closed_eye", lucide("eye-closed")),
                        ("open_padlock", lucide("lock-open")), ("closed_padlock", lucide("lock")),
                        ("continuous", GLYPHS["continuous"]), ("discontinuous", GLYPHS["discontinuous"]),
                        ("closed_group", lucide("folder")), ("open_group", lucide("folder-open"))):
        parts.update(_states(f"timeline_{name}", glyph, 24, 24, timeline_states, padding=4))
    parts.update(_states("timeline_gear", lucide("settings"), 24, 24, {"": "text.secondary", "_active": ACTIVE}, padding=4))
    parts.update(_states("timeline_onionskin", GLYPHS["onionskin"], 24, 24, {"": "text.secondary", "_active": ACTIVE}, padding=4))
    for suffix, color in (("_normal", "text.secondary"), ("_active", ACTIVE)):
        parts[f"timeline_empty_frame{suffix}"] = _cel(color, "empty")
        parts[f"timeline_keyframe{suffix}"] = _cel(color, "key")
        parts[f"timeline_from_left{suffix}"] = _cel(color, "left")
        parts[f"timeline_from_right{suffix}"] = _cel(color, "right")
        parts[f"timeline_from_both{suffix}"] = _cel(color, "both")
    parts["timeline_left_link_active"] = _link("left")
    parts["timeline_both_links_active"] = _link("both")
    parts["timeline_right_link_active"] = _link("right")
    parts["timeline_onionskin_range"] = frame(24, 24, (6, 12, 6, 6, 12, 6), ("accent.base", 0.25), None, 4)
    for corner in ("", "_tr", "_bl", "_br"):
        parts[f"timeline_padding{corner}"] = frame(24, 24, (2, 20, 2, 2, 20, 2), "surface.background")
    parts["timeline_drop_layer_deco"] = frame(14, 8, (6, 2, 6, 3, 2, 3), "accent.base", None, 3)
    parts["timeline_drop_frame_deco"] = frame(8, 14, (3, 2, 3, 6, 2, 6), "accent.base", None, 3)
    parts["timeline_loop_range"] = _ring(24, 24, (8, 8, 8, 6, 12, 6), "accent.base", 4)
    parts["timeline_zindex"] = icon(GLYPHS["zindex"], 12, 12, "text.secondary", 1.25)

    parts["flag_normal"] = icon(lucide("flag"), 32, 20, "text.secondary")
    parts["flag_highlight"] = icon(lucide("flag"), 32, 20, ACTIVE)

    for name, glyph in (("ok", lucide("check")), ("drop", lucide("stamp")), ("cancel", lucide("x"))):
        parts.update(_states(f"drop_pixels_{name}", glyph, 14, 16, {"": IDLE, "_selected": ACTIVE}))

    parts["warning_box"] = icon(lucide("triangle-alert"), 18, 20, "amber-400")

    # Canvas size anchors.
    for name, glyph in (("nw", "arrow-up-left"), ("n", "arrow-up"), ("ne", "arrow-up-right"), ("w", "arrow-left"),
                        ("e", "arrow-right"), ("sw", "arrow-down-left"), ("s", "arrow-down"), ("se", "arrow-down-right")):
        parts[f"canvas_{name}"] = icon(lucide(glyph), 32, padding=6)
    parts["canvas_c"] = icon(lucide("square"), 32, padding=8)
    parts["canvas_empty"] = _empty(2, 2)

    # Inks and selection modes.
    for name, glyph in (("simple", lucide("droplet")), ("alpha_compositing", lucide("blend")),
                        ("copy_color", lucide("copy")), ("lock_alpha", lucide("lock-keyhole")),
                        ("shading", lucide("contrast"))):
        parts[f"ink_{name}"] = icon(glyph, 32, padding=7)
    parts["selection_opaque"] = icon(GLYPHS["opaque"], 32, 20)
    parts["selection_masked"] = icon(GLYPHS["masked"], 32, 20)

    for index, name in enumerate(("northwest", "north", "northeast", "west", "center", "east", "southwest", "south", "southeast")):
        parts[f"pivot_{name}"] = _pivot(index)

    for kind in ("rgb", "grayscale", "indexed", "black", "white", "transparent"):
        parts[f"icon_{kind}"] = _swatch(kind)
    parts["color_wheel_indicator"] = _color_wheel_indicator()

    for name, glyph in (("no_symmetry", "symmetry_none"), ("horizontal_symmetry", "symmetry_horizontal"),
                        ("vertical_symmetry", "symmetry_vertical"), ("right_diagonal_symmetry", "symmetry_right"),
                        ("left_diagonal_symmetry", "symmetry_left")):
        parts[name] = icon(GLYPHS[glyph], 26, padding=3)

    # Small field icons (tinted by styles where they sit in lists).
    parts["icon_arrow_down"] = icon(GLYPHS["chevron_down"], 14, 8, IDLE, 1.5)
    parts["icon_close"] = icon(lucide("x"), 14)
    parts["icon_search"] = icon(lucide("search"), 16)
    parts["icon_user_data"] = icon(lucide("sticky-note"), 16)
    parts["icon_layout"] = icon(lucide("panels-top-left"), 12, 12, IDLE, 1.25)
    for name, glyph in (("pos", lucide("move")), ("size", lucide("scaling")), ("selsize", lucide("square-dashed")),
                        ("frame", lucide("film")), ("clock", lucide("clock")), ("start", lucide("arrow-left-to-line")),
                        ("end", lucide("arrow-right-to-line")), ("angle", GLYPHS["angle"]), ("key", lucide("key")),
                        ("distance", lucide("ruler")), ("grid", lucide("grid-3x3")), ("slice", lucide("slice")),
                        ("corner_radius", lucide("square-round-corner"))):
        parts[f"icon_{name}"] = icon(glyph, 16)
    parts["icon_save"] = icon(lucide("save"), 16, color=TINTED)
    parts["icon_save_small"] = icon(lucide("save"), 16)
    parts["icon_aspect_ratio"] = icon(lucide("proportions"), 20, 16)
    parts["icon_delta"] = icon(GLYPHS["delta"], 12, 16)
    parts["icon_add"] = icon(GLYPHS["plus"], 12, 12, IDLE, 1.5)

    # Tools.
    tools = {
        "rectangular_marquee": lucide("square-dashed"),
        "elliptical_marquee": lucide("circle-dashed"),
        "lasso": lucide("lasso"),
        "polygonal_lasso": lucide("lasso-select"),
        "magic_wand": lucide("wand-sparkles"),
        "pencil": lucide("pencil"),
        "spray": lucide("spray-can"),
        "eraser": lucide("eraser"),
        "eyedropper": lucide("pipette"),
        "hand": lucide("hand"),
        "move": lucide("move"),
        "zoom": lucide("zoom-in"),
        "slice": lucide("slice"),
        "paint_bucket": lucide("paint-bucket"),
        "gradient": GLYPHS["gradient"],
        "line": GLYPHS["line"],
        "curve": lucide("spline"),
        "rectangle": GLYPHS["rectangle"],
        "filled_rectangle": GLYPHS["filled_rectangle"],
        "ellipse": GLYPHS["ellipse"],
        "filled_ellipse": GLYPHS["filled_ellipse"],
        "contour": lucide("pen-tool"),
        "polygon": lucide("pentagon"),
        "text": lucide("type"),
        "blur": lucide("droplets"),
        "jumble": GLYPHS["jumble"],
        "configuration": lucide("settings-2"),
        "minieditor": lucide("picture-in-picture-2"),
        "timeline": lucide("square-chart-gantt"),
    }
    for name, glyph in tools.items():
        parts[f"tool_{name}"] = icon(glyph, 32, padding=6, stroke=1.75)

    parts["aseprite_face"] = _face("normal")
    parts["aseprite_face_mouse"] = _face("mouse")
    parts["aseprite_face_pushed"] = _face("pushed")
    parts["linear_gradient"] = _gradient("linear")
    parts["radial_gradient"] = _gradient("radial")

    folder = '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z" fill="currentColor" fill-opacity=".35"/>'
    parts["folder_icon_small"] = icon(folder, 20, 16, "zinc-400", 1.25)
    parts["folder_icon_medium"] = icon(folder, 32, 32, "zinc-400", 1.5, padding=2)
    parts["folder_icon_big"] = icon(folder, 64, 64, "zinc-400", 2, padding=4)

    parts["outline_circle"] = _outline({1, 3, 4, 5, 7})
    parts["outline_square"] = _outline(set(range(9)))
    parts["outline_horizontal"] = _outline({3, 4, 5})
    parts["outline_vertical"] = _outline({1, 4, 7})
    parts["outline_empty_pixel"] = frame(10, 10, None, None, "text.secondary", 2)
    parts["outline_full_pixel"] = frame(10, 10, None, IDLE, IDLE, 2)

    parts["dynamics"] = icon(GLYPHS["dynamics"], 32, padding=7)
    parts["dynamics_on"] = icon(GLYPHS["dynamics"], 32, padding=7, color="accent.hover")

    for name in ("tiles", "tiles_manual", "tiles_auto", "tiles_stack"):
        parts[name] = icon(GLYPHS[name], 12, 12, TINTED, 1.25)

    parts["one_win_icon"] = icon(lucide("square"), 16, 14)
    parts["multi_win_icon"] = icon(lucide("copy"), 16, 14)
    parts["spin_up"] = icon(GLYPHS["spin_up"], 10, 6, IDLE, 0.5)
    parts["spin_down"] = icon(GLYPHS["spin_down"], 10, 6, IDLE, 0.5)
    parts["corner_radius_field"] = icon(lucide("square-round-corner"), 32, padding=7)
    return parts


PARTS = _parts()
