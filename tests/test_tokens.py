import json
from pathlib import Path

import pytest

from build.colors import parse_oklch
from build.tokens import load_tokens

TOKENS_PATH = Path(__file__).parent.parent / "tokens" / "tokens.json"


def test_palette_is_flattened_to_family_shade_names():
    tokens = load_tokens(TOKENS_PATH)
    assert tokens.palette["zinc-900"] == parse_oklch("oklch(21% 0.006 285.885)")


def test_derived_shades_sit_between_their_endpoints():
    tokens = load_tokens(TOKENS_PATH)
    darkest = tokens.palette["zinc-950"].lightness
    lightest = tokens.palette["zinc-900"].lightness
    assert darkest < tokens.palette["zinc-935"].lightness < tokens.palette["zinc-915"].lightness < lightest


def test_surface_stack_gets_lighter_in_order():
    tokens = load_tokens(TOKENS_PATH)
    order = ["viewport", "background", "panel", "raised", "control"]
    lightness = [tokens.color(f"surface.{name}").lightness for name in order]
    assert lightness == sorted(lightness)
    assert len(set(lightness)) == len(lightness)


def test_hex_resolves_a_role():
    tokens = load_tokens(TOKENS_PATH)
    assert tokens.hex("text.strong") == "#fafafa"


def test_unknown_role_raises():
    tokens = load_tokens(TOKENS_PATH)
    with pytest.raises(KeyError, match="surface.missing"):
        tokens.hex("surface.missing")


def test_derived_color_pointing_at_missing_palette_entry_fails_to_load(tmp_path):
    data = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    data["derived"]["zinc-935"]["from"] = "zinc-999"
    broken = tmp_path / "tokens.json"
    broken.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="zinc-935"):
        load_tokens(broken)


def test_role_pointing_at_missing_palette_entry_fails_to_load(tmp_path):
    data = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    data["roles"]["accent.base"] = "blue-123"
    broken = tmp_path / "tokens.json"
    broken.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="blue-123"):
        load_tokens(broken)
