from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from fontTools.ttLib import TTFont

OFL_FILES = ("OFL-Geist.txt", "OFL-JetBrainsMono.txt")


@dataclass(frozen=True)
class Bake:
    source: str
    output: str
    family: str
    # Unicode code point -> name of the alternate glyph that replaces the default.
    remap: dict


BAKES = (
    # one.ss09: footed one (its zero.ss09 is deliberately not used). I.ss05: serifed I.
    Bake("Geist-Variable.ttf", "GeistUIKit-Variable.ttf", "Geist UI Kit", {0x31: "one.ss09", 0x49: "I.ss05"}),
    # zero: slashed zero.
    Bake("JetBrainsMono-Regular.ttf", "JetBrainsMonoUIKit-Regular.ttf", "JetBrains Mono UI Kit", {0x30: "zero.zero"}),
)


def _rename(font: TTFont, family: str) -> None:
    names = font["name"]
    old_family = names.getDebugName(1)
    old_compact = old_family.replace(" ", "")
    new_compact = family.replace(" ", "")
    for record in list(names.names):
        text = record.toUnicode()
        if record.nameID == 6:
            # PostScript names have no spaces.
            if text.startswith(old_compact):
                text = new_compact + text[len(old_compact):]
        elif record.nameID == 3:
            text = text.replace(old_compact, new_compact)
        elif record.nameID in (1, 4, 16):
            text = text.replace(old_family, family, 1)
        else:
            continue
        names.setName(text, record.nameID, record.platformID, record.platEncID, record.langID)


def bake_font(source: Path, output: Path, bake: Bake) -> None:
    # Pointing the character map at the alternate glyph bakes the feature in without
    # touching any outline. recalcTimestamp=False keeps the output reproducible.
    font = TTFont(source, recalcTimestamp=False)
    glyphs = set(font.getGlyphOrder())
    for glyph in bake.remap.values():
        if glyph not in glyphs:
            raise KeyError(f"{source.name} has no glyph {glyph!r}")
    for table in font["cmap"].tables:
        for codepoint, glyph in bake.remap.items():
            if codepoint in table.cmap:
                table.cmap[codepoint] = glyph
    _rename(font, bake.family)
    font.save(output)


def build_fonts(root: Path) -> list:
    # Regenerate the baked fonts and copy the license texts next to them.
    source = root / "fonts" / "source"
    target = root / "blender" / "addon" / "fonts"
    target.mkdir(parents=True, exist_ok=True)
    written = []
    for bake in BAKES:
        bake_font(source / bake.source, target / bake.output, bake)
        written.append(target / bake.output)
    for name in OFL_FILES:
        shutil.copy2(source / name, target / name)
    return written
