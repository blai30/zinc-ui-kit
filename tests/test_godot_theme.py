from pathlib import Path

from build.godot_theme import OUTPUT, generate_script
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")


def test_committed_script_matches_the_tokens():
    # Run `python -m build godot-theme` if this fails.
    assert (ROOT / OUTPUT).read_text(encoding="utf-8") == generate_script(TOKENS)


def test_colors_follow_the_roles():
    script = generate_script(TOKENS)
    assert f'"interface/theme/base_color": Color("{TOKENS.hex("surface.raised")}")' in script
    assert f'"interface/theme/accent_color": Color("{TOKENS.hex("accent.hover")}")' in script
