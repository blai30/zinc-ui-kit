from __future__ import annotations

from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtWidgets import QDialog, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout

from . import actions as action_source
from .ranking import rank


class CommandPalette(QDialog):
    @classmethod
    def create(cls, parent):
        entries, actions = action_source.collect(parent)
        return cls(parent, entries, actions)

    def __init__(self, parent, entries, actions):
        super().__init__(parent, Qt.Popup)
        self.setObjectName("uikitPalette")
        self._entries = entries
        self._actions = actions

        self._input = QLineEdit(self)
        self._input.setPlaceholderText("Type a command")
        self._list = QListWidget(self)
        self._list.setFocusPolicy(Qt.NoFocus)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.addWidget(self._input)
        layout.addWidget(self._list)
        self.resize(620, 400)

        self._input.textChanged.connect(self._refresh)
        self._input.installEventFilter(self)
        self._list.itemActivated.connect(self._run_item)
        self._refresh("")

    def show_centered(self):
        parent = self.parentWidget()
        origin = parent.mapToGlobal(parent.rect().topLeft())
        x = origin.x() + (parent.width() - self.width()) // 2
        y = origin.y() + parent.height() // 6
        self.move(x, y)
        self.show()
        self._input.setFocus()

    def eventFilter(self, watched, event):
        if watched is self._input and event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_Down, Qt.Key_Up):
                step = 1 if key == Qt.Key_Down else -1
                row = min(max(self._list.currentRow() + step, 0), self._list.count() - 1)
                self._list.setCurrentRow(row)
                return True
            if key in (Qt.Key_Return, Qt.Key_Enter):
                item = self._list.currentItem()
                if item is not None:
                    self._run_item(item)
                return True
        return super().eventFilter(watched, event)

    def _refresh(self, query):
        self._list.clear()
        for entry in rank(query, self._entries):
            text = entry.label
            if entry.path:
                text += "    " + entry.path
            if entry.shortcut:
                text += "    " + entry.shortcut
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, entry.name)
            self._list.addItem(item)
        if self._list.count():
            self._list.setCurrentRow(0)

    def _run_item(self, item):
        action = self._actions.get(item.data(Qt.UserRole))
        self.close()
        if action is not None:
            # Let the popup close and focus return before the action runs.
            QTimer.singleShot(0, action.trigger)
