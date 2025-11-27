from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal

from data.data_general import hc_diag_knob_setup_txt
from gui.configs.config_knob_setup_flag import ConfigKnobSetupFlag


class DiagKnobSetup(QMessageBox):

    sig_cancel = Signal()

    def __init__(
        self, parent=None, title="Information", knob_function=ConfigKnobSetupFlag.UNKOWN
    ):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        self.setText(hc_diag_knob_setup_txt + " " + knob_function.value)
        self.setStandardButtons(QMessageBox.Cancel)
