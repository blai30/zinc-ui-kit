from __future__ import annotations

import re

from build.tokens import Tokens

_PLACEHOLDER = re.compile(r"%([a-z]+\.[a-z]+)%")

# Blender roundness is a 0..1 fraction. QSS needs pixels, taken against a 16 px control.
RADIUS_BASIS = 16


def render_qss(template: str, tokens: Tokens) -> str:
    def replace(match: re.Match) -> str:
        name = match.group(1)
        if name.startswith("radius."):
            return f"{round(tokens.radius[name.split('.', 1)[1]] * RADIUS_BASIS)}px"
        return tokens.hex(name)

    return _PLACEHOLDER.sub(replace, template)
