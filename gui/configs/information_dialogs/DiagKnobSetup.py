from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, QTimer

from gui.configs.config_knob_setup_flag import ConfigSetupFlag


class DiagKnobSetup(QMessageBox):

    sig_cancel = Signal()

    def __init__(
        self, parent=None, title="Information", knob_function=ConfigSetupFlag.UNKOWN
    ):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        # CLEAN
        # Some arguments might not be needed anymore
        # self.setText(hc_diag_knob_setup_txt + " " + knob_function.value)
        self.setStandardButtons(QMessageBox.Cancel)
        self.cancel_button = self.button(QMessageBox.Cancel)
        self.rejected.connect(self.on_cancel)

    def on_cancel(self):
        self.sig_cancel.emit()
