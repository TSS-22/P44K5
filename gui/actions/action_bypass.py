from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QStyle
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt


class QActionBypass(QAction):
    signal_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setText("Midi bypass")
        self.setStatusTip("Midi bypass turned off")
        self.setCheckable(True)
        self.icon_stop = QIcon.fromTheme("media-playback-stop")
        self.icon_go = QIcon.fromTheme("media-playback-start")
        self.toggled.connect(self.on_toggled)  # Connect the signal
        self.setIcon(self.icon_stop)
        self.setShortcut(Qt.Key_Space)

    def on_toggled(self, checked):
        self.signal_toggled.emit(checked)
        if checked:
            self.setStatusTip("Midi bypass turned on (Space bar)")
            self.setIcon(self.icon_go)
        else:
            self.setStatusTip("Midi bypass turned off (Space bar)")
            self.setIcon(self.icon_stop)
