from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal


class DiagKnobSetup(QMessageBox):
    sig_cancel = Signal()

    def __init__(
        self,
        parent=None,
        title="Instructions",
    ):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        self.setStandardButtons(QMessageBox.Cancel)

        self.rejected.connect(self.sig_cancel.emit)
