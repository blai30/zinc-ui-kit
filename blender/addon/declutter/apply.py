from __future__ import annotations

import logging

import bpy

from .groups import GROUPS

log = logging.getLogger(__name__)

# Built-in panel classes this add-on has unregistered, keyed by class name.
_removed_panels: dict = {}


def apply_tabs(shown: dict) -> None:
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "PROPERTIES":
                continue
            space = area.spaces.active
            for group in GROUPS:
                for tab in group.tabs:
                    name = f"show_properties_{tab}"
                    if hasattr(space, name):
                        setattr(space, name, shown[group.key])
                    else:
                        log.warning("Properties editor has no %s", name)


def _register(name: str) -> None:
    panel = _removed_panels.pop(name)
    try:
        bpy.utils.register_class(panel)
    except (ValueError, RuntimeError) as error:
        log.warning("Could not restore panel %s: %s", name, error)


def _unregister(name: str) -> None:
    panel = getattr(bpy.types, name, None)
    if panel is None:
        log.warning("Panel %s not found", name)
        return
    try:
        bpy.utils.unregister_class(panel)
    except (ValueError, RuntimeError) as error:
        log.warning("Could not hide panel %s: %s", name, error)
        return
    _removed_panels[name] = panel


def apply_panels(shown: dict) -> None:
    # Parents register first and unregister last, because children are listed after their parent.
    for group in GROUPS:
        if shown[group.key]:
            for name in group.panels:
                if name in _removed_panels:
                    _register(name)
        else:
            for name in reversed(group.panels):
                if name not in _removed_panels:
                    _unregister(name)


def restore_panels() -> None:
    for group in GROUPS:
        for name in group.panels:
            if name in _removed_panels:
                _register(name)


def apply_workspaces(shown: dict) -> None:
    in_use = {window.workspace.name for manager in bpy.data.window_managers for window in manager.windows}
    doomed = set()
    for group in GROUPS:
        if shown[group.key]:
            continue
        for name in group.workspaces:
            workspace = bpy.data.workspaces.get(name)
            if workspace is not None and name not in in_use:
                doomed.add(workspace)
    if doomed:
        bpy.data.batch_remove(doomed)
