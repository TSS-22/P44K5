from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QStyle, QFileDialog
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt


class QActionMidiConnect(QAction):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Connect to MIDI controller")
        self.setStatusTip("Connect to MIDI controller")
        self.icon = QIcon.fromTheme("input-keyboard")
        self.setIcon(self.icon)
        self.triggered.connect(self.clicked)
        self.setShortcut(Qt.Key_Return)

    def clicked(self):
        pass
