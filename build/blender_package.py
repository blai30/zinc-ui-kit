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


def render_manifest(meta: dict[str, str], package_type: str = "theme", tags: tuple = ("Dark",)) -> str:
    missing = [key for key in MANIFEST_KEYS if key not in meta]
    if missing:
        raise KeyError(f"package meta is missing: {', '.join(missing)}")
    # json.dumps yields valid TOML basic strings.
    values = {key: json.dumps(meta[key]) for key in MANIFEST_KEYS}
    return f"""\
schema_version = "1.0.0"
id = {values["id"]}
version = {values["version"]}
name = {values["name"]}
tagline = {values["tagline"]}
maintainer = {values["maintainer"]}
type = {json.dumps(package_type)}
tags = {json.dumps(list(tags))}
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


def _build_extension(blender: str, stage: Path, output: Path) -> None:
    subprocess.run(
        [blender, "--command", "extension", "build", "--source-dir", str(stage), "--output-dir", str(output)],
        check=True,
    )


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
    _build_extension(blender, stage, output)
    return output / f"{tokens.meta['id']}-{tokens.meta['version']}.zip"


def stage_blender_addon(root: Path, stage: Path) -> dict[str, str]:
    source = root / "blender" / "addon"
    meta = json.loads((source / "meta.json").read_text(encoding="utf-8"))
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(source, stage, ignore=shutil.ignore_patterns("__pycache__", "meta.json"))
    write_text(stage / "blender_manifest.toml", render_manifest(meta, "add-on", ("User Interface",)))
    return meta


def build_blender_addon(root: Path) -> Path:
    blender = find_blender()
    output = root / "dist"
    meta = stage_blender_addon(root, output / "stage" / "blender-addon")
    _build_extension(blender, output / "stage" / "blender-addon", output)
    return output / f"{meta['id']}-{meta['version']}.zip"
