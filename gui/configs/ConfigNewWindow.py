from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QIcon
from gui.actions.action_refresh import QActionMidiRefresh
from gui.configs.combo_midi_list import CmbBoxMidiController
from gui.configs.wdgt_setup_knob import WidgetSetupKnob
from gui.configs.config_knob_setup_flag import ConfigKnobSetupFlag

from data.data_general import hc_file_filter


class ConfigNewWindow(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setWindowTitle("Create MIDI controller configuration")

        self.layout_window = QVBoxLayout()

        # Top part
        self.lbl_list_midi_controller = QLabel("MIDI controllers")
        self.action_refresh = QActionMidiRefresh()
        self.button_refresh = QToolButton(self)
        self.button_refresh.setDefaultAction(self.action_refresh)
        self.cmb_midi_controller = CmbBoxMidiController()

        self.button_refresh.clicked.connect(self.parent.refresh_midi_input)
        self.cmb_midi_controller.currentTextChanged.connect(
            self.parent.on_choice_controller_changed
        )

        self.layout_top = QHBoxLayout()

        self.layout_top.addWidget(self.lbl_list_midi_controller)
        self.layout_top.addWidget(self.cmb_midi_controller)
        self.layout_top.addWidget(self.button_refresh)

        self.layout_window.addLayout(self.layout_top)

        # Explanation part
        self.lbl_explanation = QLabel(
            """
            EXPLANATION HERE
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """
        )
        self.lbl_explanation.setWordWrap(True)  # Enable word wrap

        self.layout_window.addWidget(self.lbl_explanation)

        # Setup part
        self.lbl_setup_pad_title = QLabel("Pad setup:")
        self.lbl_setup_pad_xpln = QLabel("Pad explanation")

        self.lbl_setup_knob_title = QLabel("Knob setup:")
        self.lbl_setup_knob_xpln = QLabel("Knob explanation")

        self.button_setup_pad = QPushButton("Setup pad")

        self.setup_knob_mode = WidgetSetupKnob(knob_function=ConfigKnobSetupFlag.MODE)
        self.setup_knob_chord_comp = WidgetSetupKnob(
            knob_function=ConfigKnobSetupFlag.CHORD_COMP
        )
        self.setup_knob_chord_size = WidgetSetupKnob(
            knob_function=ConfigKnobSetupFlag.CHORD_SIZE
        )
        self.setup_knob_base_note = WidgetSetupKnob(
            knob_function=ConfigKnobSetupFlag.BASE_NOTE
        )
        self.setup_knob_key_degree = WidgetSetupKnob(
            knob_function=ConfigKnobSetupFlag.KEY_DEGREE
        )

        self.button_setup_pad.clicked.connect(self.on_setup_pad_clicked)
        self.setup_knob_mode.signal_button_setup_clicked.connect(
            self.on_knob_setup_clicked
        )

        self.layout_setup = QVBoxLayout()

        self.layout_setup.addWidget(self.lbl_setup_pad_title)
        self.layout_setup.addWidget(self.lbl_setup_pad_xpln)
        self.layout_setup.addWidget(self.button_setup_pad)

        self.layout_setup.addWidget(self.lbl_setup_knob_title)
        self.layout_setup.addWidget(self.lbl_setup_knob_xpln)
        self.layout_setup.addWidget(self.setup_knob_mode)
        self.layout_setup.addWidget(self.setup_knob_chord_comp)
        self.layout_setup.addWidget(self.setup_knob_chord_size)
        self.layout_setup.addWidget(self.setup_knob_base_note)
        self.layout_setup.addWidget(self.setup_knob_key_degree)

        self.layout_window.addLayout(self.layout_setup)

        # Exit part
        self.button_save = QPushButton("Save")
        self.button_cancel = QPushButton("Cancel")

        self.button_save.clicked.connect(self.on_save_click)
        self.button_cancel.clicked.connect(self.on_cancel_click)

        self.layout_exit = QHBoxLayout()

        self.layout_exit.addWidget(self.button_save)
        self.layout_exit.addWidget(self.button_cancel)

        self.layout_window.addLayout(self.layout_exit)

        self.setLayout(self.layout_window)

    def on_setup_pad_clicked(self):
        print("setup pad")

    def on_save_click(self):
        self.open_save_dialog()

    def on_cancel_click(self):
        self.close()

    def open_save_dialog(self):
        # Open the save file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",  # Dialog title
            "",  # Starting directory (empty for default)
            hc_file_filter,  # File filter
        )
        if file_path:  # If user didn't cancel
            print(file_path)
            # Here you would write your file saving logic
            self.close()

    def on_knob_setup_clicked(self, knob_function):
        # Open an instruction pop up
        if knob_function == ConfigKnobSetupFlag.MODE.value:
            self.setup_knob_mode.diag_window.show()
        elif knob_function == ConfigKnobSetupFlag.CHORD_COMP.value:
            self.setup_knob_chord_comp.diag_window.show()
        elif knob_function == ConfigKnobSetupFlag.CHORD_SIZE.value:
            self.setup_knob_chord_size.diag_window.show()
        elif knob_function == ConfigKnobSetupFlag.BASE_NOTE.value:
            self.setup_knob_base_note.diag_window.show()
        elif knob_function == ConfigKnobSetupFlag.KEY_DEGREE.value:
            self.setup_knob_key_degree.diag_window.show()

        # Need to transfer this logic linked to the pop up opening due to cancel? Or maybe a simple signal
        # Asses the knob
        # Assert success
        # If success, change value corresponding knob
        # Else tell the user
        # Close the instruction pop up

        else:
            # IMPROVE
            # show error dialog
            pass


# if knob_function == ConfigKnobSetupFlag.UNKOWN.value:

#         elif knob_function == ConfigKnobSetupFlag.MODE.value:

#         elif knob_function == ConfigKnobSetupFlag.CHORD_COMP.value:

#         elif knob_function == ConfigKnobSetupFlag.CHORD_SIZE.value:

#         elif knob_function == ConfigKnobSetupFlag.BASE_NOTE.value:

#         elif knob_function == ConfigKnobSetupFlag.KEY_DEGREE.value:
