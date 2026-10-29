from __future__ import annotations

import math
import re
from dataclasses import dataclass

_OKLCH = re.compile(r"^oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s*\)$")


@dataclass(frozen=True)
class Oklch:
    lightness: float
    chroma: float
    hue: float


def parse_oklch(text: str) -> Oklch:
    match = _OKLCH.match(text.strip())
    if match is None:
        raise ValueError(f"Not an oklch() color: {text!r}")
    lightness, chroma, hue = match.groups()
    return Oklch(float(lightness) / 100, float(chroma), float(hue))


def mix(start: Oklch, end: Oklch, amount: float) -> Oklch:
    # Hue travels the shortest arc around the wheel.
    hue_delta = (end.hue - start.hue + 180) % 360 - 180
    return Oklch(
        start.lightness + (end.lightness - start.lightness) * amount,
        start.chroma + (end.chroma - start.chroma) * amount,
        (start.hue + hue_delta * amount) % 360,
    )


def _encode(linear: float) -> float:
    # Out-of-gamut channels are clamped.
    linear = min(max(linear, 0.0), 1.0)
    if linear <= 0.0031308:
        return 12.92 * linear
    return 1.055 * linear ** (1 / 2.4) - 0.055


def to_rgb(color: Oklch) -> tuple[int, int, int]:
    hue = math.radians(color.hue)
    green_red = color.chroma * math.cos(hue)
    blue_yellow = color.chroma * math.sin(hue)

    long = (color.lightness + 0.3963377774 * green_red + 0.2158037573 * blue_yellow) ** 3
    medium = (color.lightness - 0.1055613458 * green_red - 0.0638541728 * blue_yellow) ** 3
    short = (color.lightness - 0.0894841775 * green_red - 1.2914855480 * blue_yellow) ** 3

    red = 4.0767416621 * long - 3.3077115913 * medium + 0.2309699292 * short
    green = -1.2684380046 * long + 2.6097574011 * medium - 0.3413193965 * short
    blue = -0.0041960863 * long - 0.7034186147 * medium + 1.7076147010 * short

    return tuple(round(_encode(channel) * 255) for channel in (red, green, blue))


def to_hex(color: Oklch) -> str:
    return "#{:02x}{:02x}{:02x}".format(*to_rgb(color))
