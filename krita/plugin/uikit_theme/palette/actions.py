from __future__ import annotations

from krita import Krita
from PyQt5.QtGui import QKeySequence

from .ranking import Entry


def _clean(text: str) -> str:
    return text.replace("&", "").strip()


def _menu_paths(menu_bar) -> dict:
    # Map action object names to a "Menu > Submenu" path.
    paths = {}

    def walk(menu, trail):
        for action in menu.actions():
            submenu = action.menu()
            if submenu is not None:
                walk(submenu, trail + [_clean(action.text())])
            elif action.objectName():
                paths.setdefault(action.objectName(), " > ".join(trail))

    for top in menu_bar.actions():
        if top.menu() is not None:
            walk(top.menu(), [_clean(top.text())])
    return paths


def collect(qwindow):
    # Returns (entries, actions by object name) for every enabled, named Krita action.
    paths = _menu_paths(qwindow.menuBar())
    entries = []
    actions = {}
    for action in Krita.instance().actions():
        name = action.objectName()
        label = _clean(action.text())
        if not name or not label or not action.isEnabled():
            continue
        shortcut = action.shortcut().toString(QKeySequence.NativeText)
        entries.append(Entry(name=name, label=label, path=paths.get(name, ""), shortcut=shortcut))
        actions[name] = action
    return entries, actions
