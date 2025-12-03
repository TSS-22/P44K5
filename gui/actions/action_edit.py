from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QStyle, QFileDialog
from PySide6.QtCore import Signal


class QActionConfigEdit(QAction):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Edit MIDI controller config")
        self.setStatusTip("Edit MIDI controller config (Ctrl + H)")
        self.icon = QIcon.fromTheme("document-properties")
        self.setIcon(self.icon)
        self.setShortcut(QKeySequence.Replace)
