from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import resvg_py

from build.colors import to_hex
from build.tokens import Tokens

ICONS = Path(__file__).parent.parent / "aseprite" / "icons"

# A role or palette entry, optionally with an opacity.
Paint = str | tuple[str, float]

_SVG_BODY = re.compile(r"<svg\b[^>]*>(.*)</svg>", re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


@dataclass(frozen=True)
class Part:
    width: int
    height: int
    # SVG fragment in the part's own coordinates.
    draw: Callable[[Tokens], str]
    # w1, w2, w3, h1, h2, h3 for nine-slice parts.
    slices: tuple[int, int, int, int, int, int] | None = None
    # Hotspot for cursors.
    focus: tuple[int, int] | None = None


def paint(tokens: Tokens, value: Paint | None, attribute: str) -> str:
    if value is None:
        return f'{attribute}="none"'
    name, opacity = value if isinstance(value, tuple) else (value, 1.0)
    text = f'{attribute}="{to_hex(tokens.resolve(name))}"'
    return text if opacity == 1.0 else f'{text} {attribute}-opacity="{opacity}"'


def hex_color(tokens: Tokens, name: str) -> str:
    return to_hex(tokens.resolve(name))


def rounded_rect(x: float, y: float, width: float, height: float, radius: float, corners: str = "all") -> str:
    # Path data for a rectangle whose rounded corners are picked by "all", "top", "bottom", "left", or "right".
    rounded = {
        "all": (True, True, True, True),
        "top": (True, True, False, False),
        "bottom": (False, False, True, True),
        "left": (True, False, False, True),
        "right": (False, True, True, False),
        "none": (False, False, False, False),
    }[corners]
    top_left, top_right, bottom_right, bottom_left = (radius if flag else 0 for flag in rounded)
    right, bottom = x + width, y + height
    return (
        f"M{x + top_left} {y}H{right - top_right}"
        f"A{top_right} {top_right} 0 0 1 {right} {y + top_right}V{bottom - bottom_right}"
        f"A{bottom_right} {bottom_right} 0 0 1 {right - bottom_right} {bottom}H{x + bottom_left}"
        f"A{bottom_left} {bottom_left} 0 0 1 {x} {bottom - bottom_left}V{y + top_left}"
        f"A{top_left} {top_left} 0 0 1 {x + top_left} {y}Z"
    )


def frame(
    width: int,
    height: int,
    slices: tuple[int, int, int, int, int, int] | None,
    fill: Paint | None,
    border: Paint | None = None,
    radius: float = 0,
    border_width: float = 1,
    inset: int = 0,
    corners: str = "all",
) -> Part:
    def draw(tokens: Tokens) -> str:
        # The border is stroked inside the shape so the outer edge stays on the pixel grid.
        half = border_width / 2 if border else 0
        shape = rounded_rect(
            inset + half, inset + half, width - 2 * inset - 2 * half, height - 2 * inset - 2 * half,
            max(radius - half, 0), corners,
        )
        stroke = f'{paint(tokens, border, "stroke")} stroke-width="{border_width}"' if border else ""
        return f'<path d="{shape}" {paint(tokens, fill, "fill")} {stroke}/>'

    return Part(width, height, draw, slices)


def custom(width: int, height: int, draw: Callable[[Tokens], str], slices=None, focus=None) -> Part:
    return Part(width, height, draw, slices, focus)


@cache
def lucide(name: str) -> str:
    # Inner markup of a vendored Lucide icon (24 unit grid).
    text = (ICONS / f"{name}.svg").read_text(encoding="utf-8")
    return _COMMENT.sub("", _SVG_BODY.search(text).group(1)).strip()


def _grid(width: int, height: int, padding: float) -> tuple[float, float, float]:
    # Scale and offset that center the 24 unit grid inside the padding.
    scale = min(width - 2 * padding, height - 2 * padding) / 24
    return scale, (width - 24 * scale) / 2, (height - 24 * scale) / 2


def _glyph_group(width: int, height: int, padding: float, stroke: float, rotate: float = 0) -> tuple[str, float]:
    scale, left, top = _grid(width, height, padding)
    transform = f"translate({left} {top}) scale({scale})"
    if rotate:
        transform += f" rotate({rotate} 12 12)"
    return transform, stroke / scale


def icon(
    inner: str,
    width: int,
    height: int | None = None,
    color: Paint = "text.primary",
    stroke: float = 1.5,
    padding: float = 0,
    rotate: float = 0,
) -> Part:
    # Line icon on the Lucide grid. Shapes with fill="currentColor" are filled with the icon color.
    height = height or width

    def draw(tokens: Tokens) -> str:
        transform, stroke_width = _glyph_group(width, height, padding, stroke, rotate)
        name, opacity = color if isinstance(color, tuple) else (color, 1.0)
        hex_color = to_hex(tokens.resolve(name))
        return (
            f'<g transform="{transform}" opacity="{opacity}" fill="none" stroke="{hex_color}" color="{hex_color}" '
            f'stroke-width="{stroke_width:.4f}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>'
        )

    return Part(width, height, draw)


def cursor(inner: str, focus: tuple[float, float], size: int = 32, stroke: float = 2, padding: float = 3, rotate: float = 0) -> Part:
    # White strokes over a dark outline, like system cursors. The hotspot is given on the 24 unit grid.
    scale, left, top = _grid(size, size, padding)
    hotspot = (round(left + focus[0] * scale), round(top + focus[1] * scale))

    def draw(tokens: Tokens) -> str:
        transform, stroke_width = _glyph_group(size, size, padding, stroke, rotate)
        _, outline_width = _glyph_group(size, size, padding, stroke + 3, rotate)
        groups = []
        for color, width in ((to_hex(tokens.resolve("zinc-950")), outline_width), ("#ffffff", stroke_width)):
            groups.append(
                f'<g transform="{transform}" fill="none" stroke="{color}" color="{color}" stroke-width="{width:.4f}" '
                f'stroke-linecap="round" stroke-linejoin="round">{inner}</g>'
            )
        return "".join(groups)

    return Part(size, size, draw, focus=hotspot)


@dataclass(frozen=True)
class Placement:
    x: int
    y: int
    part: Part


def pack(parts: dict[str, Part], tokens: Tokens, width: int = 512, gap: int = 2) -> tuple[dict[str, Placement], int]:
    # Shelf packing. Parts that draw identically share one sprite.
    unique: dict[tuple, tuple[int, int, str]] = {}
    for part in parts.values():
        markup = part.draw(tokens)
        unique.setdefault((part.width, part.height, markup), (part.width, part.height, markup))

    order = sorted(unique, key=lambda key: (-key[1], -key[0], key[2]))
    positions: dict[tuple, tuple[int, int]] = {}
    x = y = shelf = 0
    for key in order:
        part_width, part_height, _ = key
        if part_width > width:
            raise ValueError(f"Part is wider than the sheet: {part_width}")
        if x + part_width > width:
            x, y, shelf = 0, y + shelf + gap, 0
        positions[key] = (x, y)
        x += part_width + gap
        shelf = max(shelf, part_height)

    placements = {}
    for name, part in parts.items():
        px, py = positions[(part.width, part.height, part.draw(tokens))]
        placements[name] = Placement(px, py, part)
    return placements, y + shelf


def render_sheet(placements: dict[str, Placement], height: int, tokens: Tokens, width: int = 512) -> bytes:
    sprites = {}
    for placement in placements.values():
        part = placement.part
        sprites[(placement.x, placement.y)] = (
            f'<svg x="{placement.x}" y="{placement.y}" width="{part.width}" height="{part.height}" overflow="hidden">'
            f"{part.draw(tokens)}</svg>"
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        + "".join(sprites[key] for key in sorted(sprites))
        + "</svg>"
    )
    return bytes(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True))
