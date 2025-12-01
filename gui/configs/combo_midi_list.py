from PySide6.QtWidgets import QComboBox


class CmbBoxMidiController(QComboBox):
    def __init__(self, list_midi_controller=[]):
        super().__init__()
        self.setStyleSheet(
            """
            border: #d3d3d3;
            background: #ffffff;
            min-width: 150px;
            min-height: 22px;
            """
        )
        self.setPlaceholderText("Select a device...")

    def refresh(self, list_midi_controller):
        self.clear()
        self.addItems(list_midi_controller)
