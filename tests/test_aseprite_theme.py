import re
import xml.etree.ElementTree as ElementTree
import zipfile
from pathlib import Path

import pytest

import build.aseprite_sheet as sheet
from build.aseprite_mapping import PARTS
from build.aseprite_theme import build_aseprite_theme
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")
BASE = ElementTree.parse(ROOT / "aseprite" / "base_theme.xml").getroot()


@pytest.fixture(scope="module")
def archive(tmp_path_factory):
    output = tmp_path_factory.mktemp("dist")
    path = build_aseprite_theme(ROOT, TOKENS, output)
    with zipfile.ZipFile(path) as handle:
        yield path, handle


@pytest.fixture(scope="module")
def theme(archive):
    _, handle = archive
    return ElementTree.fromstring(handle.read("theme.xml"))


def test_extension_is_named_from_the_package(archive):
    path, _ = archive
    assert path.name == "zinc-theme-0.1.0.aseprite-extension"


def test_extension_has_the_theme_files_font_and_licenses(archive):
    _, handle = archive
    assert set(handle.namelist()) == {
        "package.json", "theme.xml", "sheet.png", "sheet.aseprite-data",
        "GeistUIKit-Variable.ttf", "OFL-Geist.txt", "LICENSE-aseprite-theme.txt", "LICENSE-lucide.txt",
    }


def test_every_stock_part_and_color_is_defined(theme):
    for section in ("parts", "colors"):
        stock = {element.get("id") for element in BASE.find(section)}
        ours = {element.get("id") for element in theme.find(section)}
        assert stock <= ours, sorted(stock - ours)


def test_theme_is_drawn_for_100_percent_scaling(theme):
    assert theme.get("screenscaling") == "1"
    assert theme.get("uiscaling") == "1"
    dimension = theme.find("dimensions/dim[@id='scrollbar_size']")
    assert dimension.get("value") == "24"


def test_parts_fit_inside_the_sheet(archive, theme):
    _, handle = archive
    png = handle.read("sheet.png")
    width, height = int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")
    for part in theme.find("parts"):
        x, y = int(part.get("x")), int(part.get("y"))
        if part.get("w1"):
            part_width = sum(int(part.get(key)) for key in ("w1", "w2", "w3"))
            part_height = sum(int(part.get(key)) for key in ("h1", "h2", "h3"))
        else:
            part_width, part_height = int(part.get("w")), int(part.get("h"))
        assert x + part_width <= width and y + part_height <= height, part.get("id")


def test_nine_slice_parts_match_their_size():
    for name, part in PARTS.items():
        if part.slices:
            assert sum(part.slices[:3]) == part.width, name
            assert sum(part.slices[3:]) == part.height, name


def test_colors_are_hex(theme):
    for color in theme.find("colors"):
        assert re.fullmatch(r"#[0-9a-f]{6}", color.get("value")), color.get("id")


def test_every_vendored_icon_is_used():
    source = (ROOT / "build" / "aseprite_mapping.py").read_text(encoding="utf-8")
    for path in sheet.ICONS.glob("*.svg"):
        assert f'"{path.stem}"' in source, path.name


def test_cursor_hotspots_are_whole_pixels_inside_the_cursor():
    for name, part in PARTS.items():
        if part.focus:
            x, y = part.focus
            assert isinstance(x, int) and isinstance(y, int), name
            assert 0 <= x < part.width and 0 <= y < part.height, name
