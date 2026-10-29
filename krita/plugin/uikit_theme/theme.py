from __future__ import annotations

import os

from PyQt5.QtGui import QColor, QFont, QFontDatabase, QPalette

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# (scheme section, key, QPalette role)
ROLE_MAP = (
    ("Colors:Window", "BackgroundNormal", QPalette.Window),
    ("Colors:Window", "ForegroundNormal", QPalette.WindowText),
    ("Colors:View", "BackgroundNormal", QPalette.Base),
    ("Colors:View", "BackgroundAlternate", QPalette.AlternateBase),
    ("Colors:View", "ForegroundNormal", QPalette.Text),
    ("Colors:Button", "BackgroundNormal", QPalette.Button),
    ("Colors:Button", "ForegroundNormal", QPalette.ButtonText),
    ("Colors:Selection", "BackgroundNormal", QPalette.Highlight),
    ("Colors:Selection", "ForegroundNormal", QPalette.HighlightedText),
    ("Colors:Tooltip", "BackgroundNormal", QPalette.ToolTipBase),
    ("Colors:Tooltip", "ForegroundNormal", QPalette.ToolTipText),
)


def _read_scheme(path: str) -> dict:
    sections = {}
    current = None
    with open(path, encoding="utf-8") as handle:
        for line in handle.read().splitlines():
            if line.startswith("["):
                current = line[1:-1]
                sections[current] = {}
            elif "=" in line and current is not None:
                key, value = line.split("=", 1)
                sections[current][key] = value
    return sections


def build_palette(base: QPalette) -> QPalette:
    sections = _read_scheme(os.path.join(ASSETS, "UIKitZinc.colors"))
    palette = QPalette(base)
    for section, key, role in ROLE_MAP:
        red, green, blue = (int(part) for part in sections[section][key].split(","))
        palette.setColor(role, QColor(red, green, blue))
    return palette


def load_stylesheet() -> str:
    with open(os.path.join(ASSETS, "style.qss"), encoding="utf-8") as handle:
        return handle.read()


def font_with_family(base: QFont) -> QFont:
    # The bundled font is registered with Qt, so no system install is needed.
    identifier = QFontDatabase.addApplicationFont(os.path.join(ASSETS, "GeistUIKit-Variable.ttf"))
    families = QFontDatabase.applicationFontFamilies(identifier) if identifier != -1 else []
    font = QFont(base)
    if families:
        font.setFamily(families[0])
    return font
