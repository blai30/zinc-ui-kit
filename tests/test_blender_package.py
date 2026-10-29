import pytest

from build.blender_package import render_manifest

META = {
    "id": "uikit_graphite",
    "name": "UI Kit Graphite",
    "tagline": "Modern graphite and blue theme built on Tailwind zinc",
    "version": "0.1.0",
    "maintainer": "Brian <brianlai30@outlook.com>",
}

EXPECTED = """\
schema_version = "1.0.0"
id = "uikit_graphite"
version = "0.1.0"
name = "UI Kit Graphite"
tagline = "Modern graphite and blue theme built on Tailwind zinc"
maintainer = "Brian <brianlai30@outlook.com>"
type = "theme"
tags = ["Dark"]
blender_version_min = "5.2.0"
license = ["SPDX:GPL-3.0-or-later"]
"""


def test_render_manifest_exact_text():
    assert render_manifest(META) == EXPECTED


def test_render_manifest_escapes_special_characters():
    tomllib = pytest.importorskip("tomllib")
    meta = {**META, "maintainer": 'Bri"an \\ <b@example.com>'}
    parsed = tomllib.loads(render_manifest(meta))
    assert parsed["maintainer"] == meta["maintainer"]


def test_render_manifest_names_missing_key():
    meta = {key: value for key, value in META.items() if key != "tagline"}
    with pytest.raises(KeyError, match="tagline"):
        render_manifest(meta)
