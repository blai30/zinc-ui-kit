from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

from build.krita_qss import render_qss
from build.krita_scheme import generate_scheme
from build.tokens import Tokens

DESCRIPTOR = """\
[Desktop Entry]
Type=Service
ServiceTypes=Krita/PythonPlugin
X-KDE-Library={id}
X-Python-2-Compatible=false
Name={name}
Comment={comment}
"""

# The font and its license are shared with the Blender add-on.
FONT_SOURCE = Path("blender") / "addon" / "fonts"
FONT_FILES = ("GeistUIKit-Variable.ttf", "OFL-Geist.txt")


def _write_text(path: Path, text: str) -> None:
    # Explicit newline keeps output LF on Windows.
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def stage_krita_plugin(root: Path, tokens: Tokens, stage: Path) -> dict:
    source = root / "krita" / "plugin"
    meta = json.loads((source / "meta.json").read_text(encoding="utf-8"))
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    package = stage / meta["id"]
    shutil.copytree(source / meta["id"], package, ignore=shutil.ignore_patterns("__pycache__"))
    assets = package / "assets"
    assets.mkdir(exist_ok=True)

    base = (root / "krita" / "theme" / "base.colors").read_text(encoding="utf-8")
    template = (root / "krita" / "theme" / "style.qss.template").read_text(encoding="utf-8")
    _write_text(assets / "UIKitGraphite.colors", generate_scheme(base, tokens))
    _write_text(assets / "style.qss", render_qss(template, tokens))
    for name in FONT_FILES:
        shutil.copy2(root / FONT_SOURCE / name, assets / name)

    _write_text(stage / f"{meta['id']}.desktop", DESCRIPTOR.format(**meta))
    return meta


def build_krita_plugin(root: Path, tokens: Tokens, output: Path) -> Path:
    stage = output / "stage" / "krita-plugin"
    meta = stage_krita_plugin(root, tokens, stage)
    path = output / f"{meta['id']}-{meta['version']}.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(stage.rglob("*")):
            if file.is_file():
                archive.write(file, file.relative_to(stage).as_posix())
    return path
