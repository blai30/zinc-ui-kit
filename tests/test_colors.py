import re

import pytest

from build.colors import Oklch, mix, parse_oklch, to_hex, to_rgb


def test_parse_percent_lightness():
    assert parse_oklch("oklch(14.1% 0.005 285.823)") == Oklch(0.141, 0.005, 285.823)


def test_parse_rejects_other_formats():
    with pytest.raises(ValueError):
        parse_oklch("#18181b")


def test_white_and_black():
    assert to_hex(parse_oklch("oklch(100% 0 0)")) == "#ffffff"
    assert to_hex(parse_oklch("oklch(0% 0 0)")) == "#000000"


def test_mid_gray():
    # Linear 0.125 encodes to sRGB 0.3885, which is 99 (0x63).
    assert to_hex(parse_oklch("oklch(50% 0 0)")) == "#636363"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("oklch(98.5% 0 0)", (250, 250, 250)),
        ("oklch(21% 0.006 285.885)", (24, 24, 27)),
        ("oklch(14.1% 0.005 285.823)", (9, 9, 11)),
    ],
)
def test_zinc_matches_published_hex_within_tolerance(value, expected):
    actual = to_rgb(parse_oklch(value))
    assert all(abs(actual_channel - expected_channel) <= 3 for actual_channel, expected_channel in zip(actual, expected))


def test_mix_endpoints_and_midpoint():
    start = Oklch(0.1, 0.0, 0.0)
    end = Oklch(0.3, 0.1, 100.0)
    assert mix(start, end, 0.0) == start
    assert mix(start, end, 1.0) == end
    middle = mix(start, end, 0.5)
    assert middle.lightness == pytest.approx(0.2)
    assert middle.chroma == pytest.approx(0.05)
    assert middle.hue == pytest.approx(50.0)


def test_mix_takes_shortest_hue_arc():
    forward = mix(Oklch(0.5, 0.1, 350.0), Oklch(0.5, 0.1, 10.0), 0.5)
    assert forward.hue == pytest.approx(0.0)
    backward = mix(Oklch(0.5, 0.1, 10.0), Oklch(0.5, 0.1, 350.0), 0.5)
    assert backward.hue == pytest.approx(0.0)


def test_out_of_gamut_color_is_clamped():
    color = Oklch(0.5, 0.4, 30.0)
    assert all(isinstance(channel, int) and 0 <= channel <= 255 for channel in to_rgb(color))
    assert re.fullmatch(r"#[0-9a-f]{6}", to_hex(color))
