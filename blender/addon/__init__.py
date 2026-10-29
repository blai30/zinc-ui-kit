from __future__ import annotations

import logging
from pathlib import Path

import bpy

from . import font_settings, preferences
from .declutter import apply
from .declutter.groups import GROUPS

log = logging.getLogger(__name__)

FONT_DIR = Path(__file__).parent / "fonts"


def _settings():
    entry = bpy.context.preferences.addons.get(__package__)
    return entry.preferences if entry else None


def _shown() -> dict:
    settings = _settings()
    if settings is None:
        return {group.key: group.default_shown for group in GROUPS}
    return {group.key: getattr(settings, f"show_{group.key}") for group in GROUPS}


def refresh(apply_tabs_to_open_file: bool = False) -> None:
    shown = _shown()
    # Opened files keep their tabs unless the user just changed a setting.
    if apply_tabs_to_open_file or not bpy.data.filepath:
        apply.apply_tabs(shown)
    apply.apply_panels(shown)
    settings = _settings()
    if settings is None or settings.use_fonts:
        font_settings.apply_fonts(FONT_DIR)
    else:
        font_settings.restore_fonts()


@bpy.app.handlers.persistent
def _on_new_file(_dummy) -> None:
    # Untitled files are new or factory-startup scenes. Opened files are left alone.
    if not bpy.data.filepath:
        shown = _shown()
        apply.apply_tabs(shown)
        apply.apply_workspaces(shown)


def _startup() -> None:
    # Runs once after Blender finishes loading, when windows and screens exist.
    refresh()
    _on_new_file(None)


def register() -> None:
    bpy.utils.register_class(preferences.UIKitPreferences)
    preferences.on_change = lambda: refresh(apply_tabs_to_open_file=True)
    bpy.app.handlers.load_post.append(_on_new_file)
    bpy.app.handlers.load_factory_startup_post.append(_on_new_file)
    bpy.app.timers.register(_startup, first_interval=0.1)


def unregister() -> None:
    if bpy.app.timers.is_registered(_startup):
        bpy.app.timers.unregister(_startup)
    for handlers in (bpy.app.handlers.load_post, bpy.app.handlers.load_factory_startup_post):
        if _on_new_file in handlers:
            handlers.remove(_on_new_file)
    apply.restore_panels()
    apply.apply_tabs({group.key: True for group in GROUPS})
    font_settings.restore_fonts()
    preferences.on_change = None
    bpy.utils.unregister_class(preferences.UIKitPreferences)
