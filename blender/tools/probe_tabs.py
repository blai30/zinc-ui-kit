# Run in a windowed Blender (a window opens briefly):
# BLENDER_USER_RESOURCES=/tmp/uikit-profile blender --factory-startup --python probe_tabs.py -- <path to blender/>
import sys

import bpy

sys.path.insert(0, sys.argv[sys.argv.index("--") + 1])

from addon.declutter import apply
from addon.declutter.groups import GROUPS


def available_tabs():
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "PROPERTIES":
                space = area.spaces.active
                tabs = []
                for item in space.bl_rna.properties["context"].enum_items:
                    try:
                        space.context = item.identifier
                        if space.context == item.identifier:
                            tabs.append(item.identifier)
                    except TypeError:
                        pass
                return tabs


def run():
    bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
    apply.apply_tabs({group.key: True for group in GROUPS})
    everything = available_tabs()
    apply.apply_tabs({group.key: group.default_shown for group in GROUPS})
    defaults = available_tabs()
    print("TABS_ALL", everything)
    print("TABS_DEFAULT", defaults)
    expected = ["SCENE", "RENDER", "OBJECT", "MODIFIER", "DATA", "MATERIAL", "TEXTURE"]
    print("PROBE", "OK" if defaults == expected and len(everything) > len(defaults) else "FAIL")
    bpy.ops.wm.quit_blender()


bpy.app.timers.register(run, first_interval=2.0)
