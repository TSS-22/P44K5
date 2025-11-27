from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton,
    QFileDialog,
)
from PySide6.QtGui import QIcon
from gui.actions.action_refresh import QActionMidiRefresh
from gui.configs.combo_midi_list import CmbBoxMidiController

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

    def refresh_list_midi_controller(self):
        print("refresh midi controller list")

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
