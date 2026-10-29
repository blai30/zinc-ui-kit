# Run inside Blender:
# blender -b --factory-startup --python verify_theme.py --python-exit-code 1 -- <theme.xml> <editor_border hex> <panel_roundness>
import sys

import _rna_xml
import bpy

path, border_hex, roundness = sys.argv[sys.argv.index("--") + 1 :][:3]

_rna_xml.xml_file_run(
    bpy.context,
    path,
    (("preferences.themes[0]", "Theme"), ("preferences.ui_styles[0]", "ThemeStyle")),
)

interface = bpy.context.preferences.themes[0].user_interface
actual = "#" + "".join(f"{round(channel * 255):02x}" for channel in interface.editor_border[:3])
assert actual == border_hex, f"editor_border {actual} != {border_hex}"
assert abs(interface.panel_roundness - float(roundness)) < 1e-6, interface.panel_roundness
print("THEME OK")
