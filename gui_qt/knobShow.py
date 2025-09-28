from PySide6.QtWidgets import QDial
from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent, QMouseEvent


class KnobShow(QDial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEnabled(True)  # Keep it visually active

    def wheelEvent(self, event: QWheelEvent):
        event.ignore()  # Ignore wheel events

    def mousePressEvent(self, event: QMouseEvent):
        event.ignore()  # Ignore mouse press

    def mouseMoveEvent(self, event: QMouseEvent):
        event.ignore()  # Ignore mouse move

    def mouseReleaseEvent(self, event: QMouseEvent):
        event.ignore()  # Ignore mouse release
