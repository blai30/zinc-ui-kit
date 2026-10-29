from __future__ import annotations

import logging
from pathlib import Path

import bpy

log = logging.getLogger(__name__)

UI_FONT = "GeistUIKit-Variable.ttf"
MONO_FONT = "JetBrainsMonoUIKit-Regular.ttf"

# The user's font paths from before this add-on changed them.
_original: tuple | None = None


def _without_ours(path: str, font_dir: Path) -> str:
    # A path inside our own font folder was saved by an earlier session or version
    # of this add-on (the file may no longer exist), so it means the default font.
    return "" if path and Path(path).parent == font_dir else path


def apply_fonts(font_dir: Path) -> None:
    global _original
    ui_path = font_dir / UI_FONT
    mono_path = font_dir / MONO_FONT
    if not (ui_path.is_file() and mono_path.is_file()):
        log.warning("Bundled fonts not found in %s", font_dir)
        return
    view = bpy.context.preferences.view
    if _original is None:
        _original = (_without_ours(view.font_path_ui, font_dir), _without_ours(view.font_path_ui_mono, font_dir))
    view.font_path_ui = str(ui_path)
    view.font_path_ui_mono = str(mono_path)


def restore_fonts() -> None:
    global _original
    if _original is None:
        return
    view = bpy.context.preferences.view
    view.font_path_ui, view.font_path_ui_mono = _original
    _original = None
