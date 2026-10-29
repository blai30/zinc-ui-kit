from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Group:
    key: str
    label: str
    default_shown: bool
    # SpaceProperties show_properties_<tab> names.
    tabs: tuple[str, ...] = ()
    # Built-in panel class names under bpy.types. Children are listed after their parent.
    panels: tuple[str, ...] = ()
    workspaces: tuple[str, ...] = ()


GROUPS = (
    Group("sculpting", "Sculpting", True, workspaces=("Sculpting",)),
    Group("texture_painting", "Texture painting", True, tabs=("texture",), workspaces=("Texture Paint",)),
    Group("materials", "Materials and shader nodes", True, tabs=("material",), workspaces=("Shading",)),
    Group(
        "rigging_animation",
        "Rigging and animation",
        False,
        tabs=("bone", "bone_constraints"),
        panels=("OBJECT_PT_animation", "OBJECT_PT_motion_paths", "OBJECT_PT_motion_paths_display"),
        workspaces=("Animation",),
    ),
    Group(
        "everything_else",
        "Everything else (rendering, physics, compositing, scripting)",
        False,
        tabs=("tool", "world", "collection", "output", "view_layer", "constraints", "particles", "physics", "effects"),
        panels=(
            "OBJECT_PT_relations",
            "OBJECT_PT_collections",
            "OBJECT_PT_instancing",
            "OBJECT_PT_instancing_size",
            "OBJECT_PT_lineart",
            "OBJECT_PT_custom_props",
        ),
        workspaces=("Rendering", "Compositing", "Geometry Nodes", "Scripting"),
    ),
)
