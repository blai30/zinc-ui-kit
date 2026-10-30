import json
import re
from pathlib import Path

from build.terminal_theme import (
    GHOSTTY_OUTPUT,
    WINDOWS_TERMINAL_OUTPUT,
    generate_ghostty,
    generate_windows_terminal,
)
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")

NAMES = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]
ANSI_KEYS = NAMES + [f"bright{name.capitalize()}" for name in NAMES]


def _scheme() -> dict[str, str]:
    (scheme,) = json.loads(generate_windows_terminal(TOKENS))["schemes"]
    return scheme


def test_committed_themes_match_the_tokens():
    # Run `python -m build terminal-themes` if this fails.
    assert (ROOT / WINDOWS_TERMINAL_OUTPUT).read_text(encoding="utf-8") == generate_windows_terminal(TOKENS)
    assert (ROOT / GHOSTTY_OUTPUT).read_text(encoding="utf-8") == generate_ghostty(TOKENS)


def test_windows_terminal_scheme_defines_every_color():
    # Fragments drop schemes that miss any of the 16 colors.
    scheme = _scheme()
    assert set(ANSI_KEYS) <= scheme.keys()
    assert all(re.fullmatch(r"#[0-9a-f]{6}", value) for key, value in scheme.items() if key != "name")


def test_ghostty_theme_follows_the_roles():
    settings = dict(line.split(" = ", 1) for line in generate_ghostty(TOKENS).splitlines() if not line.startswith("palette"))
    assert settings["background"] == TOKENS.hex("surface.viewport")
    assert settings["foreground"] == TOKENS.hex("text.primary")
    assert settings["cursor-color"] == TOKENS.hex("accent.base")


def test_both_terminals_share_the_palette():
    palette = [line.removeprefix("palette = ") for line in generate_ghostty(TOKENS).splitlines() if line.startswith("palette")]
    scheme = _scheme()
    assert palette == [f"{index}={scheme[key]}" for index, key in enumerate(ANSI_KEYS)]
