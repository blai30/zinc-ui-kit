from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from build.colors import Oklch, mix, parse_oklch, to_hex


@dataclass(frozen=True)
class Tokens:
    palette: dict[str, Oklch]
    roles: dict[str, str]
    radius: dict[str, float]
    meta: dict[str, str]

    def color(self, role: str) -> Oklch:
        return self.palette[self.roles[role]]

    def hex(self, role: str) -> str:
        return to_hex(self.color(role))

    def resolve(self, name: str) -> Oklch:
        # A role ("accent.base") or a palette entry ("violet-400").
        return self.color(name) if name in self.roles else self.palette[name]

    def shade(self, name: str) -> str:
        # Palette entry name behind a role or palette entry.
        return self.roles.get(name, name)


def load_tokens(path: Path) -> Tokens:
    data = json.loads(path.read_text(encoding="utf-8"))

    palette = {
        f"{family}-{shade}": parse_oklch(value)
        for family, shades in data["palette"].items()
        for shade, value in shades.items()
    }
    for name, spec in data["derived"].items():
        try:
            start, end = palette[spec["from"]], palette[spec["to"]]
            amount = spec["amount"]
        except KeyError as error:
            raise ValueError(f"Derived color {name!r} references unknown entry or key {error}") from error
        palette[name] = mix(start, end, amount)

    missing = sorted({name for name in data["roles"].values() if name not in palette})
    if missing:
        raise ValueError(f"Roles reference unknown palette entries: {', '.join(missing)}")

    return Tokens(palette, data["roles"], data["radius"], data["meta"])
