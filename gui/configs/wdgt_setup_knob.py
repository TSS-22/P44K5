from PySide6.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal

from gui.configs.config_knob_setup_flag import ConfigKnobSetupFlag
from gui.configs.information_dialogs.DiagKnobSetup import DiagKnobSetup


class WidgetSetupKnob(QWidget):

    signal_button_setup_clicked = Signal(str)

    def __init__(
        self,
        knob_function=ConfigKnobSetupFlag.UNKOWN,
        button_text="Setup",
        checkbox_text="activate",
    ):
        super().__init__()

        self.function = knob_function

        self.diag_window = DiagKnobSetup(
            title="Instructions",
            knob_function=self.function,
        )

        # Create widgets
        self.checkbox = QCheckBox(checkbox_text)
        self.label = QLabel(knob_function.value)
        self.button = QPushButton(button_text)
        self.button.clicked.connect(self.button_clicked)

        self.button.setEnabled(False)
        self.checkbox.stateChanged.connect(self.checkbox_action)

        # Create horizontal layout
        layout = QHBoxLayout()

        # Add widgets to the layout
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Set the layout for this widget
        self.setLayout(layout)

    def checkbox_action(self, state):
        if state == 0 or state == 1:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def button_clicked(self):
        self.signal_button_setup_clicked.emit(self.function.value)
