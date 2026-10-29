from pathlib import Path

import pytest

from build.krita_qss import render_qss
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")
TEMPLATE = (ROOT / "krita" / "theme" / "style.qss.template").read_text(encoding="utf-8")


def test_placeholders_are_replaced_with_role_hex():
    text = render_qss("a { color: %text.primary%; }", TOKENS)
    assert text == f"a {{ color: {TOKENS.hex('text.primary')}; }}"


def test_radius_placeholders_use_pixels():
    text = render_qss("a { border-radius: %radius.panel%; }", TOKENS)
    assert "px" in text


def test_unknown_placeholder_fails_loudly():
    with pytest.raises(KeyError, match="surface.nope"):
        render_qss("a { color: %surface.nope%; }", TOKENS)


def test_shipped_template_renders_with_no_leftover_markers():
    text = render_qss(TEMPLATE, TOKENS)
    assert "%" not in text
    assert "\r" not in text
    assert len(text) > 500


def test_shipped_template_uses_the_whole_surface_stack():
    for role in ("surface.background", "surface.panel", "surface.raised", "surface.control", "accent.base"):
        assert f"%{role}%" in TEMPLATE, role
