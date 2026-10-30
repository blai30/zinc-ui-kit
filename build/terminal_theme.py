from __future__ import annotations

import json
from pathlib import Path

from build.colors import to_hex
from build.tokens import Tokens

GHOSTTY_OUTPUT = Path("ghostty") / "Zinc"
WINDOWS_TERMINAL_OUTPUT = Path("windows-terminal") / "Zinc.json"

# ANSI colors 0-15 as role or palette entry. Normal colors use 400 shades, which read
# better on dark gray than the 500s; bright black stays light enough for comments and
# shell autosuggestions.
ANSI = [
    ("black", "zinc-800"),
    ("red", "red-400"),
    ("green", "green-400"),
    ("yellow", "yellow-400"),
    ("blue", "blue-400"),
    ("purple", "fuchsia-400"),
    ("cyan", "cyan-400"),
    ("white", "zinc-300"),
    ("brightBlack", "zinc-500"),
    ("brightRed", "red-300"),
    ("brightGreen", "green-300"),
    ("brightYellow", "yellow-300"),
    ("brightBlue", "blue-300"),
    ("brightPurple", "fuchsia-300"),
    ("brightCyan", "cyan-300"),
    ("brightWhite", "text.strong"),
]

BACKGROUND = "surface.viewport"
FOREGROUND = "text.primary"
CURSOR = "rose-300"
SELECTION = "zinc-700"
SELECTION_TEXT = "text.strong"


def _hex(tokens: Tokens, name: str) -> str:
    return to_hex(tokens.resolve(name))


def generate_windows_terminal(tokens: Tokens) -> str:
    scheme = {
        "name": "Zinc",
        "background": _hex(tokens, BACKGROUND),
        "foreground": _hex(tokens, FOREGROUND),
        "cursorColor": _hex(tokens, CURSOR),
        "selectionBackground": _hex(tokens, SELECTION),
        **{key: _hex(tokens, name) for key, name in ANSI},
    }
    return json.dumps({"schemes": [scheme]}, indent=2) + "\n"


def generate_ghostty(tokens: Tokens) -> str:
    lines = [f"palette = {index}={_hex(tokens, name)}" for index, (_, name) in enumerate(ANSI)]
    lines += [
        f"background = {_hex(tokens, BACKGROUND)}",
        f"foreground = {_hex(tokens, FOREGROUND)}",
        f"cursor-color = {_hex(tokens, CURSOR)}",
        f"cursor-text = {_hex(tokens, BACKGROUND)}",
        f"selection-background = {_hex(tokens, SELECTION)}",
        f"selection-foreground = {_hex(tokens, SELECTION_TEXT)}",
    ]
    return "\n".join(lines) + "\n"


def build_terminal_themes(root: Path, tokens: Tokens) -> list[Path]:
    outputs = [
        (root / WINDOWS_TERMINAL_OUTPUT, generate_windows_terminal(tokens)),
        (root / GHOSTTY_OUTPUT, generate_ghostty(tokens)),
    ]
    for path, text in outputs:
        path.parent.mkdir(exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    return [path for path, _ in outputs]
