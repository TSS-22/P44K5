from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QStyle
import os


class QActionBypass(QAction, QStyle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Midi bypass")
        self.setStatusTip("Turn on midi bypass")
        self.setCheckable(True)
        assert os.path.exists(
            "./ressources/gui/icons/prohibition.png"
        ), "Stop icon not found!"
        assert os.path.exists(
            "./ressources/gui/icons/play-solid.png"
        ), "Go icon not found!"
        self.icon_stop = QIcon("../ressources/gui/icons/prohibition.png")
        self.icon_go = QIcon("../ressources/gui/icons/play_solid.png")
        self.toggled.connect(self.on_toggled)  # Connect the signal
        self.setIcon(self.icon_go)

    def on_toggled(self, checked):
        if checked:
            self.setStatusTip("Turn off midi bypass")
            # self.setIcon(self.style().standardIcon(self.icon_go))
        else:
            self.setStatusTip("Turn on midi bypass")
            # self.setIcon(self.style().standardIcon(self.icon_stop))
