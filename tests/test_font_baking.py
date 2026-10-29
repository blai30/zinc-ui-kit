from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from build.fonts import BAKES, Bake, bake_font

ROOT = Path(__file__).parent.parent
SOURCE = ROOT / "fonts" / "source"


def bake_by_output(name):
    return next(bake for bake in BAKES if bake.output == name)


@pytest.fixture(scope="module")
def geist(tmp_path_factory):
    bake = bake_by_output("GeistUIKit-Variable.ttf")
    out = tmp_path_factory.mktemp("baked") / bake.output
    bake_font(SOURCE / bake.source, out, bake)
    return TTFont(out), TTFont(SOURCE / bake.source)


@pytest.fixture(scope="module")
def jetbrains(tmp_path_factory):
    bake = bake_by_output("JetBrainsMonoUIKit-Regular.ttf")
    out = tmp_path_factory.mktemp("baked") / bake.output
    bake_font(SOURCE / bake.source, out, bake)
    return TTFont(out), TTFont(SOURCE / bake.source)


def test_geist_one_and_i_use_the_alternates(geist):
    baked, _ = geist
    cmap = baked.getBestCmap()
    assert cmap[0x31] == "one.ss09"
    assert cmap[0x49] == "I.ss05"


def test_geist_leaves_everything_else_alone(geist):
    # The default zero and l stay as designed.
    baked, original = geist
    for codepoint in (0x30, 0x6C, 0x61, 0x4F, 0x69):
        assert baked.getBestCmap()[codepoint] == original.getBestCmap()[codepoint]


def test_jetbrains_zero_is_slashed_and_the_rest_is_unchanged(jetbrains):
    baked, original = jetbrains
    assert baked.getBestCmap()[0x30] == "zero.zero"
    for codepoint in (0x31, 0x49, 0x6C):
        assert baked.getBestCmap()[codepoint] == original.getBestCmap()[codepoint]


def test_families_are_renamed(geist, jetbrains):
    assert geist[0]["name"].getDebugName(1) == "Geist UI Kit"
    assert jetbrains[0]["name"].getDebugName(1) == "JetBrains Mono UI Kit"
    assert geist[0]["name"].getDebugName(6).startswith("GeistUIKit")
    assert jetbrains[0]["name"].getDebugName(6).startswith("JetBrainsMonoUIKit")


def test_original_family_name_is_not_left_in_the_family_records(geist, jetbrains):
    for baked, original in (geist, jetbrains):
        original_family = original["name"].getDebugName(1)
        for record in baked["name"].names:
            if record.nameID in (1, 16):
                assert record.toUnicode() != original_family


def test_metrics_and_glyph_count_are_preserved(geist, jetbrains):
    for baked, original in (geist, jetbrains):
        assert baked.getGlyphOrder() == original.getGlyphOrder()
        assert baked["hmtx"].metrics == original["hmtx"].metrics


def test_variable_axes_survive(geist, jetbrains):
    assert "fvar" in geist[0]
    assert "fvar" not in jetbrains[0]


def test_output_is_deterministic(tmp_path):
    bake = bake_by_output("JetBrainsMonoUIKit-Regular.ttf")
    first = tmp_path / "first.ttf"
    second = tmp_path / "second.ttf"
    bake_font(SOURCE / bake.source, first, bake)
    bake_font(SOURCE / bake.source, second, bake)
    assert first.read_bytes() == second.read_bytes()


def test_missing_glyph_fails_loudly(tmp_path):
    bake = Bake("JetBrainsMono-Regular.ttf", "x.ttf", "JetBrains Mono UI Kit", {0x30: "no.such.glyph"})
    with pytest.raises(KeyError, match="no.such.glyph"):
        bake_font(SOURCE / bake.source, tmp_path / "x.ttf", bake)


def test_committed_fonts_match_a_fresh_bake(tmp_path):
    for bake in BAKES:
        fresh = tmp_path / bake.output
        bake_font(SOURCE / bake.source, fresh, bake)
        committed = ROOT / "blender" / "addon" / "fonts" / bake.output
        assert committed.read_bytes() == fresh.read_bytes(), f"{bake.output} is stale: run python -m build fonts"


def test_licenses_are_copied_unchanged():
    for name in ("OFL-Geist.txt", "OFL-JetBrainsMono.txt"):
        assert (ROOT / "blender" / "addon" / "fonts" / name).read_bytes() == (SOURCE / name).read_bytes()
