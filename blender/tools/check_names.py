# Run inside Blender:
# blender -b --factory-startup --python check_names.py --python-exit-code 1 -- <path to blender/addon>
import sys

import bpy

sys.path.insert(0, sys.argv[sys.argv.index("--") + 1])

from declutter.groups import GROUPS

tab_properties = {prop.identifier for prop in bpy.types.SpaceProperties.bl_rna.properties}
workspace_names = {workspace.name for workspace in bpy.data.workspaces}

problems = []
for group in GROUPS:
    for tab in group.tabs:
        if f"show_properties_{tab}" not in tab_properties:
            problems.append(f"{group.key}: no SpaceProperties.show_properties_{tab}")
    for panel in group.panels:
        if not hasattr(bpy.types, panel):
            problems.append(f"{group.key}: no panel class {panel}")
    for workspace in group.workspaces:
        if workspace not in workspace_names:
            problems.append(f"{group.key}: no workspace {workspace!r}")

# Every child of a targeted panel (recursively) must be targeted too.
targeted = {panel for group in GROUPS for panel in group.panels}
parents = {}
for name in dir(bpy.types):
    cls = getattr(bpy.types, name)
    if isinstance(cls, type) and issubclass(cls, bpy.types.Panel) and getattr(cls, "bl_parent_id", ""):
        parents[name] = cls.bl_parent_id
for name in parents:
    ancestor = parents[name]
    while ancestor:
        if ancestor in targeted and name not in targeted:
            problems.append(f"child panel {name} of targeted {ancestor} is not in any group")
            break
        ancestor = parents.get(ancestor)

if problems:
    raise SystemExit("\n".join(problems))
print("NAMES OK")
