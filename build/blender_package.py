from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

from build.blender_theme import generate_theme
from build.tokens import Tokens

MACOS_BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"
WINDOWS_BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"

MANIFEST_KEYS = ("id", "version", "name", "tagline", "maintainer")


def render_manifest(meta: dict[str, str]) -> str:
    missing = [key for key in MANIFEST_KEYS if key not in meta]
    if missing:
        raise KeyError(f"tokens meta is missing: {', '.join(missing)}")
    # json.dumps yields a valid TOML basic string.
    values = {key: json.dumps(meta[key]) for key in MANIFEST_KEYS}
    return f"""\
schema_version = "1.0.0"
id = {values["id"]}
version = {values["version"]}
name = {values["name"]}
tagline = {values["tagline"]}
maintainer = {values["maintainer"]}
type = "theme"
tags = ["Dark"]
blender_version_min = "5.2.0"
license = ["SPDX:GPL-3.0-or-later"]
"""


def find_blender() -> str:
    candidates = [os.environ.get("BLENDER_BIN"), shutil.which("blender"), MACOS_BLENDER, WINDOWS_BLENDER]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Blender not found. Set BLENDER_BIN to the Blender executable.")


def write_text(path: Path, text: str) -> None:
    # Explicit newline keeps output LF on Windows.
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def build_blender_theme(root: Path, tokens: Tokens) -> Path:
    blender = find_blender()
    stage = root / "dist" / "stage" / "blender-theme"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    base_xml = (root / "blender" / "theme" / "base_theme.xml").read_text(encoding="utf-8")
    write_text(stage / "graphite.xml", generate_theme(base_xml, tokens))
    write_text(stage / "blender_manifest.toml", render_manifest(tokens.meta))

    output = root / "dist"
    subprocess.run(
        [blender, "--command", "extension", "build", "--source-dir", str(stage), "--output-dir", str(output)],
        check=True,
    )
    return output / f"{tokens.meta['id']}-{tokens.meta['version']}.zip"
