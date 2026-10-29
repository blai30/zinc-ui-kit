from pathlib import Path

FONT_DIR = Path(__file__).parent.parent / "blender" / "addon" / "fonts"
TRUETYPE_MAGIC = b"\x00\x01\x00\x00"


def test_font_files_are_truetype():
    for name in ("GeistUIKit-Variable.ttf", "JetBrainsMonoUIKit-Regular.ttf"):
        data = (FONT_DIR / name).read_bytes()
        assert data[:4] == TRUETYPE_MAGIC, name
        assert len(data) > 10_000, name


def test_licenses_ship_with_the_fonts():
    for name in ("OFL-Geist.txt", "OFL-JetBrainsMono.txt"):
        text = (FONT_DIR / name).read_text(encoding="utf-8")
        assert "SIL OPEN FONT LICENSE" in text.upper(), name
        assert "\r" not in text, name
