import json
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
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from gui.actions.action_refresh import QActionMidiRefresh
from gui.configs.combo_midi_list import CmbBoxMidiController
from gui.configs.wdgt_setup_knob import WidgetSetupKnob
from gui.configs.config_knob_setup_flag import ConfigSetupFlag
from gui.configs.information_dialogs.DiagKnobSetup import DiagKnobSetup
from gui.configs.information_dialogs.DiagPadSetup import DiagPadSetup

from data.data_general import hc_file_filter, hc_diag_knob_setup_txt, hc_file_extension


class ConfigNewWindow(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Setup data
        self.polled_messages = []
        self.midi_control_value = {}
        for val in ConfigSetupFlag:
            self.midi_control_value[val.value] = None
        self.midi_control_value.update({"pad_mode": None})

        self.setWindowTitle("Create MIDI controller configuration")

        self.active_setup = ConfigSetupFlag.NONE
        self.midi_poll_timer = QTimer()

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

        # Dialog windows
        self.diag_window_knob = DiagKnobSetup()
        self.diag_window_knob.sig_cancel.connect(self.on_cancel_setup)

        self.diag_window_pad = DiagPadSetup()
        self.diag_window_pad.sig_cancel.connect(self.on_cancel_setup)
        self.diag_window_pad.sig_ok.connect(self.on_ok_pad_setup)
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
        ## Pads
        self.lbl_setup_pad_title = QLabel("Pad setup:")
        self.lbl_setup_pad_xpln = QLabel("Pad explanation")

        self.lbl_setup_knob_title = QLabel("Knob setup:")
        self.lbl_setup_knob_xpln = QLabel("Knob explanation")

        self.button_setup_pad = QPushButton("Setup pad")

        ## Knobs
        self.setup_knob_mode = WidgetSetupKnob(knob_function=ConfigSetupFlag.MODE)
        self.setup_knob_chord_comp = WidgetSetupKnob(
            knob_function=ConfigSetupFlag.CHORD_COMP
        )
        self.setup_knob_chord_size = WidgetSetupKnob(
            knob_function=ConfigSetupFlag.CHORD_SIZE
        )
        self.setup_knob_base_note = WidgetSetupKnob(
            knob_function=ConfigSetupFlag.BASE_NOTE
        )
        self.setup_knob_key_degree = WidgetSetupKnob(
            knob_function=ConfigSetupFlag.KEY_DEGREE
        )

        ## Signals/Slots
        self.button_setup_pad.clicked.connect(self.on_setup_pad_clicked)
        self.setup_knob_mode.signal_button_setup_clicked.connect(
            self.on_knob_setup_clicked
        )
        self.setup_knob_chord_comp.signal_button_setup_clicked.connect(
            self.on_knob_setup_clicked
        )
        self.setup_knob_chord_size.signal_button_setup_clicked.connect(
            self.on_knob_setup_clicked
        )
        self.setup_knob_base_note.signal_button_setup_clicked.connect(
            self.on_knob_setup_clicked
        )
        self.setup_knob_key_degree.signal_button_setup_clicked.connect(
            self.on_knob_setup_clicked
        )

        ## Layout
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
        self.active_setup = ConfigSetupFlag.PAD
        self.diag_window_pad.show()
        self.polled_messages = []
        self.midi_poll_timer.timeout.connect(self.poll_midi_messages_pad)
        self.midi_poll_timer.start(2)

    def on_save_click(self):
        self.open_save_dialog()

    def on_cancel_click(self):
        self.close()
        self.midi_poll_timer.stop()

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
            # IMPROVE
            # Make the dictionnary cleaner
            # Here you would write your file saving logic
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.midi_control_value, f, indent=4)
            self.close()

    def on_knob_setup_clicked(self, knob_function):
        self.active_setup = knob_function
        # Open an instruction pop up
        self.set_text_diag_knob_setup(knob_function)
        self.diag_window_knob.show()

        # Start a timer to poll for MIDI messages
        self.midi_poll_timer.timeout.connect(self.poll_midi_messages_knob)
        self.midi_poll_timer.start(5)  # Check every 10ms

    def poll_midi_messages_knob(self):
        print("polling knob")
        messages = list(self.parent.logic_worker.midi_bridge.input.iter_pending())
        if messages:

            self.midi_poll_timer.stop()  # Stop the timer
            print("Received:", messages)
            # Process messages here
            self.on_midi_message_received(messages)

    def poll_midi_messages_pad(self):
        print("polling pad")

        messages = self.parent.logic_worker.midi_bridge.input.iter_pending()
        if messages:
            for msg in messages:
                self.polled_messages.append(msg)

    def on_midi_message_received(self, messages):
        print(messages)
        print(self.active_setup)
        control = "None"
        if messages[0].is_cc():
            control = messages[0].control
            print(control)
        else:
            print("Invalid knob")

        self.midi_control_value[self.active_setup] = control
        self.update_setup_val_disp()
        self.diag_window_knob.hide()
        print("done")
        self.active_setup = ConfigSetupFlag.NONE

    def closeEvent(self, event):
        self.diag_window_knob.close()
        self.diag_window_pad.close()
        self.midi_poll_timer.stop()

    def set_text_diag_knob_setup(self, val_function):
        self.diag_window_knob.setText(hc_diag_knob_setup_txt + " " + val_function)

    def on_cancel_setup(self):
        self.midi_poll_timer.stop()
        self.diag_window_knob.hide()
        self.diag_window_pad.hide()

    def update_setup_val_disp(self):
        self.setup_knob_mode.lbl_knob_value.setText(
            str(self.midi_control_value[ConfigSetupFlag.MODE.value])
        )
        self.setup_knob_chord_comp.lbl_knob_value.setText(
            str(self.midi_control_value[ConfigSetupFlag.CHORD_COMP.value])
        )
        self.setup_knob_chord_size.lbl_knob_value.setText(
            str(self.midi_control_value[ConfigSetupFlag.CHORD_SIZE.value])
        )
        self.setup_knob_base_note.lbl_knob_value.setText(
            str(self.midi_control_value[ConfigSetupFlag.BASE_NOTE.value])
        )
        self.setup_knob_key_degree.lbl_knob_value.setText(
            str(self.midi_control_value[ConfigSetupFlag.KEY_DEGREE.value])
        )

    def on_ok_pad_setup(self):
        print("ok pad")
        self.midi_poll_timer.stop()
        print(self.polled_messages)
        base_note = 9999
        if self.polled_messages:
            if self.polled_messages[0].is_cc():
                self.midi_control_value.update({"pad_mode": "control_change"})
                for msg in self.polled_messages:
                    if msg.control < base_note:
                        base_note = msg.control
            else:
                self.midi_control_value.update({"pad_mode": "note"})
                for msg in self.polled_messages:
                    if msg.note < base_note:
                        base_note = msg.note
        self.midi_control_value[self.active_setup.value] = base_note
        self.active_setup = ConfigSetupFlag.NONE
        self.polled_messages = []
