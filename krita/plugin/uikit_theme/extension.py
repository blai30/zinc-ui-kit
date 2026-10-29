from __future__ import annotations

import time

from krita import Extension, Krita
from PyQt5.QtCore import QEvent, QObject, QTimer
from PyQt5.QtGui import QFont, QKeySequence, QPalette
from PyQt5.QtWidgets import QApplication, QShortcut

from . import theme
from .palette.dialog import CommandPalette

SETTINGS_GROUP = "uikitTheme"
# Ignore palette-change events caused by our own apply.
QUIET_SECONDS = 1.5


class _Watcher(QObject):
    # Krita re-applies its own theme when the user changes it in Settings.
    # Re-apply ours afterwards.
    def __init__(self, extension):
        super().__init__()
        self._extension = extension
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(400)
        self._timer.timeout.connect(extension.apply)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.ApplicationPaletteChange and self._extension.wants_reapply():
            self._timer.start()
        return False


class UIKitExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self._originals = None
        self._quiet_until = 0.0
        self._watcher = None
        self._palette_dialog = None

    def setup(self):
        Krita.instance().notifier().windowCreated.connect(self._on_window_created)

    def createActions(self, window):
        toggle = window.createAction("uikit_theme_toggle", "UI Kit Theme", "tools/scripts")
        toggle.setCheckable(True)
        toggle.setChecked(self._enabled())
        toggle.toggled.connect(self._set_enabled)

        palette_action = window.createAction("uikit_command_palette", "Command Palette...", "tools/scripts")
        palette_action.triggered.connect(self.open_palette)
        # Ctrl maps to Cmd on macOS.
        shortcut = QShortcut(QKeySequence("Ctrl+K"), window.qwindow())
        shortcut.activated.connect(self.open_palette)

    def _on_window_created(self):
        # Let the window finish constructing before restyling the application.
        if self._enabled():
            QTimer.singleShot(0, self.apply)

    def _enabled(self) -> bool:
        return Krita.instance().readSetting(SETTINGS_GROUP, "enabled", "true") == "true"

    def _set_enabled(self, enabled: bool) -> None:
        Krita.instance().writeSetting(SETTINGS_GROUP, "enabled", "true" if enabled else "false")
        if enabled:
            self.apply()
        else:
            self.restore()

    def wants_reapply(self) -> bool:
        return self._enabled() and time.monotonic() > self._quiet_until

    def apply(self):
        application = QApplication.instance()
        if self._originals is None:
            self._originals = (QPalette(application.palette()), application.styleSheet(), QFont(application.font()))
        self._quiet_until = time.monotonic() + QUIET_SECONDS
        palette, stylesheet, font = self._originals
        application.setPalette(theme.build_palette(palette))
        application.setStyleSheet(theme.load_stylesheet())
        application.setFont(theme.font_with_family(font))
        if self._watcher is None:
            self._watcher = _Watcher(self)
            application.installEventFilter(self._watcher)

    def restore(self):
        if self._originals is None:
            return
        application = QApplication.instance()
        palette, stylesheet, font = self._originals
        self._quiet_until = time.monotonic() + QUIET_SECONDS
        application.setPalette(palette)
        application.setStyleSheet(stylesheet)
        application.setFont(font)
        self._originals = None

    def open_palette(self):
        window = Krita.instance().activeWindow()
        if window is None:
            return
        self._palette_dialog = CommandPalette.create(window.qwindow())
        self._palette_dialog.show_centered()
