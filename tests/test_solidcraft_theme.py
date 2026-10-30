import json
import re
from pathlib import Path

from build.solidcraft_theme import OUTPUT, generate_theme
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")


def test_committed_theme_matches_the_tokens():
    # Run `python -m build solidcraft-theme` if this fails.
    assert (ROOT / OUTPUT).read_text(encoding="utf-8") == generate_theme(TOKENS)


def test_every_color_is_hex_with_optional_alpha():
    colors = json.loads(generate_theme(TOKENS))["colors"]
    values = [item for value in colors.values() for item in (value if isinstance(value, list) else [value])]
    assert all(re.fullmatch(r"#[0-9a-f]{6}([0-9a-f]{2})?", value) for value in values)


def test_accent_and_surfaces_follow_the_roles():
    colors = json.loads(generate_theme(TOKENS))["colors"]
    assert colors["accent"] == TOKENS.hex("accent.base")
    assert colors["panel"] == TOKENS.hex("surface.panel")
    assert colors["viewport_top"] == TOKENS.hex("surface.raised")
    assert colors["app_bar_hover"] == TOKENS.hex("text.strong") + "14"
