import json
from pathlib import Path

import pytest

from build.blender_package import render_manifest, stage_blender_addon

PROJECT_ROOT = Path(__file__).parent.parent

META = {
    "id": "uikit_zinc",
    "name": "UI Kit Zinc",
    "tagline": "Modern zinc and rose theme built on Tailwind colors",
    "version": "0.1.0",
    "maintainer": "Brian <brianlai30@outlook.com>",
}

EXPECTED = """\
schema_version = "1.0.0"
id = "uikit_zinc"
version = "0.1.0"
name = "UI Kit Zinc"
tagline = "Modern zinc and rose theme built on Tailwind colors"
maintainer = "Brian <brianlai30@outlook.com>"
type = "theme"
tags = ["Dark"]
blender_version_min = "5.2.0"
license = ["SPDX:GPL-3.0-or-later"]
"""


def test_render_manifest_exact_text():
    assert render_manifest(META) == EXPECTED


def test_render_manifest_escapes_special_characters():
    meta = {**META, "maintainer": 'Bri"an \\ <b@example.com>'}
    line = next(line for line in render_manifest(meta).splitlines() if line.startswith("maintainer = "))
    # A JSON string literal is also a valid TOML basic string.
    assert json.loads(line.removeprefix("maintainer = ")) == meta["maintainer"]


def test_render_manifest_names_missing_key():
    meta = {key: value for key, value in META.items() if key != "tagline"}
    with pytest.raises(KeyError, match="tagline"):
        render_manifest(meta)


def test_addon_manifest_has_type_and_tags():
    meta = {
        "id": "uikit_declutter",
        "version": "0.1.0",
        "name": "UI Kit Declutter",
        "tagline": "Declutters Blender",
        "maintainer": "Someone <someone@example.com>",
    }
    text = render_manifest(meta, "add-on", ("User Interface",))
    assert 'type = "add-on"' in text
    assert 'tags = ["User Interface"]' in text


def test_theme_manifest_is_unchanged_by_defaults():
    meta = {
        "id": "uikit_zinc",
        "version": "0.1.1",
        "name": "UI Kit Zinc",
        "tagline": "Modern zinc and rose theme built on Tailwind colors",
        "maintainer": "Someone <someone@example.com>",
    }
    text = render_manifest(meta)
    assert 'type = "theme"' in text
    assert 'tags = ["Dark"]' in text


def test_staged_addon_contains_the_package_and_a_manifest(tmp_path):
    stage = tmp_path / "stage"
    stage_blender_addon(PROJECT_ROOT, stage)
    assert (stage / "__init__.py").is_file()
    assert (stage / "declutter" / "groups.py").is_file()
    assert (stage / "fonts" / "GeistUIKit-Variable.ttf").is_file()
    assert (stage / "blender_manifest.toml").is_file()
    assert not (stage / "meta.json").exists()
    assert not list(stage.rglob("__pycache__"))
