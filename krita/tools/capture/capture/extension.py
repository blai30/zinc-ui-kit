import os
import traceback

from krita import Extension, Krita
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication

try:
    from PyQt5.QtTest import QTest
except ImportError:
    QTest = None

OUT = os.environ.get("UIKIT_OUT", "/tmp/uikit-krita/out")
MENUS = ("File", "Layer", "Filters", "Settings")


class Capture(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.lines = []

    def setup(self):
        QTimer.singleShot(9000, self.open_document)

    def createActions(self, window):
        pass

    def window(self):
        return Krita.instance().activeWindow().qwindow()

    def note(self, text):
        self.lines.append(text)

    def find_action(self, name):
        for action in Krita.instance().actions():
            if action.objectName() == name:
                return action
        raise RuntimeError("action not found: " + name)

    def guard(self, step):
        try:
            step()
        except Exception:
            with open(os.path.join(OUT, "error.txt"), "w") as handle:
                handle.write(traceback.format_exc())
            self.finish()

    def open_document(self):
        def work():
            application = Krita.instance()
            document = application.createDocument(1200, 900, "capture", "RGBA", "U8", "", 120.0)
            application.activeWindow().addView(document)
            self.document = document
            self.note("stylesheet length %d" % len(QApplication.instance().styleSheet()))
            self.note("font " + QApplication.font().family())
            self.note("window color " + self.window().palette().window().color().name())
            QTimer.singleShot(3500, lambda: self.guard(self.window_shot))
        self.guard(work)

    def window_shot(self):
        self.window().grab().save(os.path.join(OUT, "window.png"))
        for action in self.window().menuBar().actions():
            title = action.text().replace("&", "").replace(" ", "-")
            if action.menu() is not None and title in MENUS:
                action.menu().grab().save(os.path.join(OUT, "menu-%s.png" % title))
        self.note("window and menus captured")
        # Try the real shortcut first, then fall back to the action.
        if QTest is not None:
            QTest.keyClick(self.window(), Qt.Key_K, Qt.ControlModifier)
        QTimer.singleShot(1200, lambda: self.guard(self.palette_shot))

    def palette_dialog(self):
        for widget in QApplication.topLevelWidgets():
            if widget.objectName() == "uikitPalette" and widget.isVisible():
                return widget
        return None

    def palette_shot(self):
        dialog = self.palette_dialog()
        self.note("shortcut opened the palette: %s" % (dialog is not None))
        if dialog is None:
            self.find_action("uikit_command_palette").trigger()
            QTimer.singleShot(1200, lambda: self.guard(self.palette_shot_after_action))
            return
        self.palette_shot_after_action()

    def palette_shot_after_action(self):
        dialog = self.palette_dialog()
        if dialog is None:
            raise RuntimeError("palette dialog never appeared")
        dialog.grab().save(os.path.join(OUT, "palette-empty.png"))
        self.note("palette entries %d" % dialog._list.count())
        dialog._input.setText("layer")
        QTimer.singleShot(800, lambda: self.guard(self.palette_query_shot))

    def palette_query_shot(self):
        dialog = self.palette_dialog()
        dialog.grab().save(os.path.join(OUT, "palette-query.png"))
        first = dialog._list.item(0).text() if dialog._list.count() else "none"
        self.note("palette results for 'layer': %d, first: %s" % (dialog._list.count(), first))
        dialog.close()
        toggle = self.find_action("uikit_theme_toggle")
        self.note("toggle checked before: %s" % toggle.isChecked())
        toggle.setChecked(False)
        QTimer.singleShot(2000, lambda: self.guard(self.restored_shot))

    def restored_shot(self):
        self.window().grab().save(os.path.join(OUT, "restored.png"))
        self.note(
            "after toggle off: stylesheet length %d, window color %s"
            % (len(QApplication.instance().styleSheet()), self.window().palette().window().color().name())
        )
        self.find_action("uikit_theme_toggle").setChecked(True)
        QTimer.singleShot(2500, lambda: self.guard(self.reapplied_shot))

    def reapplied_shot(self):
        self.window().grab().save(os.path.join(OUT, "reapplied.png"))
        self.note(
            "after toggle on: stylesheet length %d, font %s"
            % (len(QApplication.instance().styleSheet()), QApplication.font().family())
        )
        self.finish()

    def finish(self):
        with open(os.path.join(OUT, "info.txt"), "w") as handle:
            handle.write("\n".join(self.lines) + "\n")
        QApplication.quit()
