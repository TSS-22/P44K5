import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from gui_qt.widgetBaseNote import WidgetBaseNote


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("8P4K PowerHouse")
        wdgt_base_note = WidgetBaseNote(self)
        self.setCentralWidget(wdgt_base_note)
