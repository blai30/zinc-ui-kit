# Run inside Blender:
# blender -b --factory-startup --python smoke_addon.py --python-exit-code 1 -- <path to blender/>
import sys

import bpy

sys.path.insert(0, sys.argv[sys.argv.index("--") + 1])

import addon
from addon import font_settings
from addon.declutter import apply
from addon.declutter.groups import GROUPS

all_off = {group.key: False for group in GROUPS}
all_on = {group.key: True for group in GROUPS}
panel_names = [name for group in GROUPS for name in group.panels]
workspace_names = [name for group in GROUPS for name in group.workspaces]

# Panels disappear when their group is off and return when it is on.
apply.apply_panels(all_off)
assert not any(hasattr(bpy.types, name) for name in panel_names), "panels still registered"
apply.apply_panels(all_on)
assert all(hasattr(bpy.types, name) for name in panel_names), "panels not restored"

# Restoring twice is harmless and leaves every panel registered.
apply.apply_panels(all_off)
apply.restore_panels()
apply.restore_panels()
assert all(hasattr(bpy.types, name) for name in panel_names), "restore_panels failed"

# Restoring a panel that something else already re-registered does not raise.
apply.apply_panels(all_off)
bpy.utils.register_class(apply._removed_panels["OBJECT_PT_relations"])
apply.restore_panels()
assert all(hasattr(bpy.types, name) for name in panel_names), "restore after external register failed"
assert not apply._removed_panels

# Only the unwanted workspaces are removed.
apply.apply_workspaces(all_off)
remaining = {workspace.name for workspace in bpy.data.workspaces}
assert not remaining & set(workspace_names), remaining
assert {"Layout", "Modeling", "UV Editing"} <= remaining, remaining

# Fonts are set, then restored to the default.
view = bpy.context.preferences.view
font_settings.apply_fonts(addon.FONT_DIR)
assert view.font_path_ui.endswith("GeistUIKit-Variable.ttf"), view.font_path_ui
assert view.font_path_ui_mono.endswith("JetBrainsMonoUIKit-Regular.ttf"), view.font_path_ui_mono
font_settings.restore_fonts()
assert view.font_path_ui == "" and view.font_path_ui_mono == ""

# A path left behind by an older version of this add-on (a file that no longer
# exists in its own font folder) counts as the default font, not the user's choice.
view.font_path_ui = str(addon.FONT_DIR / "Geist-Variable.ttf")
view.font_path_ui_mono = str(addon.FONT_DIR / "JetBrainsMono-Regular.ttf")
font_settings.apply_fonts(addon.FONT_DIR)
font_settings.restore_fonts()
assert view.font_path_ui == "" and view.font_path_ui_mono == "", (view.font_path_ui, view.font_path_ui_mono)

# A font the user picked elsewhere is restored untouched.
view.font_path_ui = "/tmp/their-own-font.ttf"
font_settings.apply_fonts(addon.FONT_DIR)
font_settings.restore_fonts()
assert view.font_path_ui == "/tmp/their-own-font.ttf", view.font_path_ui
view.font_path_ui = ""

# The add-on registers and unregisters cleanly, with a checkbox per group.
addon.register()
properties = {prop.identifier for prop in addon.preferences.UIKitPreferences.bl_rna.properties}
for group in GROUPS:
    assert f"show_{group.key}" in properties, group.key
assert "use_fonts" in properties
addon.unregister()
assert all(hasattr(bpy.types, name) for name in panel_names), "unregister left panels removed"
print("SMOKE OK")
