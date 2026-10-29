import zipfile
from pathlib import Path

import pytest

from build.krita_package import build_krita_plugin
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")


@pytest.fixture(scope="module")
def archive(tmp_path_factory):
    output = tmp_path_factory.mktemp("dist")
    path = build_krita_plugin(ROOT, TOKENS, output)
    with zipfile.ZipFile(path) as handle:
        yield path, handle


def test_zip_is_named_from_meta(archive):
    path, _ = archive
    assert path.name == "uikit_theme-0.1.0.zip"


def test_zip_has_the_descriptor_and_package(archive):
    _, handle = archive
    names = set(handle.namelist())
    assert "uikit_theme.desktop" in names
    assert "uikit_theme/__init__.py" in names
    assert "uikit_theme/extension.py" in names
    assert "uikit_theme/palette/ranking.py" in names


def test_zip_has_generated_and_bundled_assets(archive):
    _, handle = archive
    names = set(handle.namelist())
    assert "uikit_theme/assets/UIKitGraphite.colors" in names
    assert "uikit_theme/assets/style.qss" in names
    assert "uikit_theme/assets/GeistUIKit-Variable.ttf" in names
    assert "uikit_theme/assets/OFL-Geist.txt" in names


def test_zip_has_no_caches_or_template_files(archive):
    _, handle = archive
    for name in handle.namelist():
        assert "__pycache__" not in name, name
        assert not name.endswith(".template"), name
        assert name != "meta.json", name


def test_descriptor_registers_a_python_plugin(archive):
    _, handle = archive
    text = handle.read("uikit_theme.desktop").decode("utf-8")
    assert "ServiceTypes=Krita/PythonPlugin" in text
    assert "X-KDE-Library=uikit_theme" in text
    assert "Name=UI Kit Theme" in text
    assert "\r" not in text


def test_stylesheet_has_no_leftover_placeholders(archive):
    _, handle = archive
    text = handle.read("uikit_theme/assets/style.qss").decode("utf-8")
    assert "%" not in text


def test_scheme_is_named_after_the_package(archive):
    _, handle = archive
    text = handle.read("uikit_theme/assets/UIKitGraphite.colors").decode("utf-8")
    assert "Name=UI Kit Graphite" in text
