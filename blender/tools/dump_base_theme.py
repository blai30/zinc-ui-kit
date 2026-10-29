# Run inside Blender: blender -b --factory-startup --python dump_base_theme.py -- <output.xml>
import sys

import _rna_xml
import bpy

output = sys.argv[sys.argv.index("--") + 1]
_rna_xml.xml_file_write(
    bpy.context,
    output,
    (("preferences.themes[0]", "Theme"), ("preferences.ui_styles[0]", "ThemeStyle")),
)
