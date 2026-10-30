from __future__ import annotations

import re
from pathlib import Path

from build.colors import to_hex, to_rgb
from build.freecad_mapping import ICONS, PARAMETERS, PREFERENCES
from build.tokens import Tokens

# The pack is committed (the Addon Manager installs straight from git), so the build
# rewrites colors in place. Every color is keyed by name, so rebuilding is idempotent.
PACK = Path("freecad") / "Zinc Dark"

_PARAMETER = re.compile(r'^([\w ]+): ".*"$')
_GROUP = re.compile(r'^\s*<FCParamGroup Name="([^"]+)">')
_COLOR = re.compile(r'^(\s*<FCUInt Name="([^"]+)" Value=")(\d+)("/>)$')
_COMMENT = re.compile(r"^(\s*)<!-- .* -->$")
_TAG = re.compile(r"<\w+\s[^<>]*>")
_CLASS = re.compile(r'\sclass="([^"]*)"')


def _yaml_name(shade: str) -> str:
    # "zinc-935" -> "Zinc935"
    family, number = shade.split("-")
    return family.capitalize() + number


def render_parameters(text: str, tokens: Tokens) -> str:
    used = {tokens.shade(name) for name in PARAMETERS.values()}
    families = list(dict.fromkeys(shade.split("-")[0] for shade in tokens.palette))
    ordered = sorted(used, key=lambda shade: (families.index(shade.split("-")[0]), int(shade.split("-")[1])))
    palette = [f'{_yaml_name(shade)}: "{to_hex(tokens.palette[shade])}"' for shade in ordered]

    lines = []
    seen = set()
    in_palette = False
    for line in text.splitlines():
        if line == "# Tailwind palette":
            in_palette = True
            lines += [line, *palette]
            continue
        if in_palette:
            in_palette = line != ""
            if in_palette:
                continue
        match = _PARAMETER.match(line)
        if match and match.group(1) in PARAMETERS:
            key = match.group(1)
            line = f'{key}: "@{_yaml_name(tokens.shade(PARAMETERS[key]))}"'
            seen.add(key)
        lines.append(line)

    missing = sorted(set(PARAMETERS) - seen)
    if missing:
        raise KeyError(f"parameters file is missing: {', '.join(missing)}")
    return "\n".join(lines) + "\n"


def render_preferences(text: str, tokens: Tokens) -> str:
    lines = []
    seen = set()
    groups = []
    for line in text.splitlines():
        if group := _GROUP.match(line):
            groups.append(group.group(1))
        elif line.strip() == "</FCParamGroup>":
            groups.pop()
        elif color := _COLOR.match(line):
            # Paths are relative to Root/BaseApp/Preferences.
            key = "/".join([*groups[3:], color.group(2)])
            if key in PREFERENCES:
                red, green, blue = to_rgb(tokens.resolve(PREFERENCES[key]))
                # FreeCAD packs colors as 0xRRGGBBAA; the existing alpha byte is kept.
                alpha = int(color.group(3)) & 0xFF
                value = red << 24 | green << 16 | blue << 8 | alpha
                line = f"{color.group(1)}{value}{color.group(4)}"
                if lines and (comment := _COMMENT.match(lines[-1])):
                    lines[-1] = f"{comment.group(1)}<!-- {tokens.shade(PREFERENCES[key])} -->"
                seen.add(key)
        lines.append(line)

    missing = sorted(set(PREFERENCES) - seen)
    if missing:
        raise KeyError(f"preferences file is missing: {', '.join(missing)}")
    return "\n".join(lines) + "\n"


def _paint(tag: str, tokens: Tokens) -> str:
    classes = _CLASS.search(tag)
    if classes is None:
        return tag
    for name in classes.group(1).split():
        attribute, slot = name.split("-", 1)
        if attribute not in ("stroke", "fill") or slot not in ICONS:
            raise KeyError(f"unknown icon class {name!r}")
        tag, count = re.subn(rf'\s{attribute}="[^"]*"', f' {attribute}="{to_hex(tokens.resolve(ICONS[slot]))}"', tag)
        if count != 1:
            raise KeyError(f"icon class {name!r} needs exactly one {attribute} attribute")
    return tag


def render_icon(text: str, tokens: Tokens) -> str:
    return _TAG.sub(lambda match: _paint(match.group(0), tokens), text)


def _rendered_files(root: Path, tokens: Tokens) -> dict[Path, str]:
    pack = root / PACK
    files = {
        pack / "parameters" / "Zinc Dark.yaml": render_parameters,
        pack / "Zinc Dark.cfg": render_preferences,
        **{path: render_icon for path in sorted([*pack.glob("icons/*.svg"), *pack.glob("zinc-glyphs/*.svg")])},
    }
    return {path: render(path.read_text(encoding="utf-8"), tokens) for path, render in files.items()}


def stale_freecad_files(root: Path, tokens: Tokens) -> list[Path]:
    return [path for path, text in _rendered_files(root, tokens).items() if path.read_text(encoding="utf-8") != text]


def build_freecad_pack(root: Path, tokens: Tokens) -> Path:
    for path, text in _rendered_files(root, tokens).items():
        path.write_text(text, encoding="utf-8", newline="\n")
    return root / PACK
