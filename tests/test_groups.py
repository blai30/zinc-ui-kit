from declutter.groups import GROUPS

ALWAYS_VISIBLE_TABS = {"scene", "render", "object", "modifiers", "data"}
ALWAYS_VISIBLE_WORKSPACES = {"Layout", "Modeling", "UV Editing"}


def test_group_keys_are_unique():
    keys = [group.key for group in GROUPS]
    assert len(keys) == len(set(keys))


def test_no_target_belongs_to_two_groups():
    for field in ("tabs", "panels", "workspaces"):
        names = [name for group in GROUPS for name in getattr(group, field)]
        assert len(names) == len(set(names)), field


def test_defaults_match_the_spec():
    defaults = {group.key: group.default_shown for group in GROUPS}
    assert defaults == {
        "sculpting": True,
        "texture_painting": True,
        "materials": True,
        "rigging_animation": False,
        "everything_else": False,
    }


def test_always_visible_tabs_and_workspaces_are_never_assigned():
    tabs = {name for group in GROUPS for name in group.tabs}
    workspaces = {name for group in GROUPS for name in group.workspaces}
    assert not tabs & ALWAYS_VISIBLE_TABS
    assert not workspaces & ALWAYS_VISIBLE_WORKSPACES


def test_panel_names_are_blender_panel_class_names():
    for group in GROUPS:
        for name in group.panels:
            assert "_PT_" in name, name


def test_known_child_panels_are_listed_after_their_parents():
    panels = [name for group in GROUPS for name in group.panels]
    for parent, child in (
        ("OBJECT_PT_instancing", "OBJECT_PT_instancing_size"),
        ("OBJECT_PT_motion_paths", "OBJECT_PT_motion_paths_display"),
    ):
        assert panels.index(parent) < panels.index(child)
        group_of = {name: group.key for group in GROUPS for name in group.panels}
        assert group_of[parent] == group_of[child]


def test_rigging_group_owns_the_animation_panels():
    rigging = next(group for group in GROUPS if group.key == "rigging_animation")
    assert {"OBJECT_PT_animation", "OBJECT_PT_motion_paths"} <= set(rigging.panels)
    assert {"bone", "bone_constraints"} <= set(rigging.tabs)
