from __future__ import annotations

import bpy
from bpy.props import BoolProperty

from .declutter.groups import GROUPS

# Set by the add-on package so a checkbox change re-applies everything.
on_change = None


def _update(self, context) -> None:
    if on_change is not None:
        on_change()


class UIKitPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_sculpting: BoolProperty(name="Sculpting", default=True, update=_update)
    show_texture_painting: BoolProperty(name="Texture painting", default=True, update=_update)
    show_materials: BoolProperty(name="Materials and shader nodes", default=True, update=_update)
    show_rigging_animation: BoolProperty(name="Rigging and animation", default=False, update=_update)
    show_everything_else: BoolProperty(
        name="Everything else (rendering, physics, compositing, scripting)", default=False, update=_update
    )
    use_fonts: BoolProperty(name="Use Geist and JetBrains Mono fonts", default=True, update=_update)

    def draw(self, context) -> None:
        layout = self.layout
        layout.label(text="Show these features:")
        for group in GROUPS:
            layout.prop(self, f"show_{group.key}")
        layout.separator()
        layout.prop(self, "use_fonts")
        layout.label(text="Hidden workspaces return in new files when you turn a feature on.")
