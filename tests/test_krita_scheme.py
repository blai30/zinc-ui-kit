from pathlib import Path

import pytest

from build.krita_scheme import generate_scheme
from build.colors import to_rgb
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")
BASE = (ROOT / "krita" / "theme" / "base.colors").read_text(encoding="utf-8")


def sections(text):
    result = {}
    current = None
    for line in text.splitlines():
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1]
            result[current] = {}
        elif "=" in line and current is not None:
            key, value = line.split("=", 1)
            result[current][key] = value
    return result


def rgb_text(role):
    return ",".join(str(channel) for channel in to_rgb(TOKENS.color(role)))


@pytest.fixture(scope="module")
def scheme():
    return sections(generate_scheme(BASE, TOKENS))


def test_no_section_or_key_is_added_or_dropped(scheme):
    base = sections(BASE)
    assert set(scheme) == set(base)
    for name in base:
        assert set(scheme[name]) == set(base[name]), name


def test_window_uses_the_panel_surface(scheme):
    window = scheme["Colors:Window"]
    assert window["BackgroundNormal"] == rgb_text("surface.panel")
    assert window["BackgroundAlternate"] == rgb_text("surface.raised")
    assert window["ForegroundNormal"] == rgb_text("text.primary")
    assert window["DecorationFocus"] == rgb_text("accent.base")


def test_buttons_views_and_tooltips(scheme):
    assert scheme["Colors:Button"]["BackgroundNormal"] == rgb_text("surface.control")
    assert scheme["Colors:View"]["BackgroundNormal"] == rgb_text("surface.background")
    assert scheme["Colors:Tooltip"]["BackgroundNormal"] == rgb_text("surface.raised")


def test_selection_uses_the_muted_accent(scheme):
    selection = scheme["Colors:Selection"]
    assert selection["BackgroundNormal"] == rgb_text("accent.muted")
    assert selection["BackgroundAlternate"] == rgb_text("accent.pressed")
    assert selection["ForegroundNormal"] == rgb_text("text.strong")


def test_status_colors(scheme):
    window = scheme["Colors:Window"]
    assert window["ForegroundNegative"] == rgb_text("status.danger")
    assert window["ForegroundNeutral"] == rgb_text("status.warning")
    assert window["ForegroundPositive"] == rgb_text("status.success")


def test_scheme_is_named_after_the_package(scheme):
    assert scheme["General"]["Name"] == "UI Kit Zinc"
    assert scheme["General"]["ColorScheme"] == "UI Kit Zinc"


def test_output_has_lf_endings_only():
    assert "\r" not in generate_scheme(BASE, TOKENS)


def test_missing_key_fails_loudly():
    broken = BASE.replace("DecorationFocus=83,114,142", "", 1)
    with pytest.raises(KeyError, match="DecorationFocus"):
        generate_scheme(broken, TOKENS)
