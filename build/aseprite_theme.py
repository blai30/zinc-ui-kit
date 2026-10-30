from __future__ import annotations

import json
import shutil
import zipfile
import xml.etree.ElementTree as ElementTree
from pathlib import Path

from build.aseprite_mapping import COLORS, FONT_SIZES, PARTS, STYLE_ATTRIBUTES
from build.aseprite_sheet import Placement, pack, render_sheet
from build.colors import to_hex
from build.tokens import Tokens

SOURCE = Path("aseprite")
# The font and its license are shared with the Blender add-on.
FONT_SOURCE = Path("blender") / "addon" / "fonts"
FONT_FILE = "GeistUIKit-Variable.ttf"
FONT_FILES = (FONT_FILE, "OFL-Geist.txt")
LICENSE_FILES = ("LICENSE-aseprite-theme.txt", "LICENSE-lucide.txt")

# The stock theme is drawn at 1x for 200% screen scaling. This one is drawn at 2x for 100%.
SCALE = 2
# Style and layer attributes measured in pixels.
GEOMETRY = {
    "border", "border-top", "border-left", "border-right", "border-bottom",
    "padding", "padding-top", "padding-left", "padding-right", "padding-bottom",
    "margin-top", "margin-left", "margin-right", "margin-bottom",
    "width", "height", "minwidth", "gap-rows", "gap-columns", "x", "y",
}

SHEET_DATA = """\
<?xml version="1.0" encoding="utf-8"?>
<sprite>
  <slices theme="theme.xml" />
</sprite>
"""


def _scaled(value: str) -> str:
    return str(int(value) * SCALE)


def _part_element(name: str, placement: Placement) -> ElementTree.Element:
    part = placement.part
    attributes = {"id": name, "x": str(placement.x), "y": str(placement.y)}
    if part.slices:
        attributes.update(zip(("w1", "w2", "w3", "h1", "h2", "h3"), map(str, part.slices)))
    else:
        attributes.update(w=str(part.width), h=str(part.height))
    if part.focus:
        attributes.update(focusx=str(part.focus[0]), focusy=str(part.focus[1]))
    return ElementTree.Element("part", attributes)


def generate_theme(base_text: str, tokens: Tokens, placements: dict[str, Placement], name: str) -> str:
    theme = ElementTree.fromstring(base_text)
    theme.set("name", name)
    theme.set("screenscaling", "1")
    theme.set("uiscaling", "1")

    fonts = theme.find("fonts")
    fonts.clear()
    ElementTree.SubElement(fonts, "font", {"name": "Geist UI Kit", "type": "truetype", "file": FONT_FILE, "antialias": "true"})
    for font_id, size in FONT_SIZES.items():
        ElementTree.SubElement(fonts, "font", {"id": font_id, "font": "Geist UI Kit", "size": str(size)})
    fonts.find("font[@id='mini']").set("mnemonics", "off")

    for dimension in theme.find("dimensions"):
        dimension.set("value", _scaled(dimension.get("value")))

    base_colors = {color.get("id") for color in theme.find("colors")}
    missing = sorted(base_colors - set(COLORS))
    if missing:
        raise KeyError(f"No mapping for theme colors: {', '.join(missing)}")
    for color in theme.find("colors"):
        color.set("value", to_hex(tokens.resolve(COLORS[color.get("id")])))
        color.attrib.pop("new", None)

    base_parts = {part.get("id") for part in theme.find("parts")}
    missing = sorted(base_parts - set(placements))
    if missing:
        raise KeyError(f"No drawing for theme parts: {', '.join(missing)}")
    parts = theme.find("parts")
    parts.clear()
    for part_name in sorted(placements):
        parts.append(_part_element(part_name, placements[part_name]))

    for style in theme.find("styles"):
        for element in style.iter():
            for attribute in GEOMETRY & set(element.attrib):
                element.set(attribute, _scaled(element.get(attribute)))
        # Hide the embossed shadow under disabled text. The layer stays so the idle text
        # color doesn't show through for the disabled state.
        for layer in style.iter("text"):
            if layer.get("color") == "background" and layer.get("state") == "disabled":
                layer.set("color", "none")
        style.attrib.update(STYLE_ATTRIBUTES.get(style.get("id"), {}))

    ElementTree.indent(theme, space="    ")
    return '<?xml version="1.0" encoding="utf-8" ?>\n' + ElementTree.tostring(theme, encoding="unicode") + "\n"


def _write_text(path: Path, text: str) -> None:
    # Explicit newline keeps output LF on Windows.
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def stage_aseprite_theme(root: Path, tokens: Tokens, stage: Path) -> dict:
    source = root / SOURCE
    package = json.loads((source / "package.json").read_text(encoding="utf-8"))
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    placements, height = pack(PARTS, tokens)
    (stage / "sheet.png").write_bytes(render_sheet(placements, height, tokens))
    base = (source / "base_theme.xml").read_text(encoding="utf-8")
    _write_text(stage / "theme.xml", generate_theme(base, tokens, placements, package["displayName"]))
    _write_text(stage / "sheet.aseprite-data", SHEET_DATA)
    shutil.copy2(source / "package.json", stage / "package.json")
    for name in FONT_FILES:
        shutil.copy2(root / FONT_SOURCE / name, stage / name)
    for name in LICENSE_FILES:
        shutil.copy2(source / name, stage / name)
    return package


def build_aseprite_theme(root: Path, tokens: Tokens, output: Path) -> Path:
    stage = output / "stage" / "aseprite-theme"
    package = stage_aseprite_theme(root, tokens, stage)
    path = output / f"{package['name']}-{package['version']}.aseprite-extension"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(stage.rglob("*")):
            if file.is_file():
                archive.write(file, file.relative_to(stage).as_posix())
    return path
