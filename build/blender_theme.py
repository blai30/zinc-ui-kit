from __future__ import annotations

import xml.etree.ElementTree as ET

from build import blender_mapping as mapping
from build.tokens import Tokens


def _number(value: float) -> str:
    return f"{value:g}"


def _find(parent: ET.Element, path: str) -> ET.Element:
    found = parent.find(path)
    if found is None:
        raise LookupError(f"{path} not found under <{parent.tag}>")
    return found


def _set_value(element: ET.Element, name: str, value: str) -> None:
    # Raises KeyError when Blender renames or drops an attribute.
    if name not in element.attrib:
        raise KeyError(f"<{element.tag}> has no attribute {name!r}")
    element.set(name, value)


def _set_color(element: ET.Element, name: str, hex_color: str, alpha: str | None = None) -> None:
    # Use the given alpha, else keep the base alpha when the base value carries one (#rrggbbaa).
    current = element.attrib.get(name, "")
    if alpha is None and len(current) == 9:
        alpha = current[7:]
    _set_value(element, name, hex_color + (alpha or ""))


def _apply(element: ET.Element, rules: dict, tokens: Tokens) -> None:
    for name, rule in rules.items():
        role, alpha = (rule, None) if isinstance(rule, str) else rule
        _set_color(element, name, tokens.hex(role), alpha)


def generate_theme(base_xml: str, tokens: Tokens) -> str:
    root = ET.fromstring(base_xml)
    theme = _find(root, "Theme")

    interface = _find(theme, "user_interface/ThemeUserInterface")
    _apply(interface, mapping.USER_INTERFACE, tokens)
    _set_value(interface, "panel_roundness", _number(tokens.radius["panel"]))

    _apply(_find(theme, "view_3d/ThemeView3D"), mapping.VIEW_3D, tokens)

    has_state_slot = False
    for slot in interface:
        state = slot.find("ThemeWidgetStateColors")
        if state is not None:
            _apply(state, mapping.WIDGET_STATE, tokens)
            has_state_slot = True
            continue
        widget = slot.find("ThemeWidgetColors")
        if widget is None:
            continue
        _apply(widget, mapping.WIDGET, tokens)
        _apply(widget, mapping.WIDGET_OVERRIDES.get(slot.tag, {}), tokens)
        for name, value in mapping.WIDGET_FLAT.items():
            _set_value(widget, name, value)
        _set_value(widget, "roundness", _number(tokens.radius["widget"]))

    if not has_state_slot:
        raise LookupError("no ThemeWidgetStateColors found under the interface")
    unknown_slots = mapping.WIDGET_OVERRIDES.keys() - {slot.tag for slot in interface}
    if unknown_slots:
        raise LookupError(f"widget override slots not found: {sorted(unknown_slots)}")

    unknown_editors = mapping.VIEWPORT_EDITORS - {editor.tag for editor in theme}
    if unknown_editors:
        raise LookupError(f"viewport editors not found: {sorted(unknown_editors)}")

    canvas = tokens.hex("surface.viewport")
    panel = tokens.hex("surface.panel")
    space_count = 0
    for editor in theme:
        for space in editor.iterfind("*/space/*"):
            space_count += 1
            _apply(space, mapping.SPACE, tokens)
            if space.tag == "ThemeSpaceGradient":
                gradient = _find(space, "gradients/ThemeGradientColors")
                _set_color(gradient, "high_gradient", canvas)
                _set_color(gradient, "gradient", canvas)
            else:
                _set_color(space, "back", canvas if editor.tag in mapping.VIEWPORT_EDITORS else panel)

    if space_count == 0:
        raise LookupError("no editor space elements found")

    sidebars = _find(theme, "regions/ThemeRegions/sidebars/ThemeRegionsSidebars")
    _apply(sidebars, mapping.SIDEBARS, tokens)

    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode") + "\n"
