import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from build import blender_mapping as mapping
from build.blender_theme import generate_theme
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")
BASE_XML = (ROOT / "blender" / "theme" / "base_theme.xml").read_text(encoding="utf-8")
BASE = ET.fromstring(BASE_XML)
INTERFACE = "Theme/user_interface/ThemeUserInterface"
# The base theme has 18 editor spaces and 21 ThemeWidgetColors elements.
SPACE_COUNT = 18
WIDGET_COUNT = 21


def expected(base_element, name, role):
    # Role color with the base alpha kept, as the generator does.
    base_value = base_element.get(name)
    alpha = base_value[7:] if len(base_value) == 9 else ""
    return TOKENS.hex(role) + alpha


def attribute_paths(root):
    # Every (element path, attribute name) pair, with sibling indexes to keep paths unique.
    found = set()

    def walk(element, path):
        for name in element.attrib:
            found.add((path, name))
        for index, child in enumerate(element):
            walk(child, f"{path}/{child.tag}[{index}]")

    walk(root, root.tag)
    return found


@pytest.fixture(scope="module")
def theme():
    return ET.fromstring(generate_theme(BASE_XML, TOKENS))


def test_no_attribute_is_added_or_dropped(theme):
    assert attribute_paths(theme) == attribute_paths(ET.fromstring(BASE_XML))


def test_editor_border_uses_background_surface(theme):
    ui = theme.find("Theme/user_interface/ThemeUserInterface")
    assert ui.get("editor_border") == TOKENS.hex("surface.background")


def test_panel_back_keeps_base_alpha(theme):
    ui = theme.find("Theme/user_interface/ThemeUserInterface")
    assert ui.get("panel_back") == TOKENS.hex("surface.panel") + "ff"


def test_every_widget_is_flat_and_rounded(theme):
    widgets = theme.findall("Theme/user_interface/ThemeUserInterface/*/ThemeWidgetColors")
    assert len(widgets) == WIDGET_COUNT
    for widget in widgets:
        assert widget.get("show_shaded") == "FALSE"
        assert widget.get("shadetop") == "0"
        assert widget.get("shadedown") == "0"
        assert widget.get("roundness") == f"{TOKENS.radius['widget']:g}"


def test_widget_override_wins_over_generic_rule(theme):
    menu_back = theme.find("Theme/user_interface/ThemeUserInterface/wcol_menu_back/ThemeWidgetColors")
    regular = theme.find("Theme/user_interface/ThemeUserInterface/wcol_regular/ThemeWidgetColors")
    assert menu_back.get("inner") == TOKENS.hex("surface.raised") + "ff"
    assert regular.get("inner") == TOKENS.hex("surface.control") + "ff"


def test_state_fills_use_status_roles_and_keep_animation_colors(theme):
    path = "Theme/user_interface/ThemeUserInterface/wcol_state/ThemeWidgetStateColors"
    state = theme.find(path)
    base = ET.fromstring(BASE_XML).find(path)
    assert state.get("error") == TOKENS.hex("status.danger") + "ff"
    assert state.get("warning") == TOKENS.hex("status.warning") + "ff"
    assert state.get("success") == TOKENS.hex("status.success") + "ff"
    assert state.get("info") == TOKENS.hex("accent.pressed") + "ff"
    assert state.get("inner_key") == base.get("inner_key")


def test_viewport_editors_use_viewport_surface(theme):
    gradient = theme.find("Theme/view_3d/ThemeView3D/space/ThemeSpaceGradient/gradients/ThemeGradientColors")
    assert gradient.get("high_gradient") == TOKENS.hex("surface.viewport")
    assert gradient.get("gradient") == TOKENS.hex("surface.viewport")
    node_space = theme.find("Theme/node_editor/ThemeNodeEditor/space/ThemeSpaceGeneric")
    assert node_space.get("back") == TOKENS.hex("surface.viewport")


def test_panel_editors_use_panel_surface(theme):
    space = theme.find("Theme/properties/ThemeProperties/space/ThemeSpaceGeneric")
    assert space.get("back") == TOKENS.hex("surface.panel")


def test_header_keeps_base_alpha(theme):
    space = theme.find("Theme/properties/ThemeProperties/space/ThemeSpaceGeneric")
    assert space.get("header") == TOKENS.hex("surface.background") + "b3"


def test_missing_attribute_fails_loudly():
    broken = BASE_XML.replace('editor_border="#161616"', "")
    with pytest.raises(KeyError, match="editor_border"):
        generate_theme(broken, TOKENS)


def test_every_space_gets_space_roles():
    spaces = ET.fromstring(generate_theme(BASE_XML, TOKENS)).findall("Theme/*/*/space/*")
    base_spaces = BASE.findall("Theme/*/*/space/*")
    assert len(spaces) == len(base_spaces) == SPACE_COUNT
    for space, base_space in zip(spaces, base_spaces):
        for name, role in mapping.SPACE.items():
            assert space.get(name) == expected(base_space, name, role)
    assert all(len(space.get("header")) == 9 for space in spaces)


def test_every_widget_gets_widget_roles(theme):
    widgets = theme.findall(f"{INTERFACE}/*/ThemeWidgetColors")
    base_widgets = BASE.findall(f"{INTERFACE}/*/ThemeWidgetColors")
    assert len(widgets) == len(base_widgets) == WIDGET_COUNT
    for widget, base_widget in zip(widgets, base_widgets):
        for name in ("outline", "outline_sel", "inner_sel", "text", "text_sel"):
            assert widget.get(name) == expected(base_widget, name, mapping.WIDGET[name])


def test_widget_overrides_apply(theme):
    for slot, overrides in mapping.WIDGET_OVERRIDES.items():
        widget = theme.find(f"{INTERFACE}/{slot}/ThemeWidgetColors")
        base_widget = BASE.find(f"{INTERFACE}/{slot}/ThemeWidgetColors")
        for name, role in overrides.items():
            assert widget.get(name) == expected(base_widget, name, role)
    assert len(mapping.WIDGET_OVERRIDES) == 4


def test_sidebars_keep_base_alpha(theme):
    path = "Theme/regions/ThemeRegions/sidebars/ThemeRegionsSidebars"
    sidebars = theme.find(path)
    assert sidebars.get("back") == TOKENS.hex("surface.panel") + "00"
    assert sidebars.get("tab_back") == TOKENS.hex("surface.background") + "00"


def test_user_interface_roles_and_roundness(theme):
    interface = theme.find(INTERFACE)
    base_interface = BASE.find(INTERFACE)
    assert interface.get("panel_roundness") == f"{TOKENS.radius['panel']:g}" == "0.5"
    assert len(mapping.USER_INTERFACE) == 13
    # Tuple rules (explicit alpha) are covered by test_outlines_use_explicit_alpha.
    for name, role in mapping.USER_INTERFACE.items():
        if not isinstance(role, str):
            continue
        assert interface.get(name) == expected(base_interface, name, role)


def test_image_editor_uses_viewport_surface(theme):
    space = theme.find("Theme/image_editor/ThemeImageEditor/space/ThemeSpaceGeneric")
    assert space.get("back") == TOKENS.hex("surface.viewport") + BASE.find(
        "Theme/image_editor/ThemeImageEditor/space/ThemeSpaceGeneric"
    ).get("back")[7:]


def test_unknown_widget_override_fails_loudly(monkeypatch):
    monkeypatch.setitem(mapping.WIDGET_OVERRIDES, "wcol_bogus", {"inner": "surface.raised"})
    with pytest.raises(LookupError, match="wcol_bogus"):
        generate_theme(BASE_XML, TOKENS)


def test_unknown_viewport_editor_fails_loudly(monkeypatch):
    monkeypatch.setattr(mapping, "VIEWPORT_EDITORS", mapping.VIEWPORT_EDITORS | {"bogus_editor"})
    with pytest.raises(LookupError, match="bogus_editor"):
        generate_theme(BASE_XML, TOKENS)


def test_missing_state_slot_fails_loudly():
    broken = BASE_XML.replace("ThemeWidgetStateColors", "ThemeWidgetOtherColors")
    with pytest.raises(LookupError, match="ThemeWidgetStateColors"):
        generate_theme(broken, TOKENS)


def test_grid_uses_border_role_and_keeps_base_alpha(theme):
    view = theme.find("Theme/view_3d/ThemeView3D")
    base_view = BASE.find("Theme/view_3d/ThemeView3D")
    for name in ("grid", "grid_major"):
        assert view.get(name) == TOKENS.hex("border.default") + base_view.get(name)[7:]
    assert mapping.VIEW_3D.keys() == {"grid", "grid_major"}


def test_outlines_use_explicit_alpha(theme):
    ui = theme.find(INTERFACE)
    base_ui = BASE.find(INTERFACE)
    assert ui.get("editor_outline") == TOKENS.hex("text.strong") + "10"
    assert ui.get("panel_outline") == TOKENS.hex("text.strong") + "0d"
    assert ui.get("editor_outline_active") == base_ui.get("editor_outline_active")
