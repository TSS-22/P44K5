from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QStyle, QFileDialog
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt


class QActionMidiRefresh(QAction):
    signal_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Refresh MIDI controller list")
        self.setStatusTip("Refresh MIDI controller list")
        self.icon = QIcon.fromTheme("view-refresh")
        self.setIcon(self.icon)
        self.triggered.connect(self.signal_clicked.emit)
        self.setShortcut(QKeySequence.Refresh)
